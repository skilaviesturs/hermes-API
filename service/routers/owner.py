# owner.py
from fastapi import APIRouter, Depends, status, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from service.utils import findid

# more info about error handling in sqlalchemy
# https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy


from ..utils import oauth2
from .. import models, schemas
from ..database import get_db
from service import database

router = APIRouter(
    prefix="/api/v1/owner",
    tags=["Admin"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_owner(create_owner: schemas.CreateOwner,
                       db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    '''
    CREATE owner
    '''
    create_owner.firstname = create_owner.firstname.lower()
    create_owner.lastname = create_owner.lastname.lower()
    create_owner.created_at = datetime.now()

    print("Create owner param:")
    print(create_owner)

    owner_id = findid.owner_id(create_owner.firstname.lower(),
                                create_owner.lastname.lower(), db)
    print(f"owner_id: [{owner_id}]")

    if owner_id:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "status": "error",
                "message": f"owner [{create_owner.firstname} {create_owner.lastname}] already exists",
            }
        )

    new_owner = models.Owner(**create_owner.dict())

    try:

        db.add(new_owner)
        db.commit()
        db.refresh(new_owner)

    except sqlalchemy.exc.IntegrityError as error:

        print(f"error:[{error}]")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "status": "error",
                "message": error.orig.args
            }
        )

    return {
        "status": "success",
        new_owner.id: new_owner
    }


@router.get("/", response_model=List[schemas.RespondOwner]) #
async def get_owner(db: Session = Depends(database.get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    '''
    GET all owners
    '''
    owners = db.query(models.Owner).all()
    if not owners:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "records not found"
            }
        )

    return owners


@router.put("/", status_code=status.HTTP_201_CREATED)
async def update_owner(update_owner: schemas.UpdateOwner,
                       db: Session = Depends(database.get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    '''
    UPDATE owner
    '''
    print("Update owner param:")
    print(update_owner)
    # atrodam owner unikālo ID
    owner_id = findid.owner_id(update_owner.firstname.lower(),
                                update_owner.lastname.lower(), db)

    print(f"owner_id: [{owner_id}]")
    if not owner_id:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"owner [{update_owner.firstname} {update_owner.lastname}] does not exist"
            }
        )

    updated_owner = {}
    updated_owner["firstname"] = update_owner.new_firstname.lower()
    updated_owner["lastname"] = update_owner.new_lastname.lower()
    if update_owner.department:
        updated_owner["department"] = update_owner.department
    updated_owner["updated_at"] = datetime.now()
    print("Updated owner:")
    print(updated_owner)

    try:

        query = db.query(models.Owner).filter(models.Owner.id == owner_id)
        query.update(updated_owner)
        db.commit()

    except sqlalchemy.exc.IntegrityError as error:

        print(f"error:[{error}]")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": error.orig.args
            }
        )

    return {
        "status": "success",
        owner_id: updated_owner
    }
