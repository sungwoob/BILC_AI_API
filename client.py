"""FastAPI 서버에 요청을 보내는 간단한 동기식 클라이언트."""
from __future__ import annotations

import argparse
import json
from typing import Optional

import httpx
from pydantic import BaseModel, Field


class PromptResult(BaseModel):
    prompt: str = Field(..., description="API에 전달한 프롬프트")
    length: int = Field(..., description="프롬프트 문자열 길이")


class HealthStatus(BaseModel):
    status: str = Field(..., description="서비스 상태 문자열")


class PromptApiClient:
    """Prompt Echo API용 동기식 HTTP 클라이언트."""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 5.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._client: Optional[httpx.Client] = None

    def _ensure_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(base_url=self._base_url, timeout=self._timeout)
        return self._client

    def generate(self, prompt: str) -> PromptResult:
        """/generate 엔드포인트를 호출해 프롬프트 길이를 반환받습니다."""

        client = self._ensure_client()
        response = client.post("/generate", json={"prompt": prompt})
        response.raise_for_status()
        return PromptResult.model_validate(response.json())

    def health(self) -> HealthStatus:
        """/health 엔드포인트를 호출해 서비스 상태를 확인합니다."""

        client = self._ensure_client()
        response = client.get("/health")
        response.raise_for_status()
        return HealthStatus.model_validate(response.json())

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "PromptApiClient":
        self._ensure_client()
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt API 테스트용 간단한 클라이언트")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="FastAPI 서버 기본 URL (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--prompt",
        help="/generate 엔드포인트에 전달할 프롬프트. 미지정 시 헬스체크만 수행",
    )
    args = parser.parse_args()

    with PromptApiClient(args.base_url) as client:
        if args.prompt is None:
            result = client.health()
        else:
            result = client.generate(args.prompt)

    print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
