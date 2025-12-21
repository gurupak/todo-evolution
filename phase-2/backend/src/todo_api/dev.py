import uvicorn


def main():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
    )
