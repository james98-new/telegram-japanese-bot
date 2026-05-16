from openai import OpenAI
import requests
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

HISTORY_FILE = "history.json"
MAX_HISTORY = 90


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


history = load_history()
used_quotes = "
".join(history)

prompt = f"""
请生成一条适合日常使用的日语谚语。

要求：
1. 必须与以下内容完全不同，绝对不要重复：
{used_quotes}

2. 严格按照以下格式输出：
print("发送成功（90天防重复已开启）")