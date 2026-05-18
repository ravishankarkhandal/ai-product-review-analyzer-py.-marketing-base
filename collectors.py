import requests
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID, YOUTUBE_API_KEY, MAX_REVIEWS_PER_SOURCE


# ── Helper ────────────────────────────────────────────
def _google_search(query, num=MAX_REVIEWS_PER_SOURCE):
    """Generic Google Custom Search wrapper."""
    try:
        resp = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={"key": GOOGLE_API_KEY, "cx": GOOGLE_CSE_ID, "q": query, "num": num},
            timeout=10,
        )
        return resp.json().get("items", [])
    except Exception as e:
        print(f"  ⚠️  Google Search error: {e}")
        return []


# ── Platform Collectors ───────────────────────────────
def collect_google_reviews(product):
    items = _google_search(f"{product} review")
    return [
        {"source": "Google", "title": i.get("title", ""), "snippet": i.get("snippet", ""), "link": i.get("link", "")}
        for i in items
    ]


def collect_youtube_reviews(product):
    reviews = []
    try:
        resp = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "key": YOUTUBE_API_KEY,
                "q": f"{product} review",
                "part": "snippet",
                "type": "video",
                "maxResults": MAX_REVIEWS_PER_SOURCE,
                "order": "relevance",
            },
            timeout=10,
        )
        for item in resp.json().get("items", []):
            snip = item.get("snippet", {})
            vid  = item.get("id", {}).get("videoId", "")
            reviews.append({
                "source": "YouTube",
                "title":   snip.get("title", ""),
                "snippet": snip.get("description", ""),
                "link":    f"https://www.youtube.com/watch?v={vid}",
            })
    except Exception as e:
        print(f"  ⚠️  YouTube error: {e}")
    return reviews


def collect_amazon_reviews(product):
    """Amazon reviews via Google Custom Search filtered to amazon.com"""
    items = _google_search(f"{product} review site:amazon.com")
    return [
        {"source": "Amazon", "title": i.get("title", ""), "snippet": i.get("snippet", ""), "link": i.get("link", "")}
        for i in items
    ]


# ── Master Collector ──────────────────────────────────
def collect_all_reviews(product):
    print(f"\n🔍  Collecting reviews for: {product}\n")
    all_reviews = []

    print("  📌  Google Reviews …")
    all_reviews.extend(collect_google_reviews(product))

    print("  📺  YouTube Reviews …")
    all_reviews.extend(collect_youtube_reviews(product))

    print("  🛒  Amazon Reviews …")
    all_reviews.extend(collect_amazon_reviews(product))

    print(f"\n  ✅  Total reviews collected: {len(all_reviews)}")
    return all_reviews