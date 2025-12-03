import os
import configparser
import logging

logger = logging.getLogger("config")

# 1. 설정 파일 읽기
config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

if os.path.exists(CONFIG_PATH):
    config.read(CONFIG_PATH, encoding='utf-8')

# =========================================================
# 2. 바이낸스 API 키 (없어도 통과)
# =========================================================
EX_API_KEY    = config.get('BINANCE', 'api_key', fallback="")
EX_API_SECRET = config.get('BINANCE', 'secret_key', fallback="")
WEBHOOK_SECRET = config.get('SECURITY', 'webhook_secret', fallback="my_secret_password")

# =========================================================
# 3. 거래 설정 (이 부분이 빠져서 에러가 났던 겁니다!)
# =========================================================
DRY_RUN        = config.getboolean('TRADING', 'dry_run', fallback=True)
BUY_PCT        = config.getfloat('TRADING', 'buy_pct', fallback=0.98)
TRADE_LEVERAGE = config.getint('TRADING', 'trade_leverage', fallback=5)
POLL_INTERVAL  = config.getfloat('TRADING', 'poll_interval', fallback=1.0)
MAX_WAIT       = config.getint('TRADING', 'max_wait', fallback=15)

# 전략 설정
TP_RATIO       = config.getfloat('STRATEGY', 'tp_ratio', fallback=1.005)
TP_PART_RATIO  = config.getfloat('STRATEGY', 'tp_part_ratio', fallback=0.5)
SL_RATIO       = config.getfloat('STRATEGY', 'sl_ratio', fallback=0.995)
FEE_RATE       = config.getfloat('STRATEGY', 'fee_rate', fallback=0.0004)

# =========================================================
# 4. 라이선스 설정
# =========================================================
LICENSE_SERVER_URL = config.get('LICENSE', 'server_url', fallback="http://127.0.0.1:8000")
LICENSE_KEY        = config.get('LICENSE', 'license_key', fallback="")

# 5. 안내 메시지
if not EX_API_KEY or "여기에" in EX_API_KEY:
    print("\n⚠️ [주의] 바이낸스 API 키가 설정되지 않았습니다.")
    print("   -> 실매매는 불가능하지만, '라이선스 인증' 테스트는 진행합니다.\n")