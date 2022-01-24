from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session

# more info about error handling in sqlalchemy
# https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy


from ..utils import findid, hashpass
from .. import models, schemas
from ..database import get_db
from .. utils import oauth2


router = APIRouter(
    prefix="/api/v1/user",
    tags=["Admin"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RespondUser)
async def create_user(user: schemas.CreateUser,
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    '''
    CREATE user
    '''
    print(f"create_user: Current user: {current_user.email}")

    if findid.user_id(user.email, db):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "status": "error",
                "message": f"user [{user.email}] already exists."
            }
        )

    # hash the password - user.password
    hashed_password = hashpass.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except sqlalchemy.exc.IntegrityError as error:
        print(f"error:[{error}]")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "status": "error",
                "message": error.orig.args
            }
        )

    return new_user
