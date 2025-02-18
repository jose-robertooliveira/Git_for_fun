from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import create_engine, String, Float
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str]


class ItemCreate(BaseModel):
    name: str
    price: float
    description: Optional[str]


class ItemUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    description: Optional[str]


DATABASE_URL = "sqlite:///test.db"


class Base(DeclarativeBase):
    pass


class DBItem(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[float] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]]


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


@app.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    db_item = DBItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return Item(**db_item.__dict__)


@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(**db_item.__dict__)


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)) -> Item:
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return Item(**db_item.__dict__)


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return Item(**db_item.__dict__)

##==============================================================================================================
# from fastapi import FastAPI, HTTPException
# from uuid import uuid4, UUID
# from typing import List
# from models import User, Gender, Role, UserUpdateRequest

# app = FastAPI()

# db: List[User] = [
#     User(
#         id=uuid4(), 
#         first_name="Denerys",
#         last_name="Targerian",
#         gender=Gender.female,
#         roles=[Role.student]
#     ),
#     User(
#         id=uuid4(),  
#         first_name="Ozzy",
#         last_name="Osbourne",
#         gender=Gender.male,
#         roles=[Role.admin, Role.user]
#     )
# ]

# @app.get("/")
# async def root():
#     return {"Hello": "Motherfucker"}

# @app.get("/api/v1/users")
# async def fetch_users():
#     return db

# @app.post("/api/v1/users")
# async def register_user(user: User):
#     user.id = uuid4()  
#     db.append(user)
#     return {"id": user.id}

# @app.delete("/api/v1/users/{user_id}")
# async def delete_user(user_id: UUID):
#     user_index = next((_ for _, user in enumerate(db) if user.id == user_id), None)
#     if user_index is not None:
#         deleted_user = db.pop(user_index)
#         return {"message": f"User {deleted_user.id} deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

# @app.put("/api/v1/users/{user_id}")
# async def update_user(user_update: UserUpdateRequest, user_id: UUID):
#     for user in db:
#         if user.id == user_id:
#             if user_update.first_name is not None:
#                 user.first_name = user_update.first_name
#             if user_update.last_name is not None:
#                 user.last_name = user_update.last_name
#             if user_update.middle_name is not None:
#                 user.middle_name = user_update.middle_name
#             if user_update.roles is not None:
#                 user.roles = user_update.roles
#             return
#     raise HTTPException(
#         status_code=404, 
#         detail=f"user with id: {user_id} does not exist"
#     )
