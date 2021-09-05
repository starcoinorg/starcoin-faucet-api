from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.crud.base import CRUDBase
from app.models.faucet import Faucet
from app.schemes.faucet import FaucetCreate, FaucetUpdate, FaucetStatus
from app.utils import paginate
from app.db.base_class import Page
from datetime import datetime, timedelta


class CRUDFaucet(CRUDBase[Faucet, FaucetCreate,FaucetUpdate]):
     def get_day_count_by_address(self, db: Session, *, address: str, platform: str, since: datetime) -> int:
        q = db.query(self.model)

        since = since.date()
        until = since + timedelta(days=1)

        q = q.filter(
            Faucet.address == address
        )
        q = q.filter(
            Faucet.platform == platform
        ) 
        q = q.filter(and_(
            Faucet.transfered_at > since,
            Faucet.transfered_at < until,
        ))
        return q.count()
    
     def get_day_count_by_user(self, db: Session, *, url: str, platform: str, network: str) -> int:
        q = db.query(self.model)

        since = datetime.now().date()
        until = datetime.now().date() + timedelta(days=1)

        q = q.filter(
            Faucet.url == url
        )
        q = q.filter(
            Faucet.platform == platform
        ) 
        # q = q.filter(
        #     Faucet.network == network
        # ) 
        q = q.filter(and_(
            Faucet.created_at > since,
            Faucet.created_at < until,
        ))
        return q.count()

     def get_recently_by_platform(self, db: Session, *, platform: str, page_num: int = 1, page_size: int = 20) -> List[Faucet]:
        q = db.query(self.model)

        q = q.filter(
            Faucet.platform == platform
        )
        q= q.filter(
            Faucet.status == FaucetStatus.success.value
        )
        q = q.filter(
            Faucet.transfered_at > datetime.now() - timedelta(days=1)
        )
        q = q.order_by(
            Faucet.transfered_at.desc()
        )
        
        return q.limit(5).all()
        #return paginate(query=q, page_num=page_num, page_size=page_size)

faucet = CRUDFaucet(Faucet)