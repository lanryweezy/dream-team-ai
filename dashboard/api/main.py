from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dashboard.api.quick_actions_api import router as quick_actions_router

app = FastAPI(title="Dream Machine API", version="0.1.0")

# CORS for local Next.js dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Quick Actions
app.include_router(quick_actions_router)

@app.get("/health")
async def health():
    return {"status": "ok"}