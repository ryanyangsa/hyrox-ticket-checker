# 🏁 Hyrox Ticket Checker

하이록스 서울 시즌 경기의 **취소표 발생 여부를 실시간으로 감지**하고,  
**슬랙으로 자동 알림을 보내주는 Python 스크립트**입니다.

## 🚀 주요 기능

- ✅ 10초마다 티켓 페이지 실시간 체크
- ✅ ADAPTIVE 티켓 제외, 다른 티켓 등장 시 Slack 알림 발송
- ✅ 서버 시작 시 슬랙 알림
- ✅ 매일 오후 9시 정기 슬랙 상태 보고
- ✅ 모든 출력은 로그 파일로 저장 (`hyrox-ticket-checker.log`)
- ✅ 한국 시간(Asia/Seoul) 기준 동작

## 📦 설치 및 실행 방법

### 1. Python 의존 패키지 설치

```bash
pip install requests beautifulsoup4 pytz
```

### 2. 프로젝트 구조 예시

```
/app/hyrox-ticket-checker/
├── hyrox-ticket-checker.py
└── hyrox-ticket-checker.log
```

### 3. 실행

```bash
python hyrox-ticket-checker.py
```

## ⚙️ systemd 서비스로 실행 (선택)

**자동 실행 & 재시작을 원한다면 `systemd` 서비스 등록을 권장합니다.**

```ini
# /etc/systemd/system/hyrox-checker.service
[Unit]
Description=Hyrox Ticket Checker Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /app/hyrox-ticket-checker/hyrox-ticket-checker.py
WorkingDirectory=/app/hyrox-ticket-checker
Restart=always
User=nginx

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable hyrox-checker
sudo systemctl start hyrox-checker
```

## 🧪 테스트 메시지 전송

슬랙이 정상적으로 연결되었는지 확인하려면 아래 명령어로 테스트해보세요:

```bash
curl -X POST --data-urlencode "payload={
  \"channel\": \"#hyrox\",
  \"username\": \"하이록스 알리미 🤖\",
  \"text\": \"💪 슬랙 테스트 메시지입니다!\",
  \"icon_emoji\": \":muscle:\"
}" https://hooks.slack.com/services/당신의/웹훅/URL
```

## 📄 참고 사항

- Python 3.8 이상 지원 (한국 시간 처리를 위해 `pytz` 또는 Python 3.9+의 `zoneinfo` 사용 가능)
- 로그 파일 위치: `/app/hyrox-ticket-checker/hyrox-ticket-checker.log`
- 예매 URL: [Hyrox 서울 시즌](https://korea.hyrox.com/checkout/hyrox-seoul-season-25-26-2d8wvf)
- Slack Webhook은 직접 설정 필요: [Slack Webhook 만들기](https://api.slack.com/messaging/webhooks)

## 🙋‍♂️ Author

**라이언양**  
데이터와 도구를 사랑하는 개발자 💡  
🔗 Blog: [라이언양 블로그](https://blog.naver.com/ryanyangsa)  
📧 Contact: ryan.yang.sa@gmail.com
