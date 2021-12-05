from typing import Optional

from pydantic import BaseModel, Field


class BaseProduct(BaseModel):  # for patch
    name: Optional[str] = None
    price: Optional[float] = 0.0
    description: Optional[str] = None


class Product(BaseProduct):  # for get
    id: Optional[str] = Field(alias='_id')


class ProductCreate(BaseProduct):  # for post and put
    name: str
    price: float
