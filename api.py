from fastapi import FastAPI, APIRouter
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from API.routers import root, points, cards, maps, traffics, users, kanban, streets, ML

app = FastAPI()
main_router = APIRouter()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "PATCH", "HEAD"],
    allow_headers=["*"],
    max_age=3600,
)
main_router.include_router(root.router, tags=['root'])
main_router.include_router(users.router, tags=['users'], prefix='/users')
main_router.include_router(points.router, tags=['points'], prefix='/points')
main_router.include_router(cards.router, tags=['cards'], prefix='/cards')
main_router.include_router(streets.router, tags=['streets'], prefix='/streets')
main_router.include_router(maps.router, tags=['maps'], prefix='/maps')
main_router.include_router(traffics.router, tags=['traffics'], prefix='/traffics')
main_router.include_router(kanban.router, tags=['kanban'], prefix='/kanban')
main_router.include_router(ML.router, tags=['ML'], prefix='/ML')

app.include_router(main_router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=8000, reload=True)
