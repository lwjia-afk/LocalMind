from dataclasses import dataclass

@dataclass
class llmResult:
    text : str
    raw : dict
    def __getitem__(self, key):
        return self.raw[key]