from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from config.user import settings
from database import get_db
from models.user import User
from utils.user import create_token  # your JWT generator

router = APIRouter()
oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = "http://localhost:8000/auth/google/callback"
    url = await oauth.google.authorize_redirect(request, redirect_uri)
    return ({"redirect_url": str(url.headers['location'])})  # Fake preview


@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)

        if not user_info or "email" not in user_info:
            raise HTTPException(status_code=400, detail="Google login failed")

        email = user_info["email"]
        user = db.query(User).filter(User.email == email).first()

        if not user:
            user = User(email=email, is_verified=True, is_active=True)
            db.add(user)
            db.commit()
            db.refresh(user)

        access_token = create_token(data={"id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth error: {str(e)}")




# @router.post("/login")
# def login(form_data: schemas.user.UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == form_data.email).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     token = create_token({"id": user.id})
#     return {"access_token": token, "token_type": "bearer"}