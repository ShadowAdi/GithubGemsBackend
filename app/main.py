import uvicorn
from fastapi import FastAPI
from .config import logger
from .middlewares import (
    global_exception_handler,
    http_execution_handler,
    validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .database import engine, Base
from app.utils import add_cors
from app.routes import UserRouter,AuthRouter,RepoRouter,CommentRouter


Base.metadata.create_all(bind=engine)

app = FastAPI()

add_cors(app)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_execution_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/")
def check_health():
    logger.info("Checking If API Is Working")
    return {"success": True, "message": "API Is working"}

app.include_router(UserRouter)
app.include_router(AuthRouter)
app.include_router(RepoRouter)
app.include_router(CommentRouter)






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
