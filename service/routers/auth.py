from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from .. import database, models, schemas
from .. utils import hashpass, oauth2


router = APIRouter(
    tags=["Authentication"]
    )


@router.post("/token", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm returns dict: username and password

    user = db.query(models.Users).filter(
        models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials")

    if not hashpass.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials")

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return token
    return {"access_token": access_token, "token_type": "bearer"}
