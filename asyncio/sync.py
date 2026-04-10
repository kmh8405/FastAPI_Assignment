# 동기 (synchronous)
# A역할 -> B역할 : A역할이 끝난 뒤에 B역할 실행

import time

def hello():
    time.sleep(3)
    print("hello")

hello()
