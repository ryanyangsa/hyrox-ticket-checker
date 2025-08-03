import time
import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime
from pytz import timezone

# ✅ 한국 시간대 설정
KST = ZoneInfo("Asia/Seoul")

# ✅ 로그 파일 설정
log_file = open("/app/hyrox-ticket-checker/hyrox-ticket-checker.log", "a", buffering=1)
sys.stdout = log_file
sys.stderr = log_file

print(f"\n\n===== 서비스 시작: {datetime.now(KST)} =====\n")

# ✅ 슬랙 설정
SLACK_WEBHOOK_URL = "슬랙 웹훅 URL 입력"
SLACK_CHANNEL = "#hyrox"
SLACK_USERNAME = "하이록스 티켓 알리미 🤖"
SLACK_ICON = ":muscle:"

# ✅ 티켓 체크 설정
CHECK_URL = "https://korea.hyrox.com/checkout/hyrox-seoul-season-25-26-2d8wvf"
IGNORE_KEYWORDS = ["HYROX ADAPTIVE MEN", "HYROX ADAPTIVE WOMEN"]

def send_slack_alert(message):
    payload = {
        "channel": SLACK_CHANNEL,
        "username": SLACK_USERNAME,
        "text": message,
        "icon_emoji": SLACK_ICON
    }
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("✅ 슬랙 알림 전송 완료!")
    except Exception as e:
        print("❌ 슬랙 알림 실패:", e)

def check_ticket():
    response = requests.get(CHECK_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    found_tickets = []
    for tag in soup.find_all(string=True):
        text = tag.strip()
        if "HYROX" in text and any(word in text for word in ["MEN", "WOMEN", "DOUBLES", "RELAY"]):
            if not any(ignore in text for ignore in IGNORE_KEYWORDS):
                found_tickets.append(text)

    if found_tickets:
        print("🎉 새로운 티켓 발견!")
        for ticket in found_tickets:
            print(f"→ {ticket}")
        message = (
            f"🎉 새로운 티켓이 나타났어요! (KST {datetime.now(KST).strftime('%Y-%m-%d %H:%M')})\n\n"
            + "\n".join(f"• {t}" for t in found_tickets)
            + f"\n\n예매 페이지: {CHECK_URL}"
        )
        send_slack_alert(message)
    else:
        print("⏳ 아직 취소표 없음 (ADAPTIVE 외 티켓 없음)")

# ✅ 서버 시작 시 슬랙 알림
send_slack_alert(f"🚀 하이록스 티켓 체크 서비스가 시작되었습니다! (KST {datetime.now(KST).strftime('%Y-%m-%d %H:%M')})")

# ⏰ 마지막 매일 점검 알림 보낸 날짜 저장용
last_daily_report_date = None

if __name__ == "__main__":
    while True:
        try:
            check_ticket()

            # ✅ 매일 오후 9시 상태 체크 알림
            now = datetime.now(KST)
            if now.hour == 21 and (last_daily_report_date is None or last_daily_report_date != now.date()):
                send_slack_alert(f"🕘 매일 점검: 티켓 체크 서비스 정상 동작 중입니다. (KST {now.strftime('%Y-%m-%d %H:%M')})")
                last_daily_report_date = now.date()

        except Exception as e:
            print("⚠️ 오류 발생:", e)

        time.sleep(10)  # ⏲️ 10초마다 체크
