"""
Pydantic модели для эндпоинта профиля пользователя QIWI.
"""

from typing import List, Optional

from pydantic import BaseModel


class MobilePinInfo(BaseModel):
    mobilePinUsed: bool
    lastMobilePinChange: Optional[str] = None
    nextMobilePinChange: Optional[str] = None


class PassInfo(BaseModel):
    passwordUsed: bool
    lastPassChange: Optional[str] = None
    nextPassChange: Optional[str] = None


class PinInfo(BaseModel):
    pinUsed: bool


class AuthInfo(BaseModel):
    personId: int
    registrationDate: str
    boundEmail: Optional[str] = None
    ip: Optional[str] = None
    lastLoginDate: Optional[str] = None
    mobilePinInfo: Optional[MobilePinInfo] = None
    passInfo: Optional[PassInfo] = None
    pinInfo: Optional[PinInfo] = None


class IdentificationInfo(BaseModel):
    bankAlias: str
    identificationLevel: str
    passportExpired: Optional[bool] = None


class ContractInfo(BaseModel):
    blocked: bool
    contractId: int
    creationDate: str
    features: Optional[List] = None
    identificationInfo: Optional[List[IdentificationInfo]] = None


class UserInfo(BaseModel):
    defaultPayCurrency: Optional[int] = None
    defaultPaySource: Optional[int] = None
    email: Optional[str] = None
    firstTxnId: Optional[int] = None
    language: Optional[str] = None
    operator: Optional[str] = None
    phoneHash: Optional[str] = None
    promoEnabled: Optional[str] = None


class ProfileResponse(BaseModel):
    authInfo: Optional[AuthInfo] = None
    contractInfo: Optional[ContractInfo] = None
    userInfo: Optional[UserInfo] = None