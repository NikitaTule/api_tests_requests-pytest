"""
Pydantic модели для платёжных эндпоинтов QIWI.
"""

from typing import List, Optional
from pydantic import BaseModel


# --- История платежей ---

class Total(BaseModel):
    amount: float
    currency: int


class PaymentTransaction(BaseModel):
    txnId: int
    personId: int
    date: str
    errorCode: int
    error: Optional[str] = None
    status: str
    type: str
    statusText: str
    trmTxnId: str
    account: str
    sum: Total
    commission: Total
    total: Total
    provider: Optional[dict] = None
    comment: Optional[str] = None
    currencyRate: Optional[float] = None


class PaymentHistoryResponse(BaseModel):
    data: List[PaymentTransaction]
    nextTxnId: Optional[int] = None
    nextTxnDate: Optional[str] = None


# --- Создание платежа ---

class PaymentState(BaseModel):
    code: str


class PaymentTransaction(BaseModel):
    id: int
    state: PaymentState


class CreatePaymentResponse(BaseModel):
    id: str
    terms: str
    fields: dict
    sum: Total
    source: str
    transaction: PaymentTransaction
    comment: Optional[str] = None


# --- Статус транзакции ---

class TransactionResponse(BaseModel):
    txnId: int
    personId: int
    date: str
    errorCode: int
    error: Optional[str] = None
    status: str
    type: str
    statusText: str
    trmTxnId: str
    account: str
    sum: Total
    commission: Total
    total: Total
    comment: Optional[str] = None
    currencyRate: Optional[float] = None