import cv2 
import pytesseract

img = cv2.imread("C:/Users/saisr/OneDrive/Documents/janasena-party-hd-pics/image-to-text.jpeg")

# Adding custom options
custom_config = r'--oem 3 --psm 6'
file_text = pytesseract.image_to_string(img, config=custom_config)
file_text = file_text.strip()
print("Text content:",file_text)
