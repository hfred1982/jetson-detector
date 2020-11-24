import numpy as np
import cv2

import jetson.utils

def analyse_image(net, img, width, height, detections, st):
	# get image from CUDA
	input_image = jetson.utils.cudaToNumpy(img, width, height, 4)
	input_image = cv2.cvtColor(input_image, cv2.COLOR_RGBA2RGB).astype(np.uint8)

	informations = []

	font = cv2.FONT_HERSHEY_SIMPLEX
	for detection in detections:
		#print(detection)
		ID = detection.ClassID
		top = detection.Top
		left = detection.Left
		bottom = detection.Bottom
		right = detection.Right
		area = detection.Area
		item = net.GetClassDesc(ID)

		if item == "person":
			input_image[int(top):int(bottom), int(left):int(right)] = cv2.blur(input_image[int(top):int(bottom), int(left):int(right)], (25, 25))
		cv2.rectangle(input_image, (int(left), int(top)), (int(right), int(bottom)), (225, 0, 0), 2)
		cv2.putText(input_image, str(item), (int(left)+10, int(top) - 20), font, 1, (255,255,255), 3) 
        
		informations.append(str(st) + " : " +item)
        
	cv2.putText(input_image, str(st), (50,50), font, 1, (255,255,255), 3)
    
	return input_image, informations
