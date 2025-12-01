from fastapi import FastAPI
from app.routers.webhook import router as webhook_router
from app.routers.report import router as report_router, report
import logging

# 로그에 보여줄 설정값들 가져오기
from app.config import DRY_RUN, TRADE_LEVERAGE, BUY_PCT

# 스케줄러 (매일 리포트용)
from apscheduler.schedulers.background import BackgroundScheduler

# FastAPI 앱 초기화
app = FastAPI(title="My Trading Bot", version="2.0.0")

@app.on_event("startup")
def on_startup():
    """
    앱 기동 시:
    1) 설정 상태 로그 출력 (고객 안심용)
    2) 매일 KST 09:00에 일일 리포트 실행 스케줄러 등록
    """
    
    # -----------------------------------------------------
    # [시작 로그] 고객이 config.ini를 잘 고쳤는지 보여줍니다.
    # -----------------------------------------------------
    mode_emoji = "⚠️ TEST MODE (가상 매매)" if DRY_RUN else "🚀 LIVE MODE (실전 매매)"
    
    print(f"\n{'='*50}")
    print(f"       🤖 자동매매 봇 시스템 가동 시작")
    print(f"{'='*50}")
    print(f" [상태] : {mode_emoji}")
    print(f" [설정] : 레버리지 x{TRADE_LEVERAGE} / 잔고사용 {BUY_PCT * 100}%")
    print(f"{'='*50}\n")
    # -----------------------------------------------------

    # 1) 일일 리포트 스케줄러 (한국 시간 09:00)
    try:
        sched = BackgroundScheduler(timezone="Asia/Seoul")
        sched.add_job(lambda: report(), 'cron', hour=9, minute=0)
        sched.start()
        print("✅ [스케줄러] 일일 리포트 타이머 시작 (매일 09:00 KST)")
    except Exception as e:
        print(f"⚠️ [스케줄러] 시작 실패: {e}")

# 라우터 등록
app.include_router(webhook_router)
app.include_router(report_router)

@app.get("/health")
def health():
    """서버 생존 확인용"""
    return {"status": "alive", "mode": "dry_run" if DRY_RUN else "live"}