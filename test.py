import os

img_li=[]
li = ['과자','나','친구','까까']
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

selimg(li)
print(img_li)