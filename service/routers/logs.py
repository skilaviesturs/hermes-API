from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

# more info about error handling in sqlalchemy
# https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy


from ..utils import findid, oauth2
from .. import models, schemas
from ..database import get_db, execute_sql


router = APIRouter(
    prefix="/api/v1/logs",
    tags=["Logs"]
)


@router.get("/")  # 
async def get_all_logs(db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):  # , response_model=schemas.ReturnLog
    '''
    # Izgūstam visus žurnalēšanas notikumus
    # TODO: jāizdomā kā samapot vienā skatā rezultātus arī no sastītajām tabulām - Computer, LogFlag
    '''
    # logs = db.query(models.Log).all()

    sql_string = r'''
        select distinct c.name as computer, l.created_at as timestamp, f.name as status , l.message
        from log as l
        inner join computer as c on c.id = l.id_computer 
        inner join logflag as f on f.id = l.id_logflag 
    '''

    result = execute_sql(sql_string)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "records not found"
            }
        )

    # Formējam output { 'computername': [[notikums],[notikums],[notikums]] }
    output = {}
    for line in result:
        a, *b = line
        if a not in output:
            output[a] = [b]
        else:
            output[a].append(b)
    # print(output)

    return output


@router.post("/{computername}", status_code=status.HTTP_201_CREATED) #, response_model=List[schemas.RespondLog]
async def create_log(computername, log: schemas.CreateLog,
                     db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    '''
    # Ieraksta žurnalēšanas notikumu db esošam datoram
    '''
    computer_id = findid.computer_id(computername, db)
    if computer_id:
        log.id_computer = int(computer_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"computer {computername} not found"
            }
        )

    # print(log.dict())
    #new_log_post = models.Log(idcomputer=log.idcomputer, idlogflag=log.idlogflag, message=log.message)
    # print(log.dict())
    log.created_at = datetime.now()
    new_log_post = models.Log(**log.dict())
    db.add(new_log_post)
    db.commit()
    db.refresh(new_log_post)

    return { 'message': 'sucess' }


@router.get("/{computername}")  # , response_model=List[schemas.RespondLog
async def get_computer_logs(computername, db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    '''
    # Izgūstam visus datora žurnalēšanas notikumus
    '''
    # atrodam datora unikālo ID
    computer_id = findid.computer_id(computername, db)
    print(f"router: [{computername}] found id:{computer_id}")

    if not computer_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"Computer [{computername}] not found"
            }
        )

    # atgriežam visus LOG ierakstus pēc datora ID
    # logs = db.query(models.Log, models.LogFlag).join(
    #     models.LogFlag, models.Log.id_logflag == models.LogFlag.id).filter(
    #     models.Log.id_computer == computer_id).all()

    sql_string = r'''
        select distinct c.name as computer, l.created_at as timestamp, f.name as status , l.message
	        from log as l
	        inner join computer as c on c.id = l.id_computer 
	        inner join logflag as f on f.id = l.id_logflag
            where c.id = ?
    '''
    result = execute_sql(sql_string, computer_id)

    

    print(f"router: [{computername}] found {len(result)} records")
    # print(result)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": f"records not found"
            }
        )

    # Formējam output { 'computername': [[notikums],[notikums],[notikums]] }
    output = {}
    for line in result:
        a, *b = line
        if a not in output:
            output[a] = [b]
        else:
            output[a].append(b)
    # print(output)

    return output
