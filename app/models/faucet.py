from datetime import datetime
from enum import auto
from sqlalchemy import Boolean, Column, Integer, String, BigInteger, DateTime, Index

from app.db.base_class import Base
import datetime


class Faucet(Base):
    id = Column(Integer, primary_key=True, index=True)
    network = Column(String(20), nullable=True)
    platform = Column(String(20), nullable=True)
    address = Column(String(128), nullable=True, index=True)
    status = Column(Integer, default=0, nullable=True)
    url = Column(String(128), nullable=True)
    amount = Column(BigInteger, default=0, nullable=True)
    transfered_txn = Column(String(128), nullable=True)
    transfered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    Index('ix_faucet_platform_transfered_at_status', platform, transfered_at, status)