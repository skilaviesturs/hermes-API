# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Owner(Base):
    __tablename__ = "owner"

    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=True)
    department = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class Computer(Base):
    __tablename__ = "computer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    dnsname = Column(String, nullable=True, unique=True)
    location = Column(String, nullable=True)
    cpu = Column(String, nullable=True)
    ram = Column(String, nullable=True)
    ipv4 = Column(String, nullable=True, unique=True)
    mac = Column(String, nullable=True, unique=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    owner_id = Column(Integer, ForeignKey("owner.id"), server_default=text('0'))
    owner = relationship("Owner")
    disks = relationship("Disk")
    events = relationship("Events")
    sofware = relationship("Software")
    logs = relationship("Log")


class Disk(Base):
    __tablename__ = "disk"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    free = Column(Integer, nullable=False)
    disk_type = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    id_computer = Column(Integer, ForeignKey("computer.id"), nullable=False)
    computer = relationship("Computer", viewonly=True)


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    event_time = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)

    id_computer = Column(Integer, ForeignKey("computer.id"), nullable=False)
    computer = relationship("Computer", viewonly=True)

class Software(Base):
    __tablename__ = "software"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    id_computer = Column(Integer, nullable=False)
    ident_number = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    id_computer = Column(Integer, ForeignKey("computer.id"), nullable=False)
    computer = relationship("Computer", viewonly=True)

class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    created_at = Column(String, nullable=True)

    id_logflag = Column(Integer, ForeignKey("logflag.id"),
                       server_default=text('0'))
    logflag = relationship("LogFlag")

    id_computer = Column(Integer, ForeignKey("computer.id"), nullable=False)
    computer = relationship("Computer", viewonly=True)

class LogFlag(Base):
    __tablename__ = "logflag"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, server_default=text('False'))
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
