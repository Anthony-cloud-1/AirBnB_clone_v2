#!/usr/bin/python3
"""The amenity class"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """The class for Amenity
    Attributes:
        name: input name
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary=place_amenity)
