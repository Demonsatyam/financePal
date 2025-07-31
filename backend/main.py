from fastapi import FastAPI
from routes import auth, policy  # 👈 these must match folder/file names

app = FastAPI()

# 👇 these two lines are critical
app.include_router(auth.router)
app.include_router(policy.router)
