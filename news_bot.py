import os
import requests
import feedparser

# 讀取你的小米專屬接收頻道：hk-news-168168168
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "hk-news-168168168")

# 依照指定來源精選的優質 RSS
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
    blocks = []
    for cat in CATEGORIES:
        try:
            feed = feedparser.parse(cat["url"])
            items = []
            # 每個項目嚴格擷取最新 5 則新聞
            for entry in feed.entries[:5]:
                title = entry.title.strip()
                items.append(f"• {title}")
            
            if items:
                section_text = f"【{cat['name']}】\n" + "\n".join(items)
                blocks.append(section_text)
        except Exception as e:
            print(f"擷取 {cat['name']} 失敗: {e}")
            continue
    return "\n\n".join(blocks)

def send_ntfy(title, body):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    headers = {
        "Title": title.encode("utf-8"),
        "Tags": "newspaper,hong_kong",
        "Priority": "default"
    }
    try:
        resp = requests.post(url, data=body.encode("utf-8"), headers=headers, timeout=25)
        print("ntfy 推送結果代碼：", resp.status_code)
    except Exception as e:
        print("發送失敗：", e)

if __name__ == "__main__":
    news = get_top_news()
    if news:
        send_ntfy("☀️ 早晨新聞速遞（精選5則）", news)
