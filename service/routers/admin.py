#admin.py
from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. utils import oauth2

# more info about error handling in sqlalchemy
# https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy


from .. import models
from ..database import get_db


router = APIRouter(
    prefix="/api/v1",
    tags=["Admin"]
)


@router.get("/status")
async def db_record_count(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    '''
    # Statistikas metode: atgriež rindu skaitu visās tabulās
    '''
    print(f"[router.get][db_record_count] Current user: {current_user.email}")
    comps = db.query(models.Computer).all()
    owner = db.query(models.Owner).all()
    disks = db.query(models.Disk).all()
    software = db.query(models.Software).all()
    logs = db.query(models.Log).all()
    logflags = db.query(models.LogFlag).all()
    events = db.query(models.Events).all()
    users = db.query(models.Users).all()
    result_tables = {
        'Computers': len(comps),
        'Owners': len(owner),
        'Logs': len(logs),
        'Events': len(events),
        'Disks': len(disks),
        'Software': len(software),
        'Users': len(users),
    }
    result_clasificators = {
        'LogFlags': len(logflags),
    }

    return {
        "status": "success",
        "tables": result_tables,
        "clasificators": result_clasificators,
    }
