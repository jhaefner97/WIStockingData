from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WIStockingData(Base):
    __tablename__ = "WIStockingData"
    __table_args__ = {"schema": "StockingData"}  # Specifies the schema

    Index = Column(Integer, primary_key=True, autoincrement=True)
    StockingYear = Column(Integer, nullable=True)
    Source = Column(String(128), nullable=True)
    StockedWaterbodyName = Column(String(128), nullable=True)
    LocalWaterbodyName = Column(String(128), nullable=True)
    Species = Column(String(128), nullable=True)
    StrainStock = Column(String(128), nullable=True)
    AgeClass = Column(String(128), nullable=True)
    NumberFishStocked = Column(Integer, nullable=True)
    AvgFishLengthIN = Column(Integer, nullable=True)
    County=Column(String(100), nullable=True)

    def __repr__(self):
        return (
            f"<WIStockingData(Index={self.Index}, "
            f"StockingYear={self.StockingYear}, Source={self.Source}, "
            f"StockedWaterbodyName={self.StockedWaterbodyName}, "
            f"Local_Waterbody_Name={self.LocalWaterbodyName}, "
            f"Species={self.Species}, StrainStock={self.StrainStock}, "
            f"AgeClass={self.AgeClass}, NumberFishStocked={self.NumberFishStocked}, "
            f"AvgFishLengthIN={self.AvgFishLengthIN})>"
        )