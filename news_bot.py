import os
import requests
import feedparser

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

CATEGORIES = [
    {
        "name": "📰 香港時事（大型來源）",
        "url": "https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml"
    },
    {
        "name": "🤖 科技與AI（香港及台灣）",
        "url": "https://technews.tw/feed/"
    },
    {
        "name": "⚽ 國際足球（英國權威來源）",
        "url": "https://feeds.bbci.co.uk/sport/football/rss.xml"
    },
    {
        "name": "🏇 香港賽馬（香港賽馬會官方）",
        "url": "https://racingnews.hkjc.com/chinese/feed/"
    },
    {
        "name": "🎬 香港娛樂（全港大型來源）",
        "url": "https://rthk.hk/rthk/news/rss/c_expressnews_centertainment.xml"
    }
]

def get_top_news():
    blocks = ["☀️ <b>【早晨新聞速遞】</b>\n"]
    for cat in CATEGORIES:
        try:
            feed = feedparser.parse(cat["url"])
            items = []
            # 每個項目嚴格精選 5 則最新頭條
            for entry in feed.entries[:5]:
                title = entry.title.strip().replace("<", "&lt;").replace(">", "&gt;")
                link = entry.link.strip() if hasattr(entry, 'link') else ""
                if link:
                    items.append(f"• <a href='{link}'>{title}</a>")
                else:
                    items.append(f"• {title}")
            
            if items:
                section_text = f"<b>{cat['name']}</b>\n" + "\n".join(items)
                blocks.append(section_text)
        except Exception as e:
            print(f"擷取 {cat['name']} 失敗: {e}")
            continue
    return "\n\n".join(blocks)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, json=payload, timeout=20)
        print("Telegram 發送結果：", resp.status_code, resp.text)
    except Exception as e:
        print("發送出錯：", e)

if __name__ == "__main__":
    if BOT_TOKEN and CHAT_ID:
        content = get_top_news()
        send_telegram(content)
    else:
        print("請確保 GitHub Secrets 已設定 TELEGRAM_BOT_TOKEN 與 TELEGRAM_CHAT_ID")
