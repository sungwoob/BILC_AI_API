# BILC_AI_API

프롬프트 문자열을 입력받아 간단한 JSON을 반환하는 FastAPI 샘플입니다.

## 실행 방법
1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```

2. 개발 서버 실행
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. API 호출 예시
   ```bash
   curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "안녕하세요"}'
   ```

   응답 예시:
   ```json
   {
     "prompt": "안녕하세요",
     "length": 5
   }
   ```

4. 헬스체크
   ```bash
   curl http://localhost:8000/health
   ```
