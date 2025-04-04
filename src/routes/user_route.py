# Library imports
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status

# File imports
from .. import database
from ..schemas import user_schema
from ..controllers import user_controller

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

@router.post('/', response_model=user_schema.ShowUser)
def create_user(request: user_schema.User,db: Session = Depends(get_db)):
    return user_controller.create(request,db)

@router.get('/{id}',response_model=user_schema.ShowUser)
def get_user(id:int,db: Session = Depends(get_db)):
    return user_controller.show(id,db)
