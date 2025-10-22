from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
import logging
from ...core.config import settings
# from ...core.deps import get_current_user, get_db
from ...services.llm_gateway import ask_llm_stub
from ...db.models import ChatLog
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["chat"])


logger = logging.getLogger(__name__)


# Proxy endpoint: forwards query to an external classifier service
@router.get("/classify")
async def classify_proxy(user_query: str, user_id: int = 1):
	"""Forward the incoming query to the external /classify endpoint and return its JSON response.

	This expects the external service URL in `settings.CLASSIFIER_URL` (e.g.
	http://localhost:8001 or similar). The external endpoint should be mounted at
	{CLASSIFIER_URL}/classify and accept GET with query params `user_query` and `user_id`.
	"""
	# Prefer explicit CLASSIFIER_URL, fall back to legacy LLM_URL, then localhost
	base = getattr(settings, "CLASSIFIER_URL", None) or getattr(settings, "LLM_URL", None) or "http://localhost:8001"
	url = f"{base.rstrip('/')}/classify"
	params = {"user_query": user_query, "user_id": user_id}

	# Allow configurable timeout and a few retries for transient failures
	timeout_seconds = getattr(settings, "CLASSIFIER_TIMEOUT", 30)
	max_retries = 2
	backoff = 0.5
	last_exc = None
	for attempt in range(1, max_retries + 2):
		try:
			async with httpx.AsyncClient(timeout=timeout_seconds) as client:
				resp = await client.get(url, params=params)
			break
		except httpx.ReadTimeout as e:
			last_exc = e
			logger.warning("Read timeout when contacting classifier (attempt %s/%s): %s", attempt, max_retries + 1, e)
			if attempt <= max_retries:
				await httpx.sleep(backoff * attempt)
				continue
			logger.exception("Timeout when contacting classifier service %s", url)
			raise HTTPException(status_code=504, detail=f"Timeout contacting classifier service: {e}")
		except httpx.RequestError as e:
			last_exc = e
			logger.exception("Request error when contacting classifier service %s (attempt %s/%s)", url, attempt, max_retries + 1)
			if attempt <= max_retries:
				await httpx.sleep(backoff * attempt)
				continue
			raise HTTPException(status_code=502, detail=f"Error contacting classifier service: {e}")

	if resp.status_code != 200:
		# bubble up the response body if available and log it
		try:
			detail = resp.json()
		except Exception:
			detail = resp.text
		logger.warning("Classifier returned non-200 (%s): %s", resp.status_code, detail)
		# Use 502 Bad Gateway for upstream failures to keep API semantics consistent
		raise HTTPException(status_code=502, detail={"remote_error": detail, "remote_status": resp.status_code})

	try:
		return resp.json()
	except Exception:
		return {"response_text": resp.text}

# @router.get("/home")
# def home(user=Depends(get_current_user)):
#     return {
#         "welcome": f"Hello {user.username}",
#         "role": user.role,
#         "links": {
#             "instructor_mgmt": "/teachers/me/instructors" if user.role=="teacher" else None,
#             "course_mgmt": "/courses",
#             "assessments": "/assessments"
#         },
#         "llm_endpoint": "/chat/ask"  # plug in your LLM later
#     }

# @router.post("/ask")
# def ask(question: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
#     answer = ask_llm_stub(question, user.user_id)
#     log = ChatLog(user_id=user.user_id, question=question, answer=answer, status="ok", created_at=datetime.utcnow())
#     db.add(log); db.commit()
#     return {"answer": answer}



