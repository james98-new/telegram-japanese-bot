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


def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        print("Telegram 推送成功")
    else:
        print(f"Telegram 推送失败: {res.text}")


def main():
    history = load_history()
    used_quotes = "\n".join(history)

    prompt = f"""请生成一条适合日常使用的日语谚语。

要求：
1. 必须与以下内容完全不同，绝对不要重复：
{used_quotes}

2. 严格按照以下格式输出，不要输出任何其他内容：

【谚语】
（日语原句）

【读音】
（平假名标注）

【中文翻译】
（翻译内容）

【职场应用】
（针对职场新人的场景解析，100字以内）"""

    # 调用 OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=1.0
    )

    ai_text = response.choices[0].message.content.strip()
    print("AI 返回内容：\n" + ai_text)

    # 推送到 Telegram
    send_telegram(ai_text)

    # 提取谚语原句并更新历史
    import re
    match = re.search(r"【谚语】\s*(.*?)\n", ai_text)
    if match:
        new_quote = match.group(1).strip()
        history.append(new_quote)
        # 只保留最近 MAX_HISTORY 条
        if len(history) > MAX_HISTORY:
            history = history[-MAX_HISTORY:]
        save_history(history)
        print(f"已记录谚语：{new_quote}（共 {len(history)} 条）")
    else:
        print("未能提取谚语原句，请检查 AI 返回格式")


if __name__ == "__main__":
    main()
