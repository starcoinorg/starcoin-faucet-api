from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.crud.base import CRUDBase
from app.models.faucet import Faucet
from app.schemes.faucet import FaucetCreate, FaucetMaxRetry, FaucetUpdate, FaucetStatus
from app.utils import paginate
from app.db.base_class import Page
from datetime import datetime, timedelta


class CRUDFaucet(CRUDBase[Faucet, FaucetCreate, FaucetUpdate]):
    def get_day_count_by_address(self, db: Session, *, address: str, network: str, since: datetime) -> int:
        q = db.query(self.model)

        since = since.date()
        until = since + timedelta(days=1)

        q = q.filter(
            Faucet.address == address
        )
        q = q.filter(
            Faucet.network == network
        )
        q = q.filter(and_(
            Faucet.transfered_at > since,
            Faucet.transfered_at < until,
        ))
        return q.count()

    def get_create_count_by_address(self, db: Session, *, address: str, network: str, ) -> int:
        q = db.query(self.model)

        since = datetime.utcnow().date()
        until = datetime.utcnow().date() + timedelta(days=1)

        q = q.filter(
            Faucet.address == address
        )
        q = q.filter(
            Faucet.network == network
        )
        q = q.filter(and_(
            Faucet.created_at > since,
            Faucet.created_at < until,
        ))
        return q.count()

    def get_recently_by_network(self, db: Session, *, network: str, page_num: int = 1, page_size: int = 20) -> List[Faucet]:
        q = db.query(self.model)

        q = q.filter(
            Faucet.network == network
        )
        q = q.filter(
            Faucet.status == FaucetStatus.success.value
        )
        q = q.filter(
            Faucet.transfered_at > datetime.utcnow() - timedelta(days=1)
        )
        q = q.order_by(
            Faucet.transfered_at.desc()
        )
        return q.limit(5).all()

    def get_recent_one_by_status(self, db: Session, *, status) -> Faucet:
        q = db.query(self.model)
        q = q.filter(
            Faucet.status == status
        )
        q = q.order_by(
            Faucet.created_at.asc()
        )
        return q.first()

    def get_one_by_transfer_retry(self, db: Session) -> Faucet:
        q = db.query(self.model)
        q = q.filter(
            Faucet.status ==  FaucetStatus.coin_transfer_retry.value
        )
        q = q.filter(
            Faucet.transfer_retry < FaucetMaxRetry.transfer.value
        )
        q = q.order_by(
            Faucet.created_at.desc()
        )
        return q.first()

    def get_one_by_scrape_retry(self, db: Session) -> Faucet:
        q = db.query(self.model)
        q = q.filter(
            Faucet.status ==  FaucetStatus.coin_scrape_retry.value
        )
        q = q.filter(
            Faucet.scrape_retry < FaucetMaxRetry.scrape.value
        )
        q = q.order_by(
            Faucet.created_at.desc()
        )
        return q.first()


faucet = CRUDFaucet(Faucet)
