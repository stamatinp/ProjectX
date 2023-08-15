from . import db
from flask import session, redirect
from hashlib import sha256

def authenticate(username, password):
    passwordhash = sha256(password.encode()).hexdigest()

    user_doc = db.get_user(username)

    if user_doc is None:
        return (False, {
            'eroare':"Userul nu este inregistrat!",
            'username':username,
            'password':password
        })

    if user_doc["password"] != passwordhash:
        return (False, {
            'eroare':"Parola este gresita!",
            'username':username,
            'password':password
        })

    return (True, user_doc)



def requires_auth(route_func):

    def wrapper(*args, **kwargs):
        username = session.get("username")
        if username:
            kwargs['username'] = username
            return route_func(*args, **kwargs)
        else:
            return redirect("/login")
    
    wrapper.__name__ = route_func.__name__

    return wrapper