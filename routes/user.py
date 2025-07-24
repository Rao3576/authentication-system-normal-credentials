from fastapi import APIRouter, Depends, HTTPException, status, Request
import schemas.user
from sqlalchemy.orm import Session
import models, schemas,utils
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
import utils.verify_emails



router=APIRouter()


@router.post("/register")
def register(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = utils.user.hash_password(user.password)
    new_user = models.user.User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = utils.user.email_create_token({"sub": user.email})    
    utils.verify_emails.send_verification_email(user.email, token)
    return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={
                         "status_code":status.HTTP_200_OK,
                         "message": "Please check your email to verify your account."})

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    data = utils.user.decode_token(token)
    if not data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.user.User).filter(models.user.User.email == data["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()    
    return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={
                         "status_code":status.HTTP_200_OK,
                         "message": "Email verified successfully!"})

@router.post("/login")
def login(form_data: schemas.user.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.email == form_data.email).first()
    
    if not user or not utils.user.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=401, detail="Email not verified")

    # Convert SQLAlchemy model to Pydantic model using from_attributes
    user_data = schemas.user.UserOut.model_validate(user)  # ✅ from_attributes applies here
    user_dict = user_data.model_dump()                     # ✅ ensure JSON serializable

    access_token, refresh_token = utils.user.create_tokens({"sub": user.email})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status_code": status.HTTP_200_OK,
            "message": "User logged in successfully",
            "data": user_dict,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    )






