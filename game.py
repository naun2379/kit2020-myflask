import json
def set_charact(name):
    character = {
        "name": name,
        "level" : 1,
        "hp":100,
        "items":["비행기", "ㅁㅁㅁㅁ","ㄴㄴㄴㄴ"],
        "skill":["ㅂㅂㅂ","ㅈㅈㅈ","ㄷㄷㄷ"]
    }
    with open("static/save.txt","w",encoding='utf-8') as f:
        json.dump(character , f , ensure_ascii = False, indent=4)
    #print("{0}님 반갑습니다.(hp {1})로 게임시작합니다".format(character["name"],character["hp"]))
    return character

def save_game(filename,charact):
    f = open(filename,"w" , encoding="utf-8")
    for key in charact:
        print("%s:%s" % (key,charact[key]))
        f.white("%s:%s\n" % (key,charact[key]))
    f.close()

#print("길을 가다가 퉁퉁이를 만났습니다.")
#while(True):
    #try:
        #print("1 싸운다 2. 도망간다")
        #num = int(intput("선택"))
        #break
   # except:
        #print("숫자만 입력하세요")

#game(num,character)