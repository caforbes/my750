from dotenv import load_dotenv

from app import app
from app.db import dbconnect
from app.models import Entry

load_dotenv()


@app.shell_context_processor
def make_shell_context():
    return {"dbconnect": dbconnect, "Entry": Entry}
