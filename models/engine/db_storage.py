#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base


class DBStorage:
    """ create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        _dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            _query = self.__session.query(cls)
            for element in _query:
                key = "{}.{}".format(type(element).__name__, element.id)
                _dict[key] = element
        else:
            list_a = [State, City, User, Place, Review, Amenity]
            for clas in list_a:
                _query = self.__session.query(clas)
                for element in _query:
                    key = "{}.{}".format(type(element).__name__, element.id)
                    _dict[key] = element
        return (_dict)

    def new(self, obj):
        """add a new element in the table
        """
        self.__session.add(obj)
    def reload(self):
        """configuration
        """
        Base.metadata.create_all(self.__engine)
        _sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(_sec)
        self.__session = Session()

    def close(self):
        """ calls remove()
        """
        self.__session.close()
    
    def save(self):
        """save changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete an element in the table
        """
        if obj:
            self.session.delete(obj)
