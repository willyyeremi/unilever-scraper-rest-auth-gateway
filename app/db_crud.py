from sqlalchemy import update, create_engine
from sqlalchemy.orm import Session

from db_object import tr_users, ms_roles
from db_connection import create_url


##############################
# table public.users
##############################

def read_ms_roles(connection_engine, **kwargs):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        result = session.query(ms_roles).filter_by(**kwargs).first()
    return result


##############################
# table public.users
##############################

def create_tr_users(connection_engine, data):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        new_data = tr_users(
                username = data['username']
                ,password_hash = data['password_hash']
                ,password_salt = data['password_salt']
                ,roles_id = data['roles_id']
                ,is_active = 1
        )
        session.add(new_data)
        session.commit()

def read_tr_users(connection_engine, **kwargs):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        result = session.query(tr_users).filter_by(**kwargs).first()
    return result

def update_tr_users(connection_engine, written_username, **kwargs):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        stmt = update(tr_users).where(tr_users.username == written_username).values(**kwargs)
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