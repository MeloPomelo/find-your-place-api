from app.crud.base_crud import CRUDBase
from app.models import Transaction
from app.schemas.transaction_schema import TransactionCreate, TransactionUpdate
from app.crud import user_crud


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    async def create_transaction(
        self,
        *,
        transaction: Transaction,
    ) -> Transaction:
        await user_crud.user.add_bonuses(user_id=transaction.user_id, amount=transaction.amount)
        new_transaction = await self.create(obj_in=transaction)
        return new_transaction


transaction = CRUDTransaction(Transaction)