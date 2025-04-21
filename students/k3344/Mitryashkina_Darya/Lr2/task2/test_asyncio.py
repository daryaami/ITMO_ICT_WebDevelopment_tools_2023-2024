import asyncio
import time

async def main():
    pass


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
