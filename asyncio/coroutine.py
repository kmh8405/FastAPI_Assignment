# 코루틴 함수(coroutine function)
# -> 앞에 async def를 붙이는 순간, 코루틴 함수이다.

# 동기식
# 1) 함수 정의: def sync() -> sync()없어도 된다.(기본이 동기(sync)라서)
# 2) 함수 호출: foo() => 동기식에서 함수 호출하면 함수가 실행된다.

# def hello():
#     print("hello")

# print(hello())

# 결과:
# hello
# None

# -----------------------

# 비동기식
# 1) 코루틴 함수 정의: async def
# 2) 코루틴 호출: boo() => 비동기식에서 함수 호출하면 coro = boo() 라는 코루틴 객체 생성
# 3) 코루틴 실행

# async def hello():
#     print("hello")

# print(hello())

# 결과: 에러 발생 -> 호출까지만 하고 실행을 안 해줬기 때문(생성만 함)
# 완전히 실행하려면 아래와 같이 3단계까지 완료해야 한다.

import asyncio # 3단계인 실행을 위해서는 이 라이브러리가 필수

async def hello():
    print("hello")

coro1 = hello()

asyncio.run(coro1) # 코루틴 객체를 asyncio의 run이라는 메서드를 통해서 실행해야 hello 출력

# 만약 호출을 여러 개 하려면, 다음과 같이 해야 함
coro1 = hello()
coro2 = hello()

async def main():
    await asyncio.gather(coro1, coro2) # 무조건 gather 사용. asyncio.run(coro1, coro2)이렇게가 안 됨 (리스트로 묶어도 안 됨)

main_coro = main()
asyncio.run(main_coro)