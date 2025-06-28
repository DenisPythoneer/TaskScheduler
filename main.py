from fastapi import FastAPI, Request, Depends, HTTPException
import uvicorn

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates # Для работы с HTML шаблонами используйте Jinja2.

from database.main import session_local, engine
from database.models import Base, Tasks
from database.config import TaskCreate, TaskResponse

from sqlalchemy.orm import Session


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") # Подключение статических файлов (CSS, JS, изображения).
templates = Jinja2Templates(directory="templates") # Подключение HTML шаблонов.


Base.metadata.create_all(engine) # Создаем таблицы в базе данных.


def get_db():
    db = session_local() # Создаёт новую сессию БД.

    try:
        yield db # Отдаёт сессию в обработчик запроса.
    finally:
        db.close() # Гарантирует закрытие сессии после завершения.


@app.get("/", tags=['- HTML'])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) # Отрисовываем нашу HTML-страницу.


@app.get('/tasks', tags=['- GET - Получить все Задачи.'])
async def get_tasks(db: Session = Depends(get_db)):
    return db.query(Tasks).all() # Возращаем все данные из таблицы.


@app.post('/tasks', response_model=TaskResponse, tags=['- POST - Добавить новую Задачу.']) # response_model=TaskResponse — определяет модель ответа (формат данных, который вернётся клиенту).
async def create_task(task: TaskCreate, db: Session = Depends(get_db)): # Принимает данные задачи в формате TaskCreate (Pydantic-модель для валидации входящих данных).
    try:
        db_task = Tasks(title=task.title, isComplete=task.is_completed)
        db.add(db_task) # Добавляем данные.
        db.commit() # Сохраняем данные.
        db.refresh(db_task) # Обновляем данные.

        return db_task
    
    except Exception as e:
        db.rollback() # Отменяет изменения, если что-то пошло не так.
        raise HTTPException(status_code=400, detail=str(e))
    

@app.delete('/tasks/{task_id}', tags=['- DELETE - Удалить Задачу.'])
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        db_task = db.query(Tasks).filter(Tasks.id == task_id).first() # Находим задачу по ID.
        
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found") # Вызываем HTTPException если не нашлось.
        
        db.delete(db_task) # Удаляем задачу.
        db.commit()
        
        return {"message": f"Task with id {task_id} has been deleted successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

@app.patch('/tasks/{task_id}', tags=['- PATCH - Изменить статус Задачи.'])
async def pacth_task(task_id: int, db: Session = Depends(get_db)):
    try:
        db_task = db.query(Tasks).filter(Tasks.id == task_id).first() # Тоже также находим нашу задачу по id.
        
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db_task.isComplete = True # Меняем значение с Fasle на True, или-же наоборот.
        
        db.commit() # Сохраняем данные.
        db.refresh(db_task) # Обновляем данные.
        
        return db_task
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)