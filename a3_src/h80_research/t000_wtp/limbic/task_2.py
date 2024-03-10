# -*- coding: utf-8 -*-
"""
Backend for the Limbic interview assignment.

Testing:-

clear; \
curl -X POST http://localhost:8000/insert_prompt \
-H "Content-Type: application/json" \
-H "Authorization: Bearer SUPER_SECRET_TOKEN" \
-d '{"prompt": "Repeat in all caps: %s", "weight": 1}'

clear; \
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-H "Authorization: Bearer SUPER_SECRET_TOKEN" \
-d '{"message": "Hey, I’ve been feeling really low today."}'

curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-H "Authorization: Bearer NOT_THE_SUPER_SECRET_TOKEN" \
-d '{"message": "Hey, I’ve been feeling really low today."}'


"""


import os.path
import sqlite3
import textwrap
import typing
import random

import fastapi
import fastapi.security
import llm
import pydantic
import dotenv

import key


# FastAPI
#
security         = fastapi.security.HTTPBearer()
TYPE_CREDENTIALS = typing.Annotated[
                                fastapi.security.HTTPAuthorizationCredentials,
                                fastapi.Depends(security)]
app = fastapi.FastAPI(
                title       = 'Limbic Interview Assignment Chat API',
                description = 'Chat API for the Limbic Interview Assignment',
                version     = '1.0.0')
APIKEY_LIMBIC = 'SUPER_SECRET_TOKEN'

# Language model.
#
APIKEY_OPENAI = key.load('APIKEY_OPENAI_LIMBIC')
model         = llm.get_model('gpt-3.5-turbo')
model.key     = APIKEY_OPENAI

# Database
#
UID_PROMPT_DEFAULT = 'UID_PROMPT_DEFAULT'


# =============================================================================
class DatabaseContext():
    """
    Context manager for the prompt database.

    """

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Return a constructed DatabaseContext object.

        """

        dirpath_self = os.path.dirname(os.path.realpath(__file__))
        filename_db  = 'prompt.db'
        filepath_db  = os.path.join(dirpath_self, filename_db)
        self.dbconn  = sqlite3.connect(filepath_db)

        assert self.dbconn is not None

        cursor = self.dbconn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt (
                uid      text,
                version  int,
                weight   float,
                template text,
                PRIMARY KEY (uid, version));
            """)

    # -------------------------------------------------------------------------
    def __enter__(self):
        """
        Enter the DatabaseContext context.

        """

        return self

    # -------------------------------------------------------------------------
    def __exit__(self, type, value, traceback):
        """
        Exit the DatabaseContext context.

        """

        self.dbconn.close()

    # -------------------------------------------------------------------------
    def pick(self, uid):
        """
        Return a list of variants.

        """

        cursor = self.dbconn.cursor()
        cursor.execute("""
            SELECT * FROM prompt WHERE uid=?
            """,
            (uid,))
        tup_row = tuple(cursor.fetchall())

        list_choice = random.choices(
                        population = tup_row,
                        weights    = (weight for (_,_,weight,_) in tup_row))

        (uid,version,weight,template) = list_choice[0]

        return (uid,version,weight,template)


    # -------------------------------------------------------------------------
    def insert(self, weight, template):
        """
        Insert a new prompt into the prompt table.

        """

        uid = UID_PROMPT_DEFAULT

        cursor = self.dbconn.cursor()
        cursor.execute("""
            SELECT * FROM prompt WHERE uid=?
            """,
            (uid,))

        set_version = {0}
        for (_,version,_,_) in cursor.fetchall():
            set_version.add(version)
        version = max(set_version) + 1

        cursor.execute("""
            INSERT INTO prompt(uid,version,weight,template)
            VALUES(?,?,?,?)
            """,
            (uid, version, weight, template))
        self.dbconn.commit()


# =============================================================================
class Prompt(pydantic.BaseModel):
    """
    Prompt information

    """

    prompt: str
    weight: int


# =============================================================================
class PromptStatus(pydantic.BaseModel):
    """
    Prompt status information

    """

    status: str


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

    content:       str
    prompt_verson: int
    prompt_weight: float


# -----------------------------------------------------------------------------
@app.post("/insert_prompt")
async def insert_prompt(credentials: TYPE_CREDENTIALS, prompt: Prompt):
    """
    Secure endpoint for the Limbic interview assignment chat system.

    """

    if credentials.credentials != APIKEY_LIMBIC:
        raise fastapi.HTTPException(
                            status_code = fastapi.status.HTTP_403_FORBIDDEN,
                            detail      = 'Invalid or expired token')

    with DatabaseContext() as db:
        db.insert(weight   = prompt.weight,
                  template = prompt.prompt)
        return PromptStatus(status = 'ok')


# -----------------------------------------------------------------------------
@app.post("/chat")
async def chat(credentials: TYPE_CREDENTIALS, request: ChatRequest):
    """
    Secure endpoint for the Limbic interview assignment chat system.

    """

    if credentials.credentials != APIKEY_LIMBIC:
        raise fastapi.HTTPException(
                            status_code = fastapi.status.HTTP_403_FORBIDDEN,
                            detail      = 'Invalid or expired token')

    with DatabaseContext() as db:
        (uid,version,weight,template) = db.pick(UID_PROMPT_DEFAULT)
        response = model.prompt(template.format(request.message))
        return ChatResponse(content       = response.text(),
                            prompt_verson = version,
                            prompt_weight = weight)
