FROM python:3.13-slim AS builder

# セキュリティアップデートを適用
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /bin/uv

WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python -m venv "$VIRTUAL_ENV"

# キャッシュ効率化のために依存関係ファイルのみを先にコピー
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen --no-editable


FROM python:3.13-slim AS runtime

# セキュリティアップデートとヘルスチェック用にcurlインストール
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# セキュリティ向上のため非rootユーザーをUIDを明示的に指定して作成
RUN groupadd -g 1001 appuser && \
    useradd --uid 1001 --gid appuser --create-home --shell /bin/bash appuser

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random

WORKDIR /app

# ファイルをコピーして所有権を一度に設定
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /app/src /app/src
COPY --from=builder --chown=appuser:appuser /app/alembic /app/alembic
COPY --from=builder --chown=appuser:appuser /app/alembic.ini /app/alembic.ini

# 非rootユーザーに切り替え
USER appuser

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

# Azure App Serviceのデフォルトポートを設定
EXPOSE 8000

# 本番環境用の設定でuvicornを起動
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
