# LocalMind — Présentation de l'Architecture

## Ce que j'ai construit

**LocalMind** est un framework de conversation LLM local, développé en Python.  
Il permet à un utilisateur d'avoir des conversations multi-tours avec un LLM fonctionnant localement (via Ollama),  
avec un suivi complet de l'historique et une journalisation structurée — le tout **100% hors ligne**.

---

## Architecture du système

```
┌─────────────────────────────────────────────────────────────────┐
│                      Client / Utilisateur                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │  ask("Bonjour", session_id)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Chat Manager                              │
│                                                                 │
│   1. Ajouter le message utilisateur à la session               │
│   2. Récupérer l'historique complet de la conversation         │
│   3. Appeler le LLM avec cet historique                        │
│   4. Ajouter la réponse de l'assistant à la session            │
│   5. Retourner la réponse                                       │
└──────────┬──────────────────────────────┬───────────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐      ┌───────────────────────────────────┐
│   Session Store      │      │         Couche LLM                │
│                      │      │                                   │
│  { UUID → Session }  │      │   baseLlmClient  (abstrait)       │
│                      │      │         │                         │
│  Session :           │      │         ▼                         │
│   - session_id       │      │   OllamaClient                    │
│   - user             │      │   POST /api/chat                  │
│   - history[ ]       │      │   → localhost:11434               │
└──────────────────────┘      └───────────────────────────────────┘
           │                              │
           └──────────────┬───────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Systèmes de support                          │
│                                                                 │
│   ┌──────────────────────┐   ┌───────────────────────────────┐  │
│   │   Config Manager     │   │        Log Manager            │  │
│   │   (config.yaml via   │   │  Console + Fichier rotatif    │  │
│   │     OmegaConf)       │   │  logs/localmind.log (5Mo×3)   │  │
│   └──────────────────────┘   └───────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Décision de conception clé :** La couche LLM est derrière une interface abstraite (`baseLlmClient`).  
Remplacer Ollama par OpenAI ou un autre fournisseur ne nécessite qu'une nouvelle classe — sans toucher au reste du système.

---

## Gestion de l'historique de conversation

### Le problème fondamental
Les LLM sont sans état — chaque appel HTTP est indépendant.  
Pour avoir une conversation multi-tours, le client doit **maintenir et rejouer l'historique** à chaque requête.

### Ma conception

```
                    ┌─────────────────────────────────┐
                    │            Session               │
                    │                                  │
                    │  session_id: "a3f2-..."  (UUID)  │
                    │  user:       "alice"             │
                    │  history: [                      │
                    │    { role: SYSTEM,    contenu }  │
                    │    { role: USER,      contenu }  │
                    │    { role: ASSISTANT, contenu }  │
                    │    { role: USER,      contenu }  │  ← grandit à chaque tour
                    │    ...                           │
                    │  ]                               │
                    └─────────────────────────────────┘
```

**Architecture en trois couches :**

```
 Couche Modèles      Couche Stockage       Couche Orchestration
┌────────────┐      ┌──────────────┐      ┌──────────────────┐
│  Message   │      │ SessionStore │      │   ChatManager    │
│  - role    │  ──► │              │  ──► │                  │
│  - content │      │ dict de      │      │ pilote le flux   │
│  - timestamp│     │ Sessions     │      │ ask()            │
│  - metadata│      │ indexé par   │      │                  │
└────────────┘      │    UUID      │      └──────────────────┘
                    └──────────────┘
```

**Flux pour chaque tour :**
```
ask("Qu'est-ce que Python ?", session_id)
        │
        ├── [1] Stocker le message utilisateur dans session.history
        │
        ├── [2] Sérialiser l'historique → [{"role": "user", "content": "..."}, ...]
        │
        ├── [3] POST historique complet vers Ollama
        │              (le LLM voit toute la conversation)
        │
        ├── [4] Stocker la réponse de l'assistant dans session.history
        │
        └── [5] Retourner le texte de la réponse
```

**Support multi-sessions :** Chaque session reçoit un UUID à la création.  
Plusieurs utilisateurs (ou conversations) peuvent fonctionner en parallèle — parfaitement isolés les uns des autres.

**Compromis assumé :** L'historique vit en mémoire (rapide, simple), pas sur disque.  
C'est un choix délibéré pour la portée actuelle — le point d'extension est clair :  
remplacer `SessionStore` par une version persistante en base de données sans toucher à rien d'autre.

---

## Journalisation structurée

### Objectifs de conception
- Toute opération traçable de bout en bout
- Identifier **quel module** a émis un log sans lire le code
- Résister aux processus longs (pas de croissance illimitée des logs)

### Format des logs

```
[2026-04-09 19:36:25] [INFO]  chat_manager: Asking: Qu'est-ce que Python ?
[2026-04-09 19:36:25] [INFO]  chat_manager: User: Qu'est-ce que Python ?
[2026-04-09 19:36:25] [INFO]  llm.ollama:   generate called — model: qwen2.5:7b
[2026-04-09 19:36:28] [INFO]  chat_manager: Assistant: Python est ...
[2026-04-09 19:43:10] [ERROR] llm.ollama:   Cannot connect to Ollama at localhost:11434
```

`[horodatage]  [niveau]  nom_du_module: message`

### Architecture à deux canaux

```
                  ┌──────────────────┐
                  │   LogManager     │
                  │   (singleton)    │
                  └────────┬─────────┘
                           │ formate avec
                           │ [heure][niveau] module: msg
                    ┌──────┴──────┐
                    │             │
              ┌─────▼─────┐  ┌───▼──────────────────────┐
              │  Console  │  │  Gestionnaire fichier     │
              │  (stdout) │  │  rotatif                  │
              └───────────┘  │  logs/localmind.log       │
                             │  max 5 Mo × 3 sauvegardes │
                             └───────────────────────────┘
```

**Pattern Singleton :** `LogManager` s'initialise une seule fois au démarrage.  
Chaque module appelle ensuite `LogManager.get_logger("nom_du_module")` pour obtenir son propre logger nommé.  
Le framework de logging Python route tous les loggers nommés vers les mêmes handlers racine — un seul `init()` câble tout.

**Fichier rotatif :** Plafonné à 5 Mo, conserve 3 sauvegardes (`localmind.log`, `.log.1`, `.log.2`).  
Évite la saturation du disque sur des déploiements longue durée.

---

## Résumé — Décisions de conception

| Domaine | Décision | Pourquoi |
|---------|----------|----------|
| Backend LLM | Interface abstraite + implémentation Ollama | Changer de backend sans toucher à la logique métier |
| Historique | Dict en mémoire, replay complet par requête | Simple, correct ; la couche stockage est facilement remplaçable |
| IDs de session | UUID | Pas de collision, pas de coordination nécessaire |
| Journalisation | Singleton + loggers nommés + fichier rotatif | Un seul init, traçable par module, usage disque borné |
| Configuration | OmegaConf + YAML | Accès par notation pointée, facile à surcharger par environnement |
