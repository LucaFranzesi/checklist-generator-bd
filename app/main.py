#region ------- IMPORTS -------------------------------------------------------------------------------------

from fastapi import FastAPI
from .routes import checklist
from .model import models
from .db.database import engine

#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

# Create db tables if not existing
models.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()

# Include checklists routing
app.include_router(checklist.router)

#endregion ---- INIT ----------------------------------------------------------------------------------------
#region ------- ROUTES --------------------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the Checklist API"}

#endregion ---- ROUTES --------------------------------------------------------------------------------------