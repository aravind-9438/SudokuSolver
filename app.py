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
			for i in range(0,6,3):
				col1, col2, col3  = st.columns(3)
				with col1:
					st.image(res[i])
				with col2:
					st.image(res[i+1])
				with col3:
					st.image(res[i+2])
		else:
			st.write("No Sudoku Found")
elif(option=="Upload a file"):
	img = st.file_uploader("Choose a file", type=['png','jpeg','jpg'])
	if(img):
		img = PIL.Image.open(img).convert('RGB') 
		img = np.array(img) 
		res = main.solve(img)
		if(res):
			for i in range(0,6,3):
				col1, col2, col3 = st.columns(3)
				with col1:
					st.image(res[i])
				with col2:
					st.image(res[i+1])
				with col3:
					st.image(res[i+2])
		else:
			st.write("No Sudoku Found")
 








