from sqlalchemy.orm import Session

from db_object import users


##############################
# table public.users
##############################

def create_users(connection_engine, data):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        new_data = users(
                username = data['username']
                ,password_hash = data['password_hash']
                ,password_salt = data['password_salt']
                ,role = data['role']
        )
        session.add(new_data)
        session.commit()

def read_users(connection_engine, **kwargs):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        result = session.query(users).filter_by(**kwargs).first()
    return result
