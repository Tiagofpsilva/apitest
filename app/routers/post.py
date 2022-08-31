
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schemas
from database import get_db
from typing import List, Optional
import oauth2
from sqlalchemy import func

router = APIRouter(prefix = "/posts", tags=['Posts'])
#as tags vão agrupar as path operations quando vamos à documentação d anossa API para ficar mais legível
    

#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]=""): #using sql we don't need to call db inside and create dependency
    # cursor.execute("""SELECT * FROM "Posts" """)
    # posts = cursor.fetchall()
    
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #usa-se isto para fazer get de todos os posts, sejam o user que faz o request ou não, neste caso faz sentido porque é rede social, os posts são publicos

    #no caso de querermos apenas fazer get dos posts da pessoa que está logada seria:
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

#para fazer join cm sqlalchemy:
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO "Posts" (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()

#     return{"data": new_post}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user.email)
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #esta linha anterior não é eficiente se tivermos um schema muito grande, podemos fazer;

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    #os dois asteriscos fazem "unpack dictionary"; vai colocar as variáveis no formato anterior automaticamente, memso se adicionarmos novos fields

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM "Posts" WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

   # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM "Posts" WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE "Posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",  (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

