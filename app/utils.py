from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

#função para tomar password do user, fazer o hash, para depois comparar com a que temas na nossa base de dados e perceber se podemos autenticar aquele user
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)