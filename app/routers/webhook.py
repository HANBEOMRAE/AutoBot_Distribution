from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import logging

from app.services.switching import switch_position
# config.ini에서 설정값 가져오기 (테스트모드 여부, 비밀번호)
from app.config import DRY_RUN

router = APIRouter()
logger = logging.getLogger("webhook")

# Pydantic 모델 (요청 메시지 검증)
class AlertPayload(BaseModel):
    symbol: str
    action: str
    strategy: str = None # [추가] 전략 이름 (통계용)

@router.post("/webhook")
async def webhook(payload: AlertPayload):
    
    # 2. 로그 출력
    sym = payload.symbol.upper().replace("/", "")
    action = payload.action.upper()
    
    # 전략 이름이 있으면 로그에 같이 표시
    strategy_log = f"| 전략: {payload.strategy}" if payload.strategy else ""
    logger.info(f"📩 [신호수신] {sym} | {action} {strategy_log}")

    # 3. 테스트 모드 확인
    if DRY_RUN:
        logger.info(f"⚠️ [TEST MODE] 매매를 건너뜁니다. ({action})")
        return {"status": "dry_run", "message": "Test mode enabled"}

    # 4. 매매 실행 (기존 로직 연결)
    try:
        res = switch_position(
            symbol=sym,
            action=action,
            # 필요한 경우 여기서 레버리지 등을 추가로 넘길 수 있음
        )
        return res
    except Exception as e:
        logger.error(f"매매 실행 중 오류: {e}")
        return {"status": "error", "message": str(e)}