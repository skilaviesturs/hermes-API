# find.py
from .. import models, schemas


def output(object):
    if object:
        print(f"findID: found id={object.id}")
        return int(object.id)
    else:
        print(f"findID: not found id")
    return bool(False)


def computer_id(computer_name, db):
    '''
    Atrodam bāzē COMPUTER unikālo id:
    if True,  return [computer.id],
    if False, return [False]
    '''
    # meklējam computer id
    computer = db.query(models.Computer).filter(
        models.Computer.name == computer_name).first()

    return output(computer)


def user_id(user_email, db):
    '''
    Atrodam bāzē USER unikālo id:
    atgriežam [user.id] vai [False]
    user_name: meklējamais vārds
    db: sesijas objects
    '''
    # meklējam user id
    user = db.query(models.Users).filter(
        models.Users.email == user_email).first()

    return output(user)


def owner_id(first_name, last_name, db):
    '''
    Atrodam bāzē OWNER unikālo id:
    if True,  return [owner.id],
    if False, return [False]
    '''
    # meklējam computer id
    owner = db.query(models.Owner).filter(
        models.Owner.firstname == first_name and
        models.Owner.lastname == last_name).first()

    return output(owner)
