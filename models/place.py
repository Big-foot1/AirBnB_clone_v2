#!/usr/bin/python3
"""Place Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from sqlalchemy import String, Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from .review import Review
from .amenity import Amenity
import models
from os import getenv


# an association table for the many to many relationship
# between Place table and Amenity table
place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             nullable=False))


class Place(BaseModel, Base):
    """Holds place attributes and Functions
    Attrs:
        city_id: city id of the place
        user_id: User id of person in the place
        name: the name of the place
        description: Brief decription of the place
        number_rooms: room number
        number_bathrooms: number of bathrooms in the room
        max_guest: maximum guest the room can host
        price_by_night: price charged per night
        latitude: latitude coordinates
        longitude: longitude coordinates
    """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenity_places = relationship("Amenity", secondary=place_amenity,
                                   primaryjoin="Place.id==place_amenity.place_id",
                                   secondaryjoin="place_amenity.amenity_id==Amenity.id",
                                   back_populates="place_amenities")
    amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """Get a list of all Reviews"""
            reviewlist = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    reviewlist.append(review)
            return reviewlist

        @property
        def amenities(self):
            """ Get Linked Amenities"""
            amenitylist = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenitylist.append(amenity)
            return amenitylist

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
