from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class LiteratureChunk(Base):
    __tablename__ = "literature_chunks"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("literature_files.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    embedding = Column(String(1024), nullable=True)  # mock embedding 