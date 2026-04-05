"""SQLAlchemy data models."""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Entry(Base):
    """Log entry model for MJlog data."""

    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<Entry(id={self.id}, title='{self.title}')>"


class DXCCEntity(Base):
    """DXCC (DX Century Club) entity model from external_data/DXCC.xlsx.

    Represents a ham radio country/entity with prefix, zone, coordinates, etc.
    Data source: http://www.arrl.org/dxcc/

    Uniqueness enforced on (prefix, entity_code, special_use) composite key.
    """

    __tablename__ = "dxcc_entities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prefix = Column(String(20), nullable=False, index=True)
    dxcc_name = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    continent = Column(String(2), nullable=False)
    itu_zone = Column(Integer, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    utc_offset = Column(Integer, nullable=True)
    prefixes = Column(String(50000), nullable=True)
    cq_zone_id = Column(Integer, nullable=True)
    entity_code = Column(Integer, nullable=False)
    special_use = Column(Boolean, default=False, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'prefix', 'entity_code', 'special_use',
            name='uq_dxcc_prefix_code_special'
        ),
    )

    def __repr__(self):
        return (
            f"<DXCCEntity(prefix='{self.prefix}', "
            f"name='{self.name}', continent='{self.continent}')>"
        )
