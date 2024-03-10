# -*- coding: utf-8 -*-
"""
Backend for the Limbic interview assignment.

"""


import typing

import fastapi
import fastapi.security
import llm
import pydantic
import dotenv

import key


APIKEY_OPENAI    = key.load('APIKEY_OPENAI_LIMBIC')
model            = llm.get_model('gpt-3.5-turbo')
model.key        = APIKEY_OPENAI
security         = fastapi.security.HTTPBearer()
TYPE_CREDENTIALS = typing.Annotated[
                                fastapi.security.HTTPAuthorizationCredentials,
                                fastapi.Depends(security)]

PROMPT_SYSTEM = """
You are a chatbot tool acting as a good friend,
who is using techniques from person-centred
counseling, supports the user, listens to their
concerns, helps them vent and work through their
issues.

Your name is Limbic.

Try not to mirror or repeat what the user says
exactly. If you need to refer to what they said
before, rephrase and summarize.

Try to keep your messages brief.

In 50% of your responses, end your messages with
insightful, but not distressing, provocative or
probing questions about what the user has said
before.

Help them think deeply about their issue and work
through it themselves.

In the other 50% of your responses, when
appropriate, aim to support and empathize, without
directly endorsing or agreeing with the user's
opinions and don't end your message in a question.

Once you've reached 12 exchanges with the user,
you should gently wind down the conversation.

"""

# -----------------------------------------------------------------------------
app = fastapi.FastAPI(
                title       = 'Limbic Interview Assignment Chat API',
                description = 'Chat API for the Limbic Interview Assignment',
                version     = '1.0.0')


# =============================================================================
class ChatRequest(pydantic.BaseModel):
    """
    Chat Request.

    """

    message: str


# =============================================================================
class ChatResponse(pydantic.BaseModel):
    """
    Chat Response.

    """

    content: str


# -----------------------------------------------------------------------------
@app.post("/chat")
async def chat(credentials: TYPE_CREDENTIALS, request: ChatRequest):
    """
    Secure endpoint for the Limbic interview assignment chat system.

    """

    if credentials.credentials != 'SUPER_SECRET_TOKEN':
        raise fastapi.HTTPException(
                                status_code = fastapi.status.HTTP_403_FORBIDDEN,
                                detail      = 'Invalid or expired token')
    llm_response = model.prompt(request.message, system = PROMPT_SYSTEM)
    return ChatResponse(content = llm_response.text())


# clear; \
# curl -X POST http://localhost:8000/chat \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer SUPER_SECRET_TOKEN" \
# -d '{"message": "Hey, I’ve been feeling really low today."}'

# curl -X POST http://localhost:8000/chat \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer NOT_THE_SUPER_SECRET_TOKEN" \
# -d '{"message": "Hey, I’ve been feeling really low today."}'
