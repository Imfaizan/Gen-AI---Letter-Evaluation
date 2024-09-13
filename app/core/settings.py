import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    CHROMA_DB_DIR: str = "./data/chroma_db"

settings = Settings()
