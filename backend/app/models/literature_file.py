from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class LiteratureFile(Base):
    __tablename__ = "literature_files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(128), nullable=False)
    file_path = Column(String(256), nullable=False)
    file_type = Column(String(16), nullable=False)
    upload_time = Column(DateTime(timezone=True), server_default=func.now()) 