#!/bin/bash

# 색상 설정 (예쁘게 보이게)
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}   자동매매 봇 서버 설치 도우미 (Ubuntu 전용)${NC}"
echo -e "${GREEN}==================================================${NC}"

# 1. 시스템 업데이트 및 필수 프로그램 설치
echo "Step 1/5: 시스템 업데이트 및 필수 프로그램(Nginx, Certbot) 설치 중..."
sudo apt-get update
# nginx: 웹서버, certbot: SSL인증서 발급기
sudo apt-get install -y python3-pip python3-venv nginx certbot python3-certbot-nginx git

# 2. 파이썬 가상환경 설정
echo "Step 2/5: 파이썬 가상환경 설정 중..."
python3 -m venv venv
source venv/bin/activate

# 필수 라이브러리 설치 (requirements.txt + 서버 구동용 패키지)
pip install -r requirements.txt
pip install uvicorn fastapi gunicorn requests

# 3. 도메인 설정 (핵심 부분)
echo -e "${GREEN}==================================================${NC}"
echo "도메인(예: mybot.com)을 구매하고, DNS 설정에서 이 서버의 IP를 연결하셨나요?"
read -p "도메인이 준비되었으면 'y', 없으면 'n'을 입력하세요: " setup_domain

if [ "$setup_domain" = "y" ]; then
    read -p "사용할 도메인 주소를 입력하세요 (예: mybot.com): " DOMAIN_NAME
    
    echo "Step 3/5: Nginx(웹서버)를 도메인 모드로 설정합니다..."
    
    # Nginx 설정 파일 작성 (도메인 -> 내부 8000포트로 전달)
    sudo tee /etc/nginx/sites-available/mybot > /dev/null <<EOF
server {
    server_name $DOMAIN_NAME;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

    # 설정 활성화
    sudo ln -s /etc/nginx/sites-available/mybot /etc/nginx/sites-enabled/
    sudo rm /etc/nginx/sites-enabled/default 2>/dev/null
    
    # SSL 인증서 발급 (Certbot이 자동으로 Nginx 설정을 고쳐서 https로 만듦)
    echo "Step 4/5: SSL 보안 인증서(자물쇠) 발급 시도..."
    sudo certbot --nginx -d $DOMAIN_NAME

else
    echo "Step 3/5: 도메인 없이 IP 모드(포트 80)로 설정합니다. (보안상 도메인 권장)"
    
    # Nginx 설정 파일 작성 (IP용)
    sudo tee /etc/nginx/sites-available/mybot_ip > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF
    sudo ln -s /etc/nginx/sites-available/mybot_ip /etc/nginx/sites-enabled/
    sudo rm /etc/nginx/sites-enabled/default 2>/dev/null
    echo "SSL 설정은 건너뜁니다."
fi

# 4. Nginx 재시작
echo "Step 5/5: 웹 서버 재시작 및 마무리..."
sudo nginx -t
sudo systemctl restart nginx

# 5. 실행 권한 부여
chmod +x start.sh

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}   설치가 모두 완료되었습니다!${NC}"
echo -e "   1. config.ini 파일을 열어 API 키와 비밀번호를 입력하세요."
echo -e "   2. ./start.sh 명령어로 봇을 실행하세요."
echo -e "${GREEN}==================================================${NC}"