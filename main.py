import cv2
import numpy as np
from utils import *
import sudukoSolver
import streamlit as st

width,height = 450,450
model = intializemodel()

global grid

def solve(imgArray):

	res = []

	#Preprocess
	# img = cv2.imread(imgPath)
	img = cv2.resize(imgArray,(width,height))
	imgthreshold = preprocess(img)
	imgBlank = np.zeros((height,width,3),np.uint8)
 
	res.append(imgthreshold)


	#Contours
	imgContours = img.copy()
	imgBigContour = img.copy()
	contours, hierarchy = cv2.findContours(imgthreshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(imgContours,contours, -1, (0,255,0), 3)

	res.append(imgContours)

	#bigContour
	biggest, maxArea = biggestContour(contours)

	if(biggest.size!=0):
		biggest = reorder(biggest)
		cv2.drawContours(imgBigContour, biggest, -1, (255,0,0), 25)
		pts1 = np.float32(biggest)
		pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
		matrix = cv2.getPerspectiveTransform(pts1,pts2)
		imgDetectedDigits = imgBlank.copy()
		imgWarpColored = cv2.warpPerspective(img,matrix,(width,height)) 
		imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

		res.append(imgBigContour)
		res.append(imgWarpColored)

		#split image and find digit
		imgSolvedDigits = imgBlank.copy()
		boxes = splitBoxes(imgWarpColored)
		numbers = getPrediction(boxes,model)

		numbers = np.asarray(numbers)
		posArray = np.where(numbers>0, 0, 1)

		grid = np.array_split(numbers,9)
		try:
			sudukoSolver.solve(grid)
		except:
			return []
		print(grid)

		flat = []
		for i in grid:
			for j in i:
				flat.append(j)
		solvedNumbers = flat*posArray
		imgSolvedDigits = displayNumbers(imgSolvedDigits,solvedNumbers)

		res.append(imgSolvedDigits)

		pts2 = np.float32(biggest) # PREPARE POINTS FOR WARP
		pts1 =  np.float32([[0, 0],[width, 0], [0, height],[width, height]]) # PREPARE POINTS FOR WARP
		matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
		imgInvWarpColored = img.copy()
		imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (width, height)) 
		inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img.copy(), 0.5, 1)
		imgDetectedDigits = drawGrid(imgDetectedDigits)
		imgSolvedDigits = drawGrid(imgSolvedDigits)

		res.append(inv_perspective)

	else:
		return []
	return res




