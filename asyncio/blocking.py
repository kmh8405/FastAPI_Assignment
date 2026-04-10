import asyncio
import time

# async def good_job():
#     print("양보합니다...")
#     await asyncio.sleep(2)
#     print("돌려받았습니다...")

# async def bad_job():
#     print("양보 안합니다...")
#     time.sleep(5)
#     print("계속 진행...")

# async def main():
#     coro1 = good_job()
#     coro2 = bad_job()
#     await asyncio.gather(coro1, coro2)

# asyncio.run(main())

# ----------------------------

async def request1():
    print("[1] 새로운 웹 요청...")
    await asyncio.sleep(2)
    print("[1] 응답...")

async def request2():
    print("[2] 새로운 웹 요청...")
    await asyncio.sleep(5)
    print("[2] 응답...")

async def main():
    coro1 = request1()
    coro2 = request2()
    await asyncio.gather(coro1, coro2)

start = time.time()
asyncio.run(main())
end = time.time()
print(f"{end - start:.2f}")