import asyncio
import logging
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

logger = logging.getLogger("backend")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

class Counter:
    def __init__(self):
        self.count = 0

    def get_new_count(self):
        self.count += 1
        return self.count
import signal

signal_map = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM',
    signal.SIGQUIT: 'SIGQUIT',
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]:
        signal.signal(sig, lambda *args: print(f"Received {signal_map[sig]} signal"))

    yield
    print("Shutting down")

counter= Counter()
app = FastAPI(lifespan=lifespan)


@app.get("/delays/{delay}")
async def debug(delay: int):
    sequence = counter.get_new_count()
    logger.info(f'{sequence}, Received request for {delay} seconds')
    await asyncio.sleep(delay)
    logger.info(f'{sequence}, Done sleeping')
    return "ok"


if __name__ == "__main__":
    server = uvicorn.Server(config=uvicorn.Config(app, host="0.0.0.0"))
    asyncio.run(server.serve())