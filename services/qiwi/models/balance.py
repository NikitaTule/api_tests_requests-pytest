from typing import List, Optional
from pydantic import BaseModel


class Currency(BaseModel):
    code: int
    name: str


class Balance(BaseModel):
    amount: float
    currency: int


class Account(BaseModel):
    alias: str
    fsAlias: str
    bankAlias: str
    title: str
    type: Optional[dict] = None
    hasBalance: bool
    balance: Optional[Balance] = None
    currency: int
    defaultAccount: bool


class BalanceResponse(BaseModel):
    accounts: List[Account]
