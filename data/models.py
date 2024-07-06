import datetime
from datetime import datetime
from typing import List, Optional

from pydantic import field_validator, BaseModel, Field


class CourierLoginModel(BaseModel):
    login: str = Field(..., min_length=2, max_length=10, pattern="^[a-zA-Z]+$")
    password: str = Field(..., min_length=4, max_length=4, pattern="^[0-9]+$")


class CourierCreateModel(BaseModel):
    login: str = Field(..., min_length=2, max_length=10, pattern="^[a-zA-Z]+$")
    password: str = Field(..., min_length=4, max_length=4, pattern="^[0-9]+$")
    firstName: Optional[str] = Field(None, min_length=2, max_length=10, pattern="^[a-zA-Zа-яА-ЯёЁ]+$")

    @field_validator('login', 'password')
    def non_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('Field cannot be empty')
        return value


class CourierModel(BaseModel):
    id: int


class CourierDeleteModel(BaseModel):
    id: int


class CourierOrdersCountModel(BaseModel):
    id: str
    ordersCount: str


class OrderFinishModel(BaseModel):
    id: int


class OrderCancelModel(BaseModel):
    track: int


class OrderCreateModel(BaseModel):
    firstName: str = Field(..., min_length=2, max_length=15, pattern="^[а-яА-ЯёЁ\\s-]+$")
    lastName: str = Field(..., min_length=2, max_length=15, pattern="^[а-яА-ЯёЁ]+$")
    address: str = Field(..., min_length=5, max_length=50, pattern="^[а-яА-ЯёЁ0-9\\s,.-]+$")
    metroStation: int
    phone: str = Field(..., min_length=10, max_length=12, pattern="^\\+?[0-9]+$")
    rentTime: int = Field(..., ge=1, le=7)
    deliveryDate: str
    comment: Optional[str] = Field(None, max_length=24, pattern="^[а-яА-ЯёЁ0-9\\s,.-]*$")
    color: Optional[List[str]] = None

    @field_validator('deliveryDate')
    def check_delivery_date(cls, value):
        parsed_date = datetime.fromisoformat(value.replace('Z', ''))
        if parsed_date.date() <= datetime.datetime.now(datetime.UTC).date():
            raise ValueError('Дата доставки должна быть позже сегодняшнего дня')
        return value


class OrderTrackModel(BaseModel):
    t: int


class OrderAcceptModel(BaseModel):
    id: int
    courierId: int


class OrderInfoModel(BaseModel):
    id: int
    courierId: Optional[int] = None
    firstName: str
    lastName: str
    address: str
    metroStation: str
    phone: str
    rentTime: int
    deliveryDate: str
    track: int
    color: List[str]
    comment: Optional[str] = None
    createdAt: str
    updatedAt: str
    status: int


class MetroSearchModel(BaseModel):
    s: str
