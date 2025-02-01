from fastapi import FastAPI


app = FastAPI()

async def test():
    import asyncio
    await asyncio.sleep(5)

@app.get("/")
async def read_main():
    await test()
    return {"msg": "Hello world"}