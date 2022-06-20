import json
import requests
import sys
import cv2
from hanspell import spell_checker
import numpy as np
import os
import shutil

#kakao에서 제공하는 ocr기능
def kakao_ocr(image_path: str):
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'   #kakao REST_API URL
    headers = {'Authorization': "KakaoAK " + "635e11243e3d9903a61094ae4ec459dc"}  #kakao API_KEY

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".JPG", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"image": data})

def ocr_main(image_url:str):
    w_list=[]
    image_path = image_url
    output = kakao_ocr(image_path).json()
    for i in range(len(output['result'])):
           ocr_spell = output['result'][i]['recognition_words'][0]
           w_list.append(ocr_spell)
    corr_spell = check_spell(w_list)

    print(w_list)
    print(corr_spell)
    return ocr_spell 
    
def check_spell(ocr_spell):
    w_list=[]
    for i in ocr_spell:
      spelled_sent = spell_checker.check(i)
      hanspell_sent = spelled_sent.checked 
      w_list.append(hanspell_sent)          
    return w_list

#kakao에서 제공하는 TTS기능
class KakaoTTS:
   def __init__(self, text, API_KEY="444df20598d73ca6836d6fceb4a55dfe"):    
      self.resp = requests.post(
         url="https://kakaoi-newtone-openapi.kakao.com/v1/synthesize",     #kakao REST_API URL
         headers={
            "Content-Type": "application/xml",
            "Authorization": f"KakaoAK {API_KEY}"    #kakao API_KEY
         },
         data=f"<speak><voice name='WOMAN_READ_CALM'>{text}</voice></speak>".encode('utf-8')
      )

   def save(self, filename="C:\\web\\donggri_web\\static\\story_sound\\output.mp3"):
      with open(filename, "wb") as file:
         file.write(self.resp.content)
      
      
#정확한 ocr기능 구현을 위한 이미지 사이즈 조정
def image_resize(img_url:str):
    print(f'img_url: {img_url}')
    src1 = cv2.imread('C:\\donggri_solution\\static\\sorce\\wallpaper.jpg') #배경
    src2 = cv2.imread(img_url) #글자파일 읽기
    
    src2=cv2.resize(src2, (800, 300)) #글씨 작게 수정

    rows, cols,_ = src2.shape
    roi = src1[200:rows+200,150:cols+150] #로고파일 필셀값을 관심영역(ROI)으로 저장함.
    
    gray = cv2.cvtColor(src2, cv2.COLOR_BGR2GRAY) #로고파일의 색상을 그레이로 변경
    _ , mask = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY) #배경은 흰색으로, 그림을 검정색으로 변경
    mask_inv = cv2.bitwise_not(mask)
    
    src1_bg = cv2.bitwise_and(roi,roi,mask=mask) #배경에서만 연산 = src1 배경 복사
    src2_fg = cv2.bitwise_and(src2,src2, mask = mask_inv) #로고에서만 연산

    dst = cv2.bitwise_or(src1_bg, src2_fg) #src1_bg와 src2_fg를 합성    
    src1[200:rows+200,150:cols+150] = dst #src1에 dst값 합성
    s_url = "C:\\donggri_solution\\static\\download\\add.jpg"
    cv2.imwrite(s_url,src1)
    return s_url


if __name__ == "__main__":
   ocr_m = ocr_main("C:\\donggri_solution\\static\\download\\testimg.jpg")


