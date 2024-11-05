from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def pass_verify(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)