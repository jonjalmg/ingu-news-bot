import os, requests, datetime, textwrap

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["6232391639"]

SYSTEM_MSG = (
    "너는 뉴스 요약봇이야. 정치·경제·산업·AI·자동차 등 "
    "의식주와 밀접한 국내외 주요 뉴스를 100줄로 요약해라. "
    "각 줄은 • 로 시작하고, 맨 끝에 (국가/출처) 표기."
)

def get_news_summary() -> str:
    res = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_MSG},
                {"role": "user", "content": "오늘 뉴스 요약해줘."},
            ],
            "temperature": 0.6,
        },
        timeout=30,
    )
    summary = res.json()["choices"][0]["message"]["content"].strip()
    # 날짜 헤더 추가
    kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    date_str = kst.strftime("%Y년 %m월 %d일 (%a)")
    return f"📰 {date_str} 주요 뉴스\n\n{summary}"

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def handler(event=None, context=None):
    try:
        news = get_news_summary()
        send_telegram(news)
    except Exception as e:
        send_telegram(f"❗️뉴스봇 오류: {e}")

if __name__ == "__main__":
    handler()
