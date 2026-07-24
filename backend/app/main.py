from fastapi import FastAPI

app = FastAPI(
    title="PlantMind API",
    description="Enterprise Operational Intelligence Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "system": "PlantMind",
        "status": "Running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
