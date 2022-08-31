
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schemas, utils
from database import get_db

router = APIRouter(prefix = "/users", tags=['Users'])
#as tags vão agrupar as path operations quando vamos à documentação d anossa API para ficar mais legível

 # path operation para criação de novo user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # para criar um hash da password, antes de criar user

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    #criação do user e envia rinfo para database
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")

    return user