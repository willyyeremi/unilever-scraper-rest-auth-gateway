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
    role = Column(String)