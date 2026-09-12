from fastapi import FastAPI

app = FastAPI(
    title = "SupportPilot.AI",
    description = "AI Powered Customer Support Platform",
    version = "0.1.0"
)

@app.get("/health")
def healthCheck():
    return {"status" : "Healthy"}