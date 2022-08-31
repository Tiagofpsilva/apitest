from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import database, schemas, models, utils, oauth2 

router = APIRouter(tags = ['authentication'])


#Path operation para recolher infos de login do user. Usamos schemas.UserLogin para usar o schema especifico do login e garantir uqe o user nos passa a info que nos queremos e nada mais
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    #quando usamos este OAuth2PasswordRequestForm ele retorna um dicionário com "username" e "password", não utiliza o termo "email", ainda que seja esse que estamos a utilizar na base de dados. Neste caso, no Postman vai aceitar as credenciais em Body - "form-data" em vez de "raw".

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    #if the email provided by the user does not match the one in our databases, raise error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    #if the hashed password given by the user doesn't match the hasehd password in our database, raise an error and say "invalid credentials"
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

        #after this, if successful matching, we have to cretae a token and return it

    access_token = oauth2.create_access_token(data = {"user_id":user.id})
        #este dicionário acima representa aquilo que vamos querer por no "payload" (ver imagem no notion), neste caso apenas o user_id - aqui não podemos por nada secreto porque vai ficar visível no token

    return {"access_token": access_token, "token_type": "bearer"}