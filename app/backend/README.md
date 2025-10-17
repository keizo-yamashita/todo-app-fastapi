# Core API

FastAPIベースのバックエンドAPIサービス

## 🛠️ 技術スタック

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (async)
- **Migration**: Alembic
- **Database**: PostgreSQL
- **Language**: Python 3.13
- **Containerization**: Docker & Docker Compose

## 📁 プロジェクト構造

```bash
src/
├── domain/           # ドメインロジック
├── infrastructure/   # インフラストラクチャ層
├── presentation/     # プレゼンテーション層
├── usecase/          # ユースケース層
└── shared/           # 共通モジュール
```

## 🚀 開発環境セットアップ

### 前提条件

- Docker & Docker Compose
- Make（オプション）

### 起動方法

```bash
# コンテナ起動
docker compose up -d

# APIサーバー確認
curl http://localhost:8000/api/users
```

### 開発モードでの起動

```bash
# 開発モードで起動（ホットリロード有効）
docker compose up core-api
```

## 📊 データベース管理

### SQLAlchemy 2.0

このプロジェクトではSQLAlchemy 2.0の非同期機能を使用してデータベース操作を行います。

### 基本的なマイグレーション操作（Alembic）

```bash
# マイグレーション生成（自動）
docker compose exec core-api uv run alembic revision --autogenerate -m "migration message"

# マイグレーション生成（手動）
docker compose exec core-api uv run alembic revision -m "migration message"

# マイグレーション実行
docker compose exec core-api uv run alembic upgrade head

# マイグレーション状態確認
docker compose exec core-api uv run alembic current

# マイグレーション履歴確認
docker compose exec core-api uv run alembic history

# マイグレーションロールバック
docker compose exec core-api uv run alembic downgrade -1
```

## 🧪 テスト

```bash
# テスト実行
docker compose exec core-api pytest

# カバレッジ付きテスト
docker compose exec core-api pytest --cov=src
```

## 🧪 契約テスト（Schemathesis）

### テスト戦略概要

本プロジェクトでは「契約テスト中心アプローチ」を採用し、以下の品質要件を達成します：

- **可用性**: 99.9%以上（年間ダウンタイム8.76時間以内）
- **応答性能**: 3秒以内（95パーセンタイル）
- **欠陥密度**: 0.01件/KLOC以下（重要度「高」の欠陥）
- **セキュリティ**: OWASP ASVS Level 2準拠

### 🎯 最適化されたSchemathesis契約テスト

#### 基本的な実行方法

```bash
# 基本的な契約テスト
task test:contract

# 全ての契約テストを実行
task test:contract:all

# API起動状況確認
task api:check
```

#### テスト種別

```bash
# 性能重視契約テスト（レスポンスタイム3秒以内の検証）
task test:contract:performance

# セキュリティ重視契約テスト（OWASP ASVS Level 2準拠）
task test:contract:security

# カスタムpytestテスト（ビジネスロジック検証）
task test:contract:custom

# 重要エンドポイント集中テスト
task test:contract:critical

# 軽量テスト（開発時用）
task test:contract:quick
```

#### CI/CD統合

```bash
# CI/CD用テスト（品質ゲート付き）
task test:contract:ci

# テスト結果レポート表示
task test:contract:report

# テスト結果アーカイブ
task test:contract:archive
```

### 📊 テスト実行フロー

```mermaid
graph TD
    A[API起動確認] --> B[OpenAPIスキーマ検証]
    B --> C[基本契約テスト]
    C --> D[性能契約テスト]
    D --> E[セキュリティ契約テスト]
    E --> F[カスタムpytestテスト]
    F --> G[統合レポート生成]
    G --> H[品質ゲート評価]
    H --> I{品質ゲート合格?}
    I -->|Yes| J[✅ テスト完了]
    I -->|No| K[❌ テスト失敗]
```

### 🎨 品質ゲート

以下の品質基準をすべてクリアする必要があります：

| 項目 | 基準値 | 説明 |
|------|--------|------|
| **レスポンスタイム** | 3秒以内 | 95パーセンタイル値 |
| **重要エンドポイント** | 2秒以内 | `/healthz`, `/users/{id}` |
| **ペイロードサイズ** | 1MB以下 | レスポンスサイズ制限 |
| **セキュリティ** | 0件 | High重要度の脆弱性 |
| **API仕様準拠** | 100% | OpenAPIスキーマ違反ゼロ |

### 📈 テスト結果レポート

テスト実行後、以下のレポートが生成されます：

```bash
test-results/
├── basic-contract-results.xml          # 基本契約テスト結果（JUnit形式）
├── performance-contract-results.xml    # 性能契約テスト結果
├── security-contract-results.xml       # セキュリティ契約テスト結果
├── custom-contract-results.xml         # カスタムテスト結果
├── custom-contract-report.html         # HTMLレポート
└── contract-test-summary.json          # 統合レポート（JSON）
```

### 🔧 カスタマイズ

#### Schemathesis設定

プロジェクトルートの `schemathesis.yaml` で設定をカスタマイズできます：

```yaml
# 性能要件調整
max_response_time: 3000  # 3秒制限

# テスト実行数調整
hypothesis_max_examples: 100

# 並列実行数
workers: 4
```

#### Hypothesis設定

`tests/contract/test_api_contracts.py` でテスト詳細を調整：

```python
@settings(
    max_examples=100,      # テスト実行数
    deadline=5000,         # タイムアウト（ミリ秒）
    suppress_health_check=[HealthCheck.too_slow]
)
```

### 🎯 重要エンドポイント最適化

重要度の高いエンドポイントには特別な検証を実装：

```python
# 重要エンドポイントリスト
critical_paths = ["/users/{user_id}", "/healthz"]

# より厳しいレスポンスタイム要件
CRITICAL_RESPONSE_TIME_LIMIT_MS = 2000  # 2秒
```

### 🚨 アラート設定

品質指標が基準を下回った場合の対応：

1. **レスポンスタイム超過**: CI/CDでテスト失敗
2. **セキュリティ脆弱性検出**: デプロイ停止
3. **API仕様違反**: 自動ロールバック

### 📚 参考資料

- [Schemathesis公式ドキュメント](https://schemathesis.readthedocs.io/)
- [テスト戦略ドキュメント](../../docs/test_strategy.md)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [Hypothesis公式ドキュメント](https://hypothesis.readthedocs.io/)

## 📝 API仕様

サーバー起動後、以下のURLでAPI仕様を確認できます：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 開発ツール

### リンター・フォーマッター

```bash
# Ruff（リンター）
docker compose exec core-api ruff check src

# Ruff（フォーマッター）
docker compose exec core-api ruff format src
```

### 型チェック

```bash
# ty（型チェッカー）
docker compose exec core-api ty check src
```

## 🚢 デプロイ

### 本番環境用ビルド

```bash
# 本番用イメージビルド
docker build -t core-api:latest .

# イメージ起動
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://user:password@host:5432/db" \
  core-api:latest
```

### ヘルスチェック

```bash
# APIヘルスチェック
curl http://localhost:8000/api/healthz
```

### 環境変数

| 変数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| DATABASE_URL | postgresql+asyncpg://user:password@db:5432/template | データベース接続URL |
| ALLOWED_ORIGIN | http://localhost:3000 | CORS許可オリジン |
| ENVIRONMENT | local | 実行環境（local/dev/prod） |

## 参考資料

### 公式ドキュメント

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/)
- [Alembic公式ドキュメント](https://alembic.sqlalchemy.org/)
- [Docker Compose公式ドキュメント](https://docs.docker.com/compose/)
- [uv公式ドキュメント](https://docs.astral.sh/uv/)

### プロジェクト固有ドキュメント

- `packages/core-api/README.md`: Core APIの詳細説明
- `docs/test_strategy.md`: テスト戦略ドキュメント
