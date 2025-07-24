# app/main.py
from fastapi import FastAPI
from database import  engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routes.user import router as router
from routes.oauth import router as oauth_router
#from routes.oauth import google_auth
from starlette.middleware.sessions import SessionMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from config.user import settings  # ✅ Make sure this line is here

# 🔐 Add this middleware BEFORE including routes
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)


# Needed for OAuth login to work
# app.add_middleware(SessionMiddleware, secret_key="9144b7205af02d9f7befd9c8a2916ed7ce2c2a44e84c433fdea814f5f8f05425afa1f362ef1be7774fc12e764aa0d6f7")

# app.include_router(router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(router, prefix="/api/v1/users", tags=["Google OAuth"])


app.include_router(router)
app.include_router(oauth_router)

#app.include_router(google_auth.router)
