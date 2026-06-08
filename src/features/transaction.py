import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    PURCHASE = "purchase"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    DEPOSIT = "deposit"


class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    amount: float
    transaction_type: TransactionType
    location: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_fraud: bool = False

    class Config:
        use_enum_values = True
