import sentry_sdk
from config import ENVIRONMENT, SENTRY_DSN
from logs.logs_setting import logging
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


def init_sentry():
    # ログレベルをINFOに設定（INFO以上のメッセージがキャプチャされる）  # Sentryに送信するイベントのレベルをERRORに設定
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
    # SentryのDSNを設定
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT if ENVIRONMENT else "dev",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            sentry_logging,
            AsyncioIntegration(),
        ],
    )
