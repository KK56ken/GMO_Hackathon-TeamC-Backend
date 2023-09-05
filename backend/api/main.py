from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN

from routers import test
from util import util

correct_key: str = util.get_apikey()
api_key_header = APIKeyHeader(name='Authorization', auto_error=False)

async def get_api_key(
    api_key_header: str = Security(api_key_header),
    ):
    if api_key_header == correct_key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

app = FastAPI()
app.include_router(test.router, dependencies=[Depends(get_api_key)], tags=["Test"])

@app.get("/")
def read_root():
    return {"status": "ok"}

