import os
import sys

ROOT = "/home/husammm/Desktop/Courses/CS_courses/DL/Clabs/Mini-Rag"
sys.path.append(ROOT)

from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv(".env")

from routes import base_router

app = FastAPI()
app.include_router(base_router)


