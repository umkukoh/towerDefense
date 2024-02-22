def add(self, a, b):
    return a+b

class 학생():
    name = "김태은"
    age = "16"
    
    def __init__(self) -> None:
        self.name = "김태은"
        self.age = "16"
    
    # member method
    def 이름얻기(self):
        return self.name
    
    def getOld(self):
        self.age += 1
        
    
    def 이름얻기():
        얻기 = str(학생.name)
        return 얻기
    
    def 나이증가(age):
        증가 = str(age) + "1"
        return 증가
    
    
    
    
# 학생1 = 학생()
# 학생2 = 학생()
#나이증가(학생1)

print(학생1.name)
print(학생2.name)

이름1 = 학생1.이름얻기()
print(이름1)