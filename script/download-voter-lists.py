# importing the requests library
import http
import cv2
import requests
import pybase64
from PIL import Image
import pytesseract
import logging
import time
import numpy as np


chunk_size = 2000
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
j = 4
while True:
	if j < 5:
		try:
			# api-endpoint
			URL = "https://gateway-voters.eci.gov.in/api/v1/captcha-service/generateCaptcha"

			# location given here
			location = "delhi technological university"

			# defining a params dict for the parameters to be sent to the API
			PARAMS = {'address':location}

			# sending get request and saving the response as response object
			r = requests.get(url = URL, params = PARAMS)

			# extracting data in json format
			data = r.json()
			# extracting latitude, longitude and formatted address
			# of the first matching location
			captcha = data['captcha']
			id = data['id']
			# printing the output
			#print("final data")
			#print(captcha)
			#print(id)
			file1 = open('file1.txt', 'w')
			file1.write(captcha)
			file1.close()
			#open file with base64 string data
			file = open('file1.txt', 'rb')
			encoded_data = file.read()
			file.close()
			#decode base64 string data
			decoded_data=pybase64.b64decode((encoded_data))
			#write the decoded data back to original format in  file
			img_file = open('image.png', 'wb')
			img_file.write(decoded_data)
			img_file.close()
			image = Image.open("image.png").convert("RGBA")
			canvas = Image.new(mode='RGBA',size=image.size,color=(255,255,255,255))
			canvas.paste(image,mask=image)
			canvas.save("new-image.png",format="PNG")
			#image = image.resize((300,150))
			# Resize
			img = cv2.imread("new-image.png")
			(h, w) = img.shape[:2]
			img = cv2.resize(img, (w*2, h*2))
			print("new-image-rgb: ",img)
			# Step 2: Apply adaptive-threshold
			gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			print("grey coloring: ",gry)
			thr = cv2.adaptiveThreshold(gry, 255, 
							   cv2.ADAPTIVE_THRESH_MEAN_C,
							   cv2.THRESH_BINARY, 33, 79)
			print("threshold: ",thr)
			custom_config = r'--psm 6'
			#custom_config = r'-l eng --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789 --psm 7'
			#custom_config = r'-l eng -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789 --psm 6'
			final_text = pytesseract.image_to_string(thr,config=custom_config)
			#final_text = pytesseract.image_to_string(thr,config=custom_config)
			print("final captcha in before stripping the text:",final_text)
			final_text = final_text.strip()
			final_text = final_text.split("\n")[0]
			print("final captcha in text:",final_text)
			#print("final captcha Id : ",id)
			URL2 = "https://gateway-voters.eci.gov.in/api/v1/printing-publish/generate-published-supplement"
			PARAMS2 = {"stateCd":"S01","districtCd":"S0124","acNumber":"125","partNumber":j,"captcha":final_text,"captchaId":id,"langCd":"ENG"}
			print("setting url and params for the post call...")
			print("URL2:",URL2,"Param2:",PARAMS2)
			response = requests.post(url = URL2, json = PARAMS2)
			print("response status:",response.content)
			data = response.json()
			if data['statusCode']== 200:
				print("post call is successful..")
				captcha = data['file']
				filename = data['refId']
				file2 = open('file2.txt', 'w')
				file2.write(captcha)
				file2.close()
				#open file with base64 string data
				file = open('file2.txt', 'rb')
				encoded_data = file.read()
				file.close()
				#decode base64 string data
				decoded_data=pybase64.b64decode((encoded_data))
				#write the decoded data back to original format in  file
				img_file = open(filename, 'wb')
				img_file.write(decoded_data)
				img_file.close()
				time.sleep(4)
				j= j+1
			else:
				print("unsucessful attempt")
				time.sleep(4)
		except:
			continue