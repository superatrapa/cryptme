import secrets
from app.cs_crypt import Crypt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

app = FastAPI()

security = HTTPBasic()

users = {}
notes = []


@app.get('/')
def index():
    return "Main Page"


@app.post('/add_user')
def add_user(username, password):
    if username not in users.keys():
        users[username] = Crypt.encode(password, key_string=username)
    return f'username "{username}" was added'


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = False
    correct_password = False

    if credentials.username in users.keys():
        correct_username = True
        correct_password = secrets.compare_digest(Crypt.encode(credentials.password, key_string=credentials.username),
                                                  users[credentials.username])

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.get("/users")
def read_users():
    return users


@app.get("/notes")
def read_notes():
    return notes


@app.post('/notes/add')
def leave_note(note: str, username: str = Depends(get_current_username)):
    notes.append({'user': username, 'note': note})
    return notes[-1]
