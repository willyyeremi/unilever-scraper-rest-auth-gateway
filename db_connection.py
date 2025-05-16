import json

from sqlalchemy import URL


##############################
# common used variable
##############################

driver_dict = {
    "postgresql": "psycopg2"
}


##############################
# main function
##############################

def create_url(ordinal: int, database_product: str):
    driver = driver_dict[database_product]
    with open('./credential.json', 'r') as f:
        data = json.load(f)
    data = data.get(str(ordinal))
    url_object = URL.create(
        f"{database_product}+{driver}"
        ,username = data.get("username")
        ,password = data.get("password")
        ,host = data.get("host")
        ,port = data.get("port")
        ,database = data.get("database_name")
    )
    return url_object