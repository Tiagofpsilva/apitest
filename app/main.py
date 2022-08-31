from fastapi import FastAPI
import models
from database import engine
from routers import post, user, auth, vote
#from config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)
#este comendado dizia ao sql alchemy para usar o "create" quando queríamos criar as tabelas no postgres, mas com o alembic deixa de ser necessário porque fazemos as atualizações por lá


app = FastAPI()

origins = ["*"]
#aqui podemos especificar os domínios que têm acesso or ex: https://www.google.com. Se quisermos fazer uma API pública colocamos o *, considera qualquer domínio.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"} 