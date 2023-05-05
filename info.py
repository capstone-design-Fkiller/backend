# 학과, 학과별 사물함, 사물함의 건물 정보를 저장

# ----건물번호----
# 교내에서 사용하는 건물번호를 그대로 적용, 사이버관은 원래 C로 표현하는데 임의로 5로 지정
BUILDINGS = {'인문과학관':1, 
             '교수학습개발원':2,
             '사회과학관':3,
             '국제학사':4,
             '사이버관':5
            }

#학과 개수 : 33
MAJORS = {'프랑스어학부':{'count':66,'lockers':{'1':66}},
          '독일어과':{'count':67,'lockers':{'1':31,'4':36}},
          '노어과':{'count':50,'lockers':{'1':50}},
          '스페인어과':{'count':139,'lockers':{'1':70,'4':69}},
          '이탈리아어과':{'count':49,'lockers':{'2':25,'4':24}},
          '포르투갈어과':{'count':49,'lockers':{'2':25,'4':24}},
          '네덜란드어과':{'count':54,'lockers':{'4':54}},
          '스칸디나비아어과':{'count':34,'lockers':{'4':34}},
          '말레이인도네시아어과':{'count':25,'lockers':{'1':25}},
          '아랍어과':{'count':49,'lockers':{'1':49}},
          '태국어과':{'count':20,'lockers':{'1':20}},
          '베트남어과':{'count':30,'lockers':{'1':30}},
          '인도어과':{'count':30,'lockers':{'1':30}},
          '터키아제르바이잔어과':{'count':30,'lockers':{'1':30}},
          '페르시아어이란학과':{'count':40,'lockers':{'1':40}},
          '몽골어과':{'count':22,'lockers':{'1':22}},
          'ELLT학과':{'count':35,'lockers':{'1':35}},
          '영미문학문화학과':{'count':44,'lockers':{'1':44}},
          'EICC학과':{'count':30,'lockers':{'1':30}},
          '중국학대학':{'count':120,'lockers':{'1':120}},
          '일본학대학':{'count':92,'lockers':{'1':92}},
          '정치외교학과':{'count':85,'lockers':{'3':50,'4':15,'5':20}},
          '행정학과':{'count':80,'lockers':{'1':10,'3':50,'5':20}},
          '미디어커뮤니케이션학부':{'count':88,'lockers':{'1':48,'3':40}},
          '영어교육과':{'count':25,'lockers':{'2':25}},
          '한국어교육과':{'count':50,'lockers':{'1':14,'2':26}},
          '프랑스어교육과':{'count':30,'lockers':{'1':14,'2':16}},
          '독일어교육과':{'count':12,'lockers':{'2':12}},
          '중국어교육과':{'count':21,'lockers':{'2':21}},
          '상경대학':{'count':150,'lockers':{'1':74,'3':76}},
          '경영학부':{'count':203,'lockers':{'5':203}},
          '국제학부':{'count':66,'lockers':{'3':22,'4':44}},
          'LD학부':{'count':20,'lockers':{'4':20}}
        }