from typing import Union

def get_user(username) -> Union[dict, None]:
    return db.users.find_one({'username': username})