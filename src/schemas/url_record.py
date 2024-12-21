from typing import Optional
from datetime import datetime

from pydantic import BaseModel

# Shared properties
class UrlRecordBase(BaseModel):
    url_full: str
    type: Optional[str]

# Properties to receive on UrlRecord creation
class UrlRecordCreate(UrlRecordBase):
    pass

# Properties to receive on UrlRecord update
class UrlRecordUpdate(BaseModel):
    type: str

# Properties shared by models stored in DB
class UrlRecordInDBBase(BaseModel):

    id: int
    url_full: str
    url_short: str
    created_at: datetime
    created_by: str
    type: str
    usage_counter: int
    status: str

# Properties to return to client
class UrlRecord(UrlRecordInDBBase):
    pass

# Properties stored in DB
class UrlRecordInDB(UrlRecordInDBBase):
    pass 