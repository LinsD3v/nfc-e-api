from fastapi import FastAPI
from routes import create_note, delete_note, get_note

app = FastAPI(title="API Mock de NFC-e")

app.include_router(create_note.router)
app.include_router(delete_note.router)
app.include_router(get_note.router)
