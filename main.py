import os
from dotenv import load_dotenv
import api

load_dotenv()


def main():
    token = os.getenv("PERSONAL_ACCESS_TOKEN")
    username = os.getenv("USER")
    base_url = os.getenv("BASE_URL", "https://api.github.com/")
    time_sleep = os.getenv("TIME_SLEEP", "1")

    # Eksik ayarları kontrol et
    if not token:
        raise ValueError("PERSONAL_ACESS_TOKEN bulunamadı (.env dosyasını kontrol et).")

    if not username:
        raise ValueError("USER bulunamadı (.env dosyasını kontrol et).")

    if not base_url.endswith("/"):
        base_url += "/"

    print(f"Kullanıcı: {username}")
    print(f"API: {base_url}")
    print(f"Bekleme süresi: {time_sleep} sn")
    print("-" * 40)

    api.unfollow_back(
        base_url,
        time_sleep,
        username,
        token,
    )


if __name__ == "__main__":
    main()
