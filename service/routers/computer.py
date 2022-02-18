# computer.py
from fastapi import APIRouter, Depends, status, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# more info about error handling in sqlalchemy
# https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy


from ..utils import findid, oauth2
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/computer",
    tags=["Computer"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_computer(create_computer: schemas.CreateComputer,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    '''
    # Izveidojam datoru
    '''
    # datorvārdu pārmainām uz lower case
    _computername = create_computer.name.lower()
    create_computer.name = _computername

    find_computer = db.query(models.Computer).filter(
        models.Computer.name == create_computer.name).first()

    if find_computer:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "status": "error",
                "message": f"computer [{create_computer.name}] already exists."
            }
        )

    new_computer = models.Computer(**create_computer.dict())
    new_computer.created_at = datetime.now()
    if create_computer.dnsname:
        new_computer.dnsname = create_computer.dnsname.lower()

    try:

        db.add(new_computer)
        db.commit()
        db.refresh(new_computer)
        print(f"[POST] computer [{new_computer.name}] created")

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
        create_computer.name: new_computer
    }


@router.get("/", response_model=List[schemas.RespondComputer])
async def get_computer(db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    '''
    # Atgriežam informāciju par visiem datoriem 
    '''
    computers = db.query(models.Computer).join(models.Owner, models.Computer.owner_id==models.Owner.id).all()

    if not computers:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "records not found"
            }
        )

    return computers


@router.put("/", status_code=status.HTTP_201_CREATED)
async def update_computer(update_computer: schemas.UpdateComputer,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    '''
    # Aktualizējam tikai datoru vērtības, kuras ir aizpildītas
    '''
    # datorvārdu pārmainām uz lower case
    _computername = update_computer.name.lower()
    update_computer.name = _computername
    # meklējam datora unikālo ID
    computer_id = findid.computer_id(update_computer.name, db)
    computer_query = db.query(models.Computer).filter(
        models.Computer.id == computer_id)

    # pārbaudam vai atgrieztas ir vērtības
    _computer = computer_query.first()

    if _computer == None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"computer [{update_computer.name}] does not exist"
            }
        )

    # nokopējam bibliotēku
    modified_dict = update_computer.dict()
    # print("[PUT] dict content is:")
    modified_dict['updated_at'] = datetime.now()

    # dnsname pārmainām uz lower case
    if update_computer.dnsname:
        modified_dict['dnsname'] = update_computer.dnsname.lower()
    # atstājam tikai atslēgas ar vērtībām, kas nav 0 un NULL
    modified_dict = {k: v for k, v in modified_dict.items() if v}

    try:

        computer_query.update(modified_dict)
        db.commit()
        print(f"[PUT] computer [{modified_dict['name']}] properties updated")

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
        update_computer.name: computer_query.first()
    }


@router.get("/iscomputer/{computername}")
async def check_is_computer(computername,
                     db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    '''
    # Atgriež true, ja datora vārds eksistē datu bāzē, savādāk atgriež false
    '''
    _computername = computername.lower()
    result = findid.computer_id(_computername, db)

    if result:
        return { "status": True }
    else:
        return { "status": False }
    