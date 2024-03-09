from pydantic import BaseModel

class Product (BaseModel):
    product_id:int
    name: str
    description: str
    company: str
    price: float
    units: int
    subcategory_id: int
