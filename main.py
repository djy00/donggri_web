# from flask import Flask, session, render_template, request, jsonify, escape
from flask import Flask, render_template, request, redirect,url_for
import shutil
import function
import os
import time 
import numpy as np
from konlpy.tag import Okt
Okt = Okt()

img_list1 = ['1','2','3','4','5','6','7','8','9','10']
img_list2 = ['1','2','3','10']
img_list3 = ['1','2','3','4','5','11']

word_answer = ["미안해","만화","심부름","달력","도서관","선행","거짓말"]
h_heart =3
d_heart =3

# 이야기 스토리
with open("./static/story_data/story_img/내용.txt","r", encoding="UTF-8") as f:
    story1 = f.read().splitlines()

# 이야기 스토리(읽기버전)
with open("./static/story_data/story_img/내용copy.txt","r", encoding="UTF-8") as f:
    story2 = f.read().splitlines()
       
# 넌센스 문제 파일
with open("./static/story_data/story_img/넌센스문제.txt", "tr", encoding="UTF-8") as f:
    quiz_li = f.read().splitlines()


def check_words():
    download_url = 'C:\\Users\\ns2ju\\Downloads\\Paint.jpg'     #손글씨 이미지가 저장되는 경로
    image_path = "C:\\donggri_solution\\static\\download\\Paint.jpg"    #손글씨 이미지를 다시 저장되는 경로
    if os.path.exists(download_url):
        os.remove(download_url)
    #Paint파일이 존재 시 삭제
    time.sleep(1)
    shutil.move(download_url, image_path)    #손글씨 이미지를 static파일로 다시 옮겨줌(오류방지)

    image_path = function.image_resize(image_path)    #이미지사이즈 수정
    ori_spell, corr_spell  = function.ocr_main(image_path)    #ocr수행
    print(f"ori_spell: {ori_spell}  corr_spell: {corr_spell}")    #확인
    
    return ori_spell,corr_spell
    
#앱 구성 
app = Flask(__name__)     #__name__은 현재 파일을 의미함(=main.py). app이라고 하는 Flask 인스턴스를 생성한다. 새로운 웹 앱이 생성된다.


#메인페이지
@app.route('/')    # default 페이지
def main():
     return render_template('main.html')   # 사용자가 default 페이지로 접속하면 main()이 실행됨.

#동화목록
@app.route('/fairytail')
def thumbnail():
    return render_template('thumbnail.html')
#그림일기
@app.route('/diary',methods=['GET','POST'])
def diary():
    if request.method == 'POST':
        download_url = 'C:\\Users\\ns2ju\\Downloads\\Paint.jpg'     #손글씨 이미지가 저장되는 경로
        image_path = "C:\\donggri_solution\\static\\download\\Paint.jpg"    #손글씨 이미지를 다시 저장되는 경로

        time.sleep(0.5)
        shutil.move(download_url, image_path)    #손글씨 이미지를 static파일로 다시 옮겨줌(오류방지)

        image_path = function.image_resize(image_path)    #이미지사이즈 수정
        corr_spell  = function.diary_ocr_main(image_path)    #ocr수행
        print(f"corr_spell: {corr_spell}")    #확인    
        nouns=[]
        for i in corr_spell:
            noun = Okt.nouns(i)
            for k in noun:
                nouns.append(k)
        print(nouns)
        
        bglist=os.listdir('static/data/bg')
        print(bglist)
        def selbg(noun):
            for i in noun:
                imgname=i+'.jpg'
                if imgname in bglist:
                    print('배경일치:',i)
                    a = '/static/data/bg/'+imgname
                    return a
                else:
                    print('배경없음:',i)

        img_li=[]
        imglist=os.listdir('static/data/img')
        print(imglist)
        def selimg(noun):
            for i in noun:
                imgname=i+'.png'
                if imgname in imglist:
                    print('이미지일치:',i)
                    s_url = '/static/data/img/'+ imgname
                    img_li.append(s_url)
                else:
                    print('이미지없음:',i)
                    
        path=selbg(nouns)
        selimg(nouns)
        print(img_li)
        return render_template('out.html', text=corr_spell, noun=nouns, sticker=img_li, image=path)
    
    return render_template('diary.html')

#동화_모험
@app.route('/fairytail/adventure')
def adventure():
    global h_heart 
    global d_heart
    h_heart,d_heart = 3,3
    _idx = 0
    first_img= "../static/story_data/story_img/1.png"
    first_sto= story1[_idx]
    return render_template('fairytale.html',first_sound='../static/story_data/story_ost/1.mp3', first_img=first_img, first_sto=first_sto, storyli=story1, page=_idx , storyset = img_list1)

#문제1 비교
@app.route('/fairytail/shoes',methods=['GET','POST'])
def shoes():
    ori_spell,_ = check_words()     
    if ori_spell == "슬리퍼":
        first_img= "../static/story_data/story_img/11.png"
        first_sto= story1[10]
        end_sound='../static/story_data/story_ost/10.mp3'
        return render_template('endingpage.html',first_img=first_img,first_sto=first_sto,endsound=end_sound)
    elif ori_spell == "운동화":
        _idx = 3
        first_img= "../static/story_data/story_img/4.png"
        first_sto= story1[3]
        return render_template('fairytale.html',first_sound='../static/story_data/story_ost/4.mp3', first_img=first_img, first_sto=first_sto, storyli=story1, page=_idx , storyset = img_list1)
    else:
        first_img= "../static/story_data/story_img/3.png"
        first_sto= story1[2]
        _idx =1
        return render_template('popup.html',first_img=first_img,first_sto=first_sto,_idx=_idx)

#문제2 비교
@app.route('/fairytail/person',methods=['GET','POST'])
def person():
    ori_spell,_ = check_words()
    
    if ori_spell == "따라간다":
        first_img= "../static/story_data/story_img/12.png"
        first_sto= story1[11]
        end_sound='../static/story_data/story_ost/11.mp3'
        return render_template('endingpage.html',first_img=first_img,first_sto=first_sto,endsound=end_sound)
    
    elif ori_spell == "안 따라간다":
        _idx = 5
        first_img= "../static/story_data/story_img/6.png"
        first_sto= story1[5]
        return render_template('fairytale.html',first_sound='../static/story_data/story_ost/6.mp3', first_img=first_img, first_sto=first_sto, storyli=story1, page=_idx , storyset = img_list1)
    else:
        first_img= "../static/story_data/story_img/5.png"
        first_sto= story1[4]
        _idx = 2
        return render_template('popup.html',first_img=first_img,first_sto=first_sto,_idx=_idx)    

#단어문제 풀기 
@app.route('/fairytail/quiz', methods=['GET', 'POST'])
def quiz():
    # num = np.random.randint(7)
    a = quiz_li[6]
    global h_heart 
    global d_heart 
    print(a)
    print(h_heart,d_heart)
    if request.method == 'POST':
        ori_spell,_ = check_words()
        if ori_spell in word_answer: # 맞춘경우
            d_heart -= 1
            if d_heart == 0: 
                _idx = 9
                first_img= "../static/story_data/story_img/10.png"
                first_sto= story1[9]
                return render_template('fairytale.html',first_sound='../static/story_data/story_ost/9.mp3', first_img=first_img, first_sto=first_sto, storyli=story1, page=_idx , storyset = img_list1)
            else :
                return render_template('quiz.html', h_heart=h_heart, d_heart=d_heart, quiz_list =a)
            
        else: # 틀린경우
            h_heart -= 1
            if h_heart == 0:            
                return render_template('popup2.html')
            else :
                return render_template('quiz.html', h_heart=h_heart, d_heart=d_heart, quiz_list =a)
         
    return render_template('quiz.html', h_heart=h_heart, d_heart=d_heart, quiz_list =a)

#동화선택지 없이 보기          
@app.route('/fairytail/ending')
def ending():  
    return render_template('fairytaleall.html',storyli=story2,storyset = img_list1)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)