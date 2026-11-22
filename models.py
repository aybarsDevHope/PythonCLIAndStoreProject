import os
from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, create_engine, select, Session
from decimal import Decimal


class envanter(SQLModel, table=True):
    __tablename__ = "envanter"
    id: int | None = Field(default=None, primary_key=True)
    ad: str = Field(max_length=100, nullable=False)
    kategori: str = Field(max_length=50, nullable=False)
    stok: int
    fiyat: Decimal = Field(max_digits=10, decimal_places=2)


load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"], echo=False)

def tablolari_olustur():
    SQLModel.metadata.create_all(engine)
