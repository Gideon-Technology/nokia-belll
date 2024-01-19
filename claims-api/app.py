from fastapi import FastAPI
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import auth_router, AuthToken

from claims import claims_router
from config import ClaimsApiConfig


api_config = ClaimsApiConfig.get_api_config()

app = FastAPI()

app.include_router(auth_router, prefix=api_config.api_prefix)
app.include_router(claims_router, prefix=api_config.api_prefix)


@app.get("/health")
def health():
    return {"ready": True}


app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=api_config.api_host,
        port=api_config.api_port,
        reload=True,
    )
