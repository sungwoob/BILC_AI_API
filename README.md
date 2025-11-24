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

## 간단한 클라이언트 사용법
동기식 HTTP 클라이언트(`client.py`)를 사용하면 API 호출을 쉽게 테스트할 수 있습니다.

```python
from client import PromptApiClient


with PromptApiClient("http://localhost:8000") as client:
    print(client.health())          # {'status': 'ok'}
    print(client.generate("hello"))  # {'prompt': 'hello', 'length': 5}
```

### CLI로 직접 호출하기
`client.py`는 기본적으로 헬스체크를 수행하며, `--prompt`를 지정하면 `/generate`를 호출합니다.

```bash
python client.py --base-url http://localhost:8000 --prompt "테스트"
```
