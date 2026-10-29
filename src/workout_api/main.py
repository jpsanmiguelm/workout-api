from fastapi import FastAPI

from workout_api.routers import health

app = FastAPI(title="Workout API")
app.include_router(health.router)


@app.get("/")
async def workout_app() -> dict[str, str]:
    return {"message": "Workout API is running"}
