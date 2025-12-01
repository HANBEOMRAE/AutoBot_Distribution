🤖 AutoBot Distribution (자동매매 봇)

트레이딩뷰(TradingView)의 웹훅 신호를 받아 바이낸스(Binance)에서 자동으로 매매를 수행하는 봇입니다.
도메인이 없어도, 리눅스를 몰라도 누구나 쉽게 설치할 수 있도록 설계되었습니다.

✨ 주요 기능

자동 설치: 명령어 한 줄로 파이썬, Nginx, SSL(보안)까지 한 번에 설치

웹훅 보안: 비밀번호(Secret) 검증 기능으로 해킹 방지

간편 설정: 메모장(config.ini)으로 API 키 관리

이중 모드: 도메인(HTTPS) 연결 모드 / IP(HTTP) 전용 모드 지원

🚀 설치 방법 (따라만 하세요!)

AWS EC2(Ubuntu) 터미널을 열고 아래 명령어 3줄을 순서대로 입력하세요.

1. 코드 다운로드

git clone [https://github.com/HANBEOMRAE/AutoBot_Distribution.git](https://github.com/HANBEOMRAE/AutoBot_Distribution.git)


2. 폴더로 이동

cd AutoBot_Distribution


3. 자동 설치 시작 (마법의 명령어)

bash install.sh


설치 중에 "도메인이 있습니까?" 라고 물어보면 상황에 맞춰 y 또는 n을 입력하세요.

⚙️ 설정 방법

설치가 끝나면 폴더 안에 있는 config.ini 파일을 열어 정보를 입력해야 합니다.

nano config.ini


[BINANCE]: 본인의 바이낸스 API Key / Secret Key 입력

[SECURITY]: 웹훅 비밀번호 설정 (트레이딩뷰 알림에도 똑같이 적어야 함)

Ctrl+X, Y, Enter를 눌러서 저장하고 나옵니다.

▶️ 실행 방법

설정이 끝났으면 아래 명령어로 봇을 실행하세요. (이제 터미널을 꺼도 봇은 계속 돌아갑니다.)

./start.sh


📊 트레이딩뷰 알림 설정 (JSON 포맷)

트레이딩뷰 알림 메시지(Message) 칸에 아래 형식을 사용하세요.

{
  "secret": "config.ini에_적은_비밀번호",
  "symbol": "BTCUSDT",
  "action": "BUY",
  "strategy": "Trend_V1"
}



4.  다 붙여넣으셨으면 아래 초록색 버튼 **[Commit changes]**를 누르세요.

---

### [2단계] 진짜 고객이 되어보기 (테스트)

이제 가장 중요한 순서입니다. **"내 컴퓨터(서버)가 아닌 다른 곳에서도 진짜 설치가 잘 될까?"**

현재 운영 중인 EC2 서버에서 테스트해도 되지만, **가장 확실한 방법**은 AWS에서 **무료 서버(t2.micro)**를 하나 새로 만들어서 거기서 테스트해보는 것입니다. (고객들은 텅 빈 서버에서 시작할 테니까요.)

만약 새 서버를 만들기 귀찮으시다면, **현재 서버에서 테스트하되 아래 주의사항을 지켜주세요.**

#### ⚠️ 현재 서버에서 테스트할 때 주의사항
* `install.sh`는 **Nginx(웹서버)**를 설치합니다. 만약 현재 서버에 이미 다른 웹서버가 돌아가고 있다면 충돌 날 수 있습니다.
* (아까 대화 내용으로는 파이썬 봇만 돌리고 계시니 큰 문제는 없을 겁니다.)

#### 테스트 명령어 (터미널에 입력)
```bash
# 1. 홈으로 이동
cd ~

# 2. 깃허브에서 다운로드 (방금 올린 따끈따끈한 파일)
git clone https://github.com/HANBEOMRAE/AutoBot_Distribution.git

# 3. 폴더 입장
cd AutoBot_Distribution

# 4. 설치 스크립트 실행
bash install.sh
