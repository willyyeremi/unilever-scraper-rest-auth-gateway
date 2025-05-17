from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


##############################
# common used variable
##############################

base = declarative_base()


##############################
# table on schema: public
##############################

class users(base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key = True)
    username = Column(String)
    password_hash = Column(String)
    password_salt = Column(String)
    roles_id = Column(String)
    is_active = Column(Integer)

class roles(base):
    __tablename__ = "roles"
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key = True)
    roles = Column(String)
    is_active = Column(Integer)