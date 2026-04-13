import requests
import random
import time
import os
import re
import json
import threading
from datetime import datetime

# ══════════════════════════════════════
#  JAP НАСТРОЙКИ
# ══════════════════════════════════════
JAP_API_KEY = "ec2fb6c8f5a4ea7ba6cf532e87a09895"
JAP_API_URL = "https://justanotherpanel.com/api/v2"

# ══════════════════════════════════════
#  TWITTER НАСТРОЙКИ
# ══════════════════════════════════════
TW_USERNAME  = "gowithRussia"
TW_SERVICE   = 1334
TW_QTY_MIN   = 800
TW_QTY_MAX   = 1500
TW_AUTH_TOKEN = "2dbd598ed7dac67ddcf07976325dbb708dd9e6e2"
TW_CT0        = "6b8b1822c5336aefde2892739247be0e645995eaa5f47fd6a99d109eb76596096ea8d667f91cc1c0021cd3afb84668920f8a01c06bd449302c70631c72a184816a16d96d8852c0d4b03c1aa75f4de043"
TW_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "Cookie": f"auth_token={TW_AUTH_TOKEN}; ct0={TW_CT0}",
    "X-Csrf-Token": TW_CT0,
    "X-Twitter-Auth-Type": "OAuth2Session",
    "X-Twitter-Active-User": "yes",
    "X-Twitter-Client-Language": "en",
    "Content-Type": "application/json",
    "Referer": "https://x.com/",
}

# ══════════════════════════════════════
#  FACEBOOK НАСТРОЙКИ
# ══════════════════════════════════════
FB_PAGE_ID  = "100081997113052"
FB_SERVICE  = 9604
FB_QTY_MIN  = 800
FB_QTY_MAX  = 1500
FB_C_USER = "61553351803414"
FB_XS     = "8%3AeGYkn8717BMe-g%3A2%3A1774503965%3A-1%3A-1%3A%3AAcx7QLCab5zvbi-lFeNFfZQcV-306iuKpPhQ-CMII9A"
FB_DATR   = "gvGqaR00HB8BBQCtWvA_ZrBw"
FB_FR     = "1OB7RBWOZkX1xBj3q.AWdGZvbe7aj44os6vwRpRCJ_yyTD61uZlfP5i6ymIVp0HkEp4Ck.Bp3GP7..AAA.0.0.Bp3GP7.AWfFHkYvPlNCbCa6-PGu_kEQVWs"
FB_SB     = "hfGqaZIWmBX2PQV9iqh9Tr1V"
FB_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": f"c_user={FB_C_USER}; xs={FB_XS}; datr={FB_DATR}; fr={FB_FR}; sb={FB_SB}",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity",
    "Referer": "https://www.facebook.com/",
}

# ══════════════════════════════════════
#  TIKTOK НАСТРОЙКИ
# ══════════════════════════════════════
TT_USERNAME  = "nationalcentrerussia"
TT_ORDERS    = [
    {"service": 8526, "min": 600, "max": 900},
    {"service": 8101, "min": 100, "max": 200},
]
TT_SESSION_ID = "77247692e0cd16885fab582db221fc7e"
TT_MS_TOKEN   = "FDpBoAbOm9dukueBFUfH47xHYuO-RX6yNiA4i5OgQDGPFtNtsoi0QXFGbeLNicKI4_oPnQm11AAU1bh6NftSI34r6IpjnRTSpXMT-iOa8MDgenfzPLJml-zBvHsd_f3w5l2k6yRS1kx6XrrtoQEzvppLrA=="
TT_TTWID      = "1%7CumJkmxsAGEmaKrymk0bKugDlfvWns9E_xl5fX6xU0IE%7C1776066751%7C5229c689f8cb2c94593653c4b4fb82011936a9132d466c3a1661ef99e41d9e7e"
TT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": f"sessionid={TT_SESSION_ID}; msToken={TT_MS_TOKEN}; ttwid={TT_TTWID}",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity",
    "Referer": "https://www.tiktok.com/",
}

CHECK_INTERVAL = 60

# ══════════════════════════════════════
#  ОБЩИЕ ФУНКЦИИ
# ══════════════════════════════════════
def log(platform, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{platform}] {msg}", flush=True)

def load_state(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            val = f.read().strip()
            return val if val else None
    return None

def save_state(filename, value):
    with open(filename, "w") as f:
        f.write(str(value))

def create_jap_order(platform, link, service, qty_min, qty_max):
    quantity = random.randint(qty_min, qty_max)
    payload = {
        "key":      JAP_API_KEY,
        "action":   "add",
        "service":  service,
        "link":     link,
        "quantity": quantity,
    }
    try:
        log(platform, f"📤 Заказ: service={service}, qty={quantity}")
        resp = requests.post(JAP_API_URL, data=payload, timeout=15)
        log(platform, f"📥 JAP: {resp.status_code} | {repr(resp.text[:200])}")
        if not resp.text.strip():
            log(platform, "❌ Пустой ответ JAP")
            return
        data = resp.json()
        if "order" in data:
            log(platform, f"✅ Заказ создан! ID: {data['order']} | Услуга: {service} | Кол-во: {quantity}")
        elif "error" in data:
            log(platform, f"❌ Ошибка JAP: {data['error']}")
    except Exception as e:
        log(platform, f"❌ Ошибка заказа: {e}")

def check_balance():
    try:
        resp = requests.post(JAP_API_URL, data={"key": JAP_API_KEY, "action": "balance"}, timeout=10)
        if resp.text.strip():
            data = resp.json()
            if "balance" in data:
                log("JAP", f"💰 Баланс: ${data['balance']} {data.get('currency','')}")
    except Exception as e:
        log("JAP", f"❌ Ошибка баланса: {e}")

# ══════════════════════════════════════
#  TWITTER
# ══════════════════════════════════════
def get_latest_tweet():
    try:
        url = "https://api.x.com/graphql/G3KGOASz96M-Qu0nwmGXNg/UserByScreenName"
        params = {
            "variables": f'{{"screen_name":"{TW_USERNAME}","withSafetyModeUserFields":true}}',
            "features": '{"hidden_profile_subscriptions_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
        }
        resp = requests.get(url, headers=TW_HEADERS, params=params, timeout=15)
        if resp.status_code != 200:
            log("Twitter", f"⚠️  UserByScreenName: {resp.status_code}")
            return None, None
        data = resp.json()
        user_id = data["data"]["user"]["result"]["rest_id"]

        url2 = "https://api.x.com/graphql/E3opETHurmVJflFsUBVuUQ/UserTweets"
        params2 = {
            "variables": f'{{"userId":"{user_id}","count":5,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}}',
            "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        }
        resp2 = requests.get(url2, headers=TW_HEADERS, params=params2, timeout=15)
        if resp2.status_code != 200:
            log("Twitter", f"⚠️  UserTweets: {resp2.status_code}")
            return None, None

        data2 = resp2.json()
        entries = data2["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
        tweet_ids = []
        for instruction in entries:
            if instruction.get("type") == "TimelineAddEntries":
                for entry in instruction.get("entries", []):
                    entry_id = entry.get("entryId", "")
                    if entry_id.startswith("tweet-"):
                        tweet_ids.append(entry_id.replace("tweet-", ""))

        if not tweet_ids:
            log("Twitter", "⚠️  Твиты не найдены")
            return None, None

        latest_id = max(tweet_ids, key=lambda x: int(x))
        tweet_url = f"https://x.com/{TW_USERNAME}/status/{latest_id}"
        return latest_id, tweet_url

    except Exception as e:
        log("Twitter", f"❌ Ошибка: {e}")
        return None, None

def twitter_bot():
    log("Twitter", f"🐦 Запущен | @{TW_USERNAME} | Услуга: {TW_SERVICE} | {TW_QTY_MIN}-{TW_QTY_MAX}")
    last_id = load_state("last_tweet_id.txt")

    if not last_id:
        latest_id, _ = get_latest_tweet()
        if latest_id:
            save_state("last_tweet_id.txt", latest_id)
            last_id = latest_id
            log("Twitter", f"📌 Первый запуск. Последний твит: #{latest_id}")

    while True:
        try:
            latest_id, tweet_url = get_latest_tweet()
            if latest_id and int(latest_id) > int(last_id):
                log("Twitter", f"🆕 Новый твит: {tweet_url}")
                create_jap_order("Twitter", tweet_url, TW_SERVICE, TW_QTY_MIN, TW_QTY_MAX)
                save_state("last_tweet_id.txt", latest_id)
                last_id = latest_id
            else:
                log("Twitter", f"🔍 Нет новых твитов (последний: #{last_id})")
        except Exception as e:
            log("Twitter", f"❌ Ошибка: {e}")
        time.sleep(CHECK_INTERVAL)

# ══════════════════════════════════════
#  FACEBOOK
# ══════════════════════════════════════
def get_latest_fb_post():
    try:
        url = f"https://www.facebook.com/profile.php?id={FB_PAGE_ID}"
        resp = requests.get(url, headers=FB_HEADERS, timeout=15)
        log("Facebook", f"📥 Status: {resp.status_code}")
        if resp.status_code != 200:
            return None, None

        html = resp.content.decode("utf-8", errors="ignore")

        matches = re.findall(r'pfbid[A-Za-z0-9]+', html)
        if matches:
            latest_pfbid = matches[0]
            post_url = f"https://www.facebook.com/permalink.php?story_fbid={latest_pfbid}&id={FB_PAGE_ID}"
            log("Facebook", f"✅ Пост найден: {post_url}")
            return latest_pfbid, post_url

        ids = []
        for pattern in [r'"story_fbid":"(\d+)"', r'"post_id":"(\d+)"', r'"top_level_post_id":"(\d+)"']:
            ids += re.findall(pattern, html)

        numeric = [x for x in set(ids) if x.isdigit() and len(x) > 10]
        if numeric:
            latest_id = max(numeric, key=lambda x: int(x))
            post_url = f"https://www.facebook.com/permalink.php?story_fbid={latest_id}&id={FB_PAGE_ID}"
            log("Facebook", f"✅ Пост найден: {post_url}")
            return latest_id, post_url

        log("Facebook", "⚠️  Посты не найдены")
        return None, None

    except Exception as e:
        log("Facebook", f"❌ Ошибка: {e}")
        return None, None

def facebook_bot():
    log("Facebook", f"📘 Запущен | ID: {FB_PAGE_ID} | Услуга: {FB_SERVICE} | {FB_QTY_MIN}-{FB_QTY_MAX}")
    last_id = load_state("last_fb_post_id.txt")

    if not last_id:
        latest_id, _ = get_latest_fb_post()
        if latest_id:
            save_state("last_fb_post_id.txt", latest_id)
            last_id = latest_id
            log("Facebook", f"📌 Первый запуск. Последний пост: #{latest_id}")

    while True:
        try:
            latest_id, post_url = get_latest_fb_post()
            if latest_id and latest_id != last_id:
                log("Facebook", f"🆕 Новый пост: {post_url}")
                create_jap_order("Facebook", post_url, FB_SERVICE, FB_QTY_MIN, FB_QTY_MAX)
                save_state("last_fb_post_id.txt", latest_id)
                last_id = latest_id
            else:
                log("Facebook", f"🔍 Нет новых постов (последний: #{last_id})")
        except Exception as e:
            log("Facebook", f"❌ Ошибка: {e}")
        time.sleep(CHECK_INTERVAL)

# ══════════════════════════════════════
#  TIKTOK
# ══════════════════════════════════════
def get_latest_tiktok():
    try:
        url = f"https://www.tiktok.com/@{TT_USERNAME}"
        resp = requests.get(url, headers=TT_HEADERS, timeout=15)
        log("TikTok", f"📥 Status: {resp.status_code}")
        if resp.status_code != 200:
            return None, None

        html = resp.content.decode("utf-8", errors="ignore")

        sigi = re.search(r'<script id="SIGI_STATE"[^>]*>(.*?)</script>', html, re.DOTALL)
        if sigi:
            try:
                data = json.loads(sigi.group(1))
                item_module = data.get("ItemModule", {})
                if item_module:
                    video_ids = list(item_module.keys())
                    if video_ids:
                        latest_id = max(video_ids, key=lambda x: int(x) if x.isdigit() else 0)
                        video_url = f"https://www.tiktok.com/@{TT_USERNAME}/video/{latest_id}"
                        log("TikTok", f"✅ Видео найдено: {video_url}")
                        return latest_id, video_url
            except Exception as e:
                log("TikTok", f"⚠️  SIGI error: {e}")

        ids = re.findall(r'tiktok\.com/@' + TT_USERNAME + r'/video/(\d+)', html)
        ids += re.findall(r'"aweme_id":"(\d+)"', html)
        if ids:
            latest_id = max(ids, key=lambda x: int(x))
            video_url = f"https://www.tiktok.com/@{TT_USERNAME}/video/{latest_id}"
            log("TikTok", f"✅ Видео найдено: {video_url}")
            return latest_id, video_url

        log("TikTok", "⚠️  Видео не найдены")
        return None, None

    except Exception as e:
        log("TikTok", f"❌ Ошибка: {e}")
        return None, None

def tiktok_bot():
    log("TikTok", f"🎵 Запущен | @{TT_USERNAME}")
    log("TikTok", f"⚙️  Заказы: 8526 ({TT_ORDERS[0]['min']}-{TT_ORDERS[0]['max']}) + 8101 ({TT_ORDERS[1]['min']}-{TT_ORDERS[1]['max']})")
    last_id = load_state("last_tiktok_id.txt")

    if not last_id:
        latest_id, _ = get_latest_tiktok()
        if latest_id:
            save_state("last_tiktok_id.txt", latest_id)
            last_id = latest_id
            log("TikTok", f"📌 Первый запуск. Последнее видео: #{latest_id}")

    while True:
        try:
            latest_id, video_url = get_latest_tiktok()
            if latest_id and int(latest_id) > int(last_id):
                log("TikTok", f"🆕 Новое видео: {video_url}")
                for order in TT_ORDERS:
                    create_jap_order("TikTok", video_url, order["service"], order["min"], order["max"])
                    time.sleep(2)
                save_state("last_tiktok_id.txt", latest_id)
                last_id = latest_id
            else:
                log("TikTok", f"🔍 Нет новых видео (последнее: #{last_id})")
        except Exception as e:
            log("TikTok", f"❌ Ошибка: {e}")
        time.sleep(CHECK_INTERVAL)

# ══════════════════════════════════════
#  MAIN
# ══════════════════════════════════════
def main():
    log("MAIN", "🚀 Объединённый бот запущен!")
    check_balance()

    threads = [
        threading.Thread(target=twitter_bot, name="Twitter", daemon=True),
        threading.Thread(target=facebook_bot, name="Facebook", daemon=True),
        threading.Thread(target=tiktok_bot, name="TikTok", daemon=True),
    ]

    for t in threads:
        t.start()
        time.sleep(5)

    log("MAIN", "✅ Все боты запущены! Twitter + Facebook + TikTok")

    while True:
        time.sleep(3600)

if __name__ == "__main__":
    main()
