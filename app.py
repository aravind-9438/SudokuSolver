import cv2
import streamlit as st 
import PIL.Image
import numpy as np
import main

# imgPath = "dataset/img_1.png"
# img = cv2.imread(imgPath)
# res = solve(img)

# btn = st.button("Take a picture")

option = st.selectbox(
     'How would you like to be solve Sudoku?',
     ('Select','Take a picture', 'Upload a file'))

 


if(option=='Take a picture'):
	img = st.camera_input("Take a picture")
	if(img):
		img = PIL.Image.open(img).convert('RGB') 
		img = np.array(img) 
		res = main.solve(img)
		if(res):
			for i in res:
				st.image(i)
		else:
			st.write("No Sudoku Found")
elif(option=="Upload a file"):
	img = st.file_uploader("Choose a file", type=['png','jpeg','jpg'])
	if(img):
		img = PIL.Image.open(img).convert('RGB') 
		img = np.array(img) 
		res = main.solve(img)
		if(res):
			for i in res:
				st.image(i)
		else:
			st.write("No Sudoku Found")
 








