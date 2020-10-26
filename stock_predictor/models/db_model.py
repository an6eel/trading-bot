from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class DBModelMixin(DateTimeModelMixin):
    id: Optional[str] = None