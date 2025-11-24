from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Prompt Echo API", version="0.1.0")


class PromptRequest(BaseModel):
    prompt: str = Field(..., description="입력 프롬프트 문자열")


class PromptResponse(BaseModel):
    prompt: str
    length: int


@app.post("/generate", response_model=PromptResponse)
def generate_response(body: PromptRequest) -> PromptResponse:
    """프롬프트 문자열을 받아 간단한 JSON 결과를 반환합니다."""

    content = body.prompt.strip()
    if not content:
        raise HTTPException(status_code=400, detail="prompt must not be empty")

    return PromptResponse(prompt=content, length=len(content))


@app.get("/health")
def health_check() -> dict[str, str]:
    """컨테이너 및 애플리케이션 상태 확인용."""

    return {"status": "ok"}
