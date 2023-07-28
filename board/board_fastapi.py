from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
import pymysql

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_db():
    app.db = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='DB_TEST2',
        autocommit=True
    )
    app.cursor = app.db.cursor()

@app.on_event("shutdown")
async def shutdown_db():
    app.db.close()

@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/board_list")
async def board_list(request: Request):
    app.cursor.execute("SELECT * FROM board")
    data = app.cursor.fetchall()
    return templates.TemplateResponse("board_list.html", {"request": request, "data": data})

@app.post("/board_posting")
async def board_posting(request: Request):
    return templates.TemplateResponse("board_posting.html", {"request": request})

@app.post("/result")
async def result(
    request: Request, id: str = Form(...), title: str = Form(...), content: str = Form(...)
):
    app.cursor.execute(f"INSERT INTO board (id, title, content) VALUES ('{id}', '{title}', '{content}')")

    app.cursor.execute("SELECT * FROM board")
    data = app.cursor.fetchall()
    return templates.TemplateResponse("board_list.html", {"request": request, "data": data})

@app.get("/board_list/{number}")
async def show_post(number: int, request: Request):
    update_query = f"UPDATE board SET views = views + 1 WHERE number = {number}"
    app.cursor.execute(update_query)

    app.cursor.execute(f"SELECT * FROM board WHERE number = '{number}'")
    post = app.cursor.fetchone()

    return templates.TemplateResponse("board_detail.html", {"request": request, "post": post})

@app.get("/board_list/{number}/delete")
async def board_edit(number: int, request: Request):
    app.cursor.execute(f"DELETE FROM board WHERE number={number};")
    return templates.TemplateResponse("board_delete.html", {"request": request})
