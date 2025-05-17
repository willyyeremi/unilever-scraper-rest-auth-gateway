from sqlalchemy import update, create_engine
from sqlalchemy.orm import Session

from db_object import users, roles
from db_connection import create_url


##############################
# table public.users
##############################

def read_roles(connection_engine, **kwargs):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        result = session.query(roles).filter_by(**kwargs).first()
    return result


##############################
# table public.users
##############################

def create_users(connection_engine, data):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        new_data = users(
                username = data['username']
                ,password_hash = data['password_hash']
                ,password_salt = data['password_salt']
                ,roles_id = data['roles_id']
                ,is_active = 1
        )
        session.add(new_data)
        session.commit()

def read_users(connection_engine, **kwargs):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        result = session.query(users).filter_by(**kwargs).first()
    return result

def update_users(connection_engine, written_username, **kwargs):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        stmt = update(users).where(users.username == written_username).values(**kwargs)
        session.execute(stmt)
        session.commit()


if __name__ == "__main__":
    url = create_url(ordinal = 1, database_product = "postgresql")
    engine = create_engine(url)
    new_data = {
        "username": "admin_update",
        "is_active": "0"
    }
    update_users(engine, "admin", **new_data)