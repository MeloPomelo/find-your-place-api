import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.models.database import Base

class Coworking(Base):
    __tablename__ = "coworking"

    # uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(200))

