# await를 쓰는 두 가지 조건:

# 1) await는 반드시 비동기 함수 안에서만 사용 가능하다
# import asyncio

# def hello(): # ❌ await를 쓰려면 def 앞에 async 필수
#     await asyncio.sleep(3)

# 2) await 할 수 있는 코드 앞에만 await를 쓸 수 있음
import asyncio
import time

async def hi():
    # await time.sleep(2) # 에러 발생 -> "NoneType object can't be awaited"
    print("start hello")
    await asyncio.sleep(2) # 정상 (time -> asyncio로 변경)
    print("end hello")

async def main():
    print("start main")
    coro = hi()
    await coro
    print("end main")

asyncio.run(main())