import sys
from sqlalchemy import Column, ForeignKey, Integer, String
# declarative base for database configuration
from sqlalchemy.ext.declarative import declarative_base
# relationship for declaring foreign key entries
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    username = Column(String(25), nullable=False)
    password = Column(String(25), nullable=False)
    id = Column(Integer, primary_key=True)


class Restaurant(Base):
    __tablename__ = 'restaurant'
    # entries of restaurant table
    name = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        # Return menu items as JSON
        return {
            'name': self.name,
            'id': self.id,
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'
    # entries of menu_item table
    name = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(20))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant, backref=backref("items", cascade="all, delete-orphan"))

    @property
    def serialize(self):
        # Return menu items as JSON
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'course': self.course,
        }


# sqllite 3 as the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
