# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.faucet import Faucet  # noqa
# from app.models.user import User  # noqa
