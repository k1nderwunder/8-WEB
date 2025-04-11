from fastapi import FastAPI, Request, Response, HTTPException, Cookie
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

users = {
    "user123": "password123",
    "alice": "qwerty"
}

sessions = {}

@app.post("/login")
async def login(data: LoginRequest, response: Response):
    if data.username not in users or users[data.username] != data.password:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    token = f"token_{data.username}"
    sessions[token] = data.username

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=300  # 5 минут
    )
    return {"message": "Вход выполнен"}

@app.get("/user")
async def get_user(session_token: str = Cookie(None)):
    if not session_token or session_token not in sessions:
        raise HTTPException(status_code=401, detail="Требуется вход")
    
    return {
        "username": sessions[session_token],
        "message": f"Привет, {sessions[session_token]}!"
    }