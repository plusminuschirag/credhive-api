import traceback
import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from routers.auth import router as auth_router
from routers.credits import router as credit_router
from clients.mongo_client import connect_mongo_db
from clients.rate_limiting_client import limiter

load_dotenv()

connect_mongo_db()

app = FastAPI(debug=True)
app.state.limiter = limiter
app.include_router(auth_router, prefix="/authentication")
app.include_router(credit_router, prefix="/credits")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the full stack trace for debugging purposes
    print(traceback.format_exc())

    # Return a generic error response
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("APP_PORT", 8002)), reload=True)
