from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


##############################
# common used variable
##############################

base = declarative_base()


##############################
# table on schema: public
##############################

class ms_roles(base):
    __tablename__ = "ms_roles"
    __table_args__ = {'schema': 'main'}
    id = Column(Integer, primary_key = True)
    roles = Column(String)
    is_active = Column(Integer)

class tr_users(base):
    __tablename__ = "tr_users"
    __table_args__ = {'schema': 'main'}
    id = Column(Integer, primary_key = True)
    username = Column(String)
    password_hash = Column(String)
    password_salt = Column(String)
    roles_id = Column(String)
    is_active = Column(Integer)