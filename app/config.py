import environ

# Load environment variables
env = environ.Env()
environ.Env.read_env()

# Environment variables
SECRET_KEY = env("SECRET_KEY")
ALGORITHM = env("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")
DATABASE_URL = env("DATABASE_URL")
