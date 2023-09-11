
from fastapi import FastAPI
from Controller.PdfController import app as pdf_app
import subprocess
import os

app = FastAPI()
app.mount("/pdf", pdf_app)



def run_alembic_migration():
    try:
        # Get the directory of the currently executing script (main.py)
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Run the Alembic migration command
        subprocess.run(['alembic', 'upgrade', 'head'], cwd=script_dir, check=True)
        print("Alembic migration completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Alembic migration failed:", e)


if __name__ == '__main__':
    import uvicorn
    run_alembic_migration()

    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
