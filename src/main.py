import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",           # module:variable
        host="127.0.0.1",    # ⬅️ plus de 0.0.0.0
        port=8000,
        reload=True,
    )
