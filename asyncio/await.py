# 동기
# import time

# def a():
#     print("A 작업 시작")
#     time.sleep(2) # 대기 발생
#     print("A 작업 종료")

# def b():
#     print("B 작업 시작")
#     time.sleep(2) # 대기 발생
#     print("B 작업 종료")

# start = time.time()
# a()
# b()
# end = time.time()
# print(f"실행 시간: {end - start:.2f}초") # 약 4.01초

# -------------------------------
# 비동기
import time
import asyncio

async def a():
    print("A 작업 시작")      # [1] a() 실행 시작
    await asyncio.sleep(2)  # [2] 2초 대기 -> 양보
    print("A 작업 종료")      # [5] a() 종료

async def b():
    print("B 작업 시작")      # [3] b() 실행 시작
    await asyncio.sleep(2)  # [4] 2초 대기 -> 양보
    print("B 작업 종료")      # [6] b() 종료

async def main():
    coro1 = a()
    coro2 = b()
    await asyncio.gather(coro1, coro2) # gather에 전달된 순서대로 실행된다. -> coro1이 먼저 나왔으니 coro1부터 실행

start = time.time()
asyncio.run(main()) # 두 개 동시에 실행 -> 동시에 시작, 동시에 완료될 것
end = time.time()
print(f"실행 시간: {end - start:.2f}초") # 약 2.00초