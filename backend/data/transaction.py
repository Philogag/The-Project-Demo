from datetime import datetime

from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    handler_category: str
    handler_id: str
    handled_at: datetime
