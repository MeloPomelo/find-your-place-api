from uuid import UUID
from datetime import datetime

from app.models.transaction_model import TransactionBase


class TransactionCreate(TransactionBase):
    user_id: UUID


class TransactionUpdate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    pass
