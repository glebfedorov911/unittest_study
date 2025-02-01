from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, Result
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

import logging
import sys
from typing import Callable
from functools import wraps


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler('lesson1/lesson1.log', encoding="utf-8", mode='a'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

INTERNAL_SERVER_ERROR = "Internal Server Error"
USER_NOT_FOUND = "User not found"

class NotFoundException(Exception):
    ...

class CustomHTTPException(Exception):
    def __init__(self, message, *, code = None) -> None:
        super().__init__(message)
        self.code = code

async def async_session():
    ...

class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

class User(Base):
    name: Mapped[str] = mapped_column(nullable=False)

class UserRead(BaseModel):
    name: str

def log_and_handle_errors(func: Callable) -> Callable:
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            exc_type, exc_value, _ = sys.exc_info()

            if exc_type:
                logger.error(f"Перехвачено исключение внутри {func.__name__}: {exc_value}")

            logger.exception(f"Ошибка в {func.__name__}: {e}")
            raise e
    
    return wrapper

class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @log_and_handle_errors
    async def get_user_by_id(self, user_id: int) -> UserRead:
        try:
            return await self.__get_user_by_id(user_id=user_id)
        except NotFoundException as e:
            raise CustomHTTPException(e, code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise CustomHTTPException(INTERNAL_SERVER_ERROR, code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def __get_user_by_id(self, user_id: int) -> UserRead:
        stmt = select(User).where(User.id == user_id)
        result: Result = await self.session.execute(stmt)
        if not (user := result.fetchone()):
            raise NotFoundException(USER_NOT_FOUND)
        return user

def get_user_repository(session: AsyncSession = Depends(async_session)) -> UserRepository:
    return UserRepository(session=session)

@app.get("/users/{user_id}")
async def get_user(user_id: int, user_repository: UserRepository = Depends(get_user_repository)) -> UserRead:
    try:
        return await user_repository.get_user_by_id(user_id=user_id)
    except CustomHTTPException as e:
        raise HTTPException(
            detail=str(e),
            status_code=e.code
        )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8001)