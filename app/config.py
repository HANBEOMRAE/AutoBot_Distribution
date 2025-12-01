import os
import configparser
import logging

# 로거 설정
logger = logging.getLogger("config")

# 1. ConfigParser 초기화
config = configparser.ConfigParser()

# 현재 파일(app/config.py)의 위치를 기준으로 상위 폴더(루트)의 config.ini를 찾습니다.
# 구조: Root/config.ini 와 Root/app/config.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

# 파일을 읽습니다.
if not os.path.exists(CONFIG_PATH):
    print(f"⚠️ [경고] 설정 파일을 찾을 수 없습니다: {CONFIG_PATH}")
    print("   -> config.ini 파일을 생성해주세요.")
else:
    config.read(CONFIG_PATH, encoding='utf-8')

# =========================================================
# 변수 매핑 (config.ini -> Python 변수)
# =========================================================

# 1. 바이낸스 키
# 섹션이 없거나 키가 없으면 빈 문자열("")로 처리하여 나중에 에러 유도
EX_API_KEY    = config.get('BINANCE', 'api_key', fallback="")
EX_API_SECRET = config.get('BINANCE', 'secret_key', fallback="")

# 3. 거래 파라미터
# getboolean, getfloat, getint를 사용하여 형변환 자동 처리
DRY_RUN        = config.getboolean('TRADING', 'dry_run', fallback=True) # 기본값 True(안전)
BUY_PCT        = config.getfloat('TRADING', 'buy_pct', fallback=0.98)
TRADE_LEVERAGE = config.getint('TRADING', 'trade_leverage', fallback=5)
POLL_INTERVAL  = config.getfloat('TRADING', 'poll_interval', fallback=1.0)
MAX_WAIT       = config.getint('TRADING', 'max_wait', fallback=15)

# 4. 전략 파라미터
TP_RATIO       = config.getfloat('STRATEGY', 'tp_ratio', fallback=1.005)
TP_PART_RATIO  = config.getfloat('STRATEGY', 'tp_part_ratio', fallback=0.5)
SL_RATIO       = config.getfloat('STRATEGY', 'sl_ratio', fallback=0.995)
FEE_RATE       = config.getfloat('STRATEGY', 'fee_rate', fallback=0.0004)

# =========================================================
# 설정 로드 확인 로그 (보안상 키는 일부만 노출)
# =========================================================
if EX_API_KEY == "여기에_API_KEY_입력" or EX_API_KEY == "":
    print("❌ [오류] config.ini에 API 키가 설정되지 않았습니다.")
else:
    # 키가 정상적으로 로드되었을 때 (보안을 위해 로그는 생략하거나 마스킹 처리)
    pass