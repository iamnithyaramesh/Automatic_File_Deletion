import os
from PIL import Image 
from pytesseract import pytesseract 
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import cv2
from textblob import TextBlob
from rembg import remove


fgbg2 = cv2.createBackgroundSubtractorMOG2()


list_of_indian_festivals=['Diwal','Christmas','New Year','Dussehra','Eid','Ganesh Chaturthi']

path_to_tesseract=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
org_image_path=r'C:\Users\nithy\OneDrive\Desktop\OSProj\sample1.jpeg'
modified_img_path=r'C:\Users\nithy\OneDrive\Desktop\OSProj\sample1.jpeg'


myconfig=r"--psm 6 --oem 3"
img1=Image.open(org_image_path)
output=remove(img1)
output.save(modified_img_path)
print('Modified')

'''pytesseract.tesseract_cmd=path_to_tesseract

text1=pytesseract.image_to_string(img1,config=myconfig)


from textblob import TextBlob
 
a = text2           # incorrect spelling
print("original text: "+str(a))
 
b = TextBlob(a)
 
# prints the corrected spelling
print("corrected text: "+str(b.correct()))

token_words1=sent_tokenize(text1)
token_words2=sent_tokenize(text2)



print(token_words2)

for i in token_words1:
    if i in list_of_indian_festivals:
        print('The image is to be deleted..')
        break

for i in token_words2:
    if i in list_of_indian_festivals:
        os.remove(delete_image_path)
        break
    else:
        print('The image can be kept')
        break'''





