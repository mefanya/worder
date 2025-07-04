from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config.env")
TOKEN = os.getenv("BOT_TOKEN")

engine = create_engine("sqlite:///worder.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
