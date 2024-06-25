import datetime
from pydantic import BaseModel

class ProductSchema(BaseModel):
    title : str
    descreption : str
    created_at : datetime.datetime
    updated_at : datetime.datetime | None = None
    
ProductListSchema = list[ProductSchema]
    