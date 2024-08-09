from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet


KEY = b'your-encryption-key'
cipher = Fernet(KEY)

# Database setup
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    content = Column(Text)

class UserHistory(Base):
    __tablename__ = 'user_history'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    query = Column(Text)
    response = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)
