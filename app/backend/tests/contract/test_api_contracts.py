"""APIコントラクトテスト。

OpenAPIスキーマに基づくAPIコントラクトの検証を行う。
"""

import pytest
import schemathesis
from hypothesis import HealthCheck, settings
from schemathesis import Case

# OpenAPI 3.1.0 実験的サポートを有効化
schemathesis.experimental.OPEN_API_3_1.enable()

# テスト対象スキーマ
schema = schemathesis.from_uri("http://localhost:8000/openapi.json")


@settings(
    deadline=10000,
    suppress_health_check=[HealthCheck.too_slow],
)
@schema.parametrize()
def test_api_contract_compliance(case: Case) -> None:
    try:
        response = case.call()
        case.validate_response(response)
    except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
        pytest.fail(f"Contract test failed for {case.method} {case.path}: {e}")


if __name__ == "__main__":
    # 直接実行時の設定
    pytest.main([__file__, "-v", "--tb=short"])
