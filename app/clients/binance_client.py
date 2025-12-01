import logging
from binance.client import Client
from app.config import EX_API_KEY, EX_API_SECRET

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 싱글톤으로 Client 인스턴스 관리
_binance_client: Client | None = None

def get_binance_client() -> Client:
    """
    실거래용 Binance Client를 반환합니다.
    config.ini에 설정된 API 키를 사용합니다.
    """
    global _binance_client

    if _binance_client is None:
        # 키가 없거나 기본값("여기에_API_KEY_입력")인 경우 에러 발생
        if not EX_API_KEY or not EX_API_SECRET or EX_API_KEY == "여기에_API_KEY_입력":
            error_msg = "❌ [오류] 바이낸스 API 키가 설정되지 않았습니다. 'config.ini' 파일을 열어 키를 입력해주세요."
            logger.error(error_msg)
            # 고객이 알아보기 쉬운 에러 메시지로 중단
            raise RuntimeError(error_msg)
        
        try:
            # 실제 거래용 Client 생성
            _binance_client = Client(EX_API_KEY, EX_API_SECRET)
            logger.info("Initialized live Binance Client.")
        except Exception as e:
            logger.error(f"바이낸스 클라이언트 생성 실패: {e}")
            raise

    return _binance_client