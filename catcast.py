import requests
import re

channel_url = "https://catcast.tv/AlvinOvcu"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://catcast.tv/"
}

def get_stream():
    try:
        r = requests.get(channel_url, headers=headers, timeout=10)
        html = r.text

        # ищем ID канала (очень важно!)
        match_id = re.search(r'channelId["\']?\s*[:=]\s*["\']?(\d+)', html)

        if not match_id:
            print("❌ Не найден ID канала")
            return None

        channel_id = match_id.group(1)
        print("Channel ID:", channel_id)

        # пробуем API Catcast
        api_url = f"https://api.catcast.tv/api/channel/{channel_id}"

        r2 = requests.get(api_url, headers=headers, timeout=10)

        if r2.status_code == 200:
            data = r2.text

            # ищем m3u8 в API
            match_stream = re.search(r'https?://[^"]+\.m3u8[^"]*', data)

            if match_stream:
                return match_stream.group(0)

        print("❌ Не найден поток через API")
        return None

    except Exception as e:
        print("Ошибка:", e)
        return None


def save_playlist(stream):
    with open("catcast.m3u8", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"#EXTINF:-1,AlvinOvcu\n{stream}\n")


if __name__ == "__main__":
    stream = get_stream()

    if stream:
        print("✅ Найден поток")
        save_playlist(stream)
    else:
        print("❌ Поток не найден")
