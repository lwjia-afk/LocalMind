import pytest
from chat_manager import LLMChatManager

def test_create_new_chat():
    chat = LLMChatManager(None)
    assert len(chat.history) == 1
    assert chat.history[0].role.value == "system"
    assert chat.history[0].content == "You are a helpful assistant."

def test_add_user_message():
    chat = LLMChatManager(None)
    chat.add_user_message("Hello")
    assert len(chat.history) == 2
    assert chat.history[1].role.value == "user"
    assert chat.history[1].content == "Hello"

def test_add_assistant_message():
    chat = LLMChatManager(None)
    chat.add_assistant_message("Hi there!")
    assert len(chat.history) == 2
    assert chat.history[1].role.value == "assistant"
    assert chat.history[1].content == "Hi there!"

def test_add_system_message():
    chat = LLMChatManager(None)
    chat.add_system_message("New system prompt")
    assert len(chat.history) == 2
    assert chat.history[1].role.value == "system"
    assert chat.history[1].content == "New system prompt"

def test_reset_chat():
    chat = LLMChatManager(None)
    chat.add_user_message("Hello")
    chat.add_assistant_message("Hi there!")
    chat.reset()
    assert len(chat.history) == 1
    assert chat.history[0].role.value == "system"
    assert chat.history[0].content == "You are a helpful assistant."    

def test_ask_with_fake_llm():
    from tests.chat.llm.test_fake_llm import fakeLLMClient
    fake_llm = fakeLLMClient()
    chat = LLMChatManager(fake_llm)
    response = chat.ask("What is the weather today?")
    assert response == "This is a fake response from the fakeLLMClient."

