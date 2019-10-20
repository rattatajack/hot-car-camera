## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2

def savePicture():
	config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
	pipeline.start(config)
    frames = pipeline.wait_for_frames()
	while True:
		color_frame = frames.get_color_frame
		if not color_frame:
			continue
		cv2.imwrite("sendText/carPic.png",color_frame)
		return


def average():
	# Configure depth and color streams
	pipeline = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

	# Start streaming
	pipeline.start(config)

	averages = 15
	originals = np.empty((480, 640, 15))
	original = np.empty((480, 640))
	try:
		while True:

			# Wait for a coherent pair of frames: depth and color
			frames = pipeline.wait_for_frames()
			depth_frame = frames.get_depth_frame()
			color_frame = frames.get_color_frame()
			if not depth_frame or not color_frame:
				continue

			# Convert images to numpy arrays
			depth_image = np.asanyarray(depth_frame.get_data())
			color_image = np.asanyarray(color_frame.get_data())
			depth_image[depth_image > 2500] = 0
			depth_image = cv2.GaussianBlur(depth_image, (3, 3), 0)
			if(averages > 0):
				originals[:, :, averages - 1] = depth_image.copy()
				averages -= 1
				if(averages == 0):
					sums = np.std(originals, 2)
					print(np.max(sums))
					original = np.mean(originals, axis=2)
					original[sums > 900] = 100000
					return original
	finally:

		# Stop streaming
		pipeline.stop()
		
		
def different(original):
	# Configure depth and color streams
	pipeline = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

	# Start streaming
	pipeline.start(config)

	try:
		while True:

			# Wait for a coherent pair of frames: depth and color
			frames = pipeline.wait_for_frames()
			depth_frame = frames.get_depth_frame()
			color_frame = frames.get_color_frame()
			if not depth_frame or not color_frame:
				continue

			# Convert images to numpy arrays
			depth_image = np.asanyarray(depth_frame.get_data())
			color_image = np.asanyarray(color_frame.get_data())
			depth_image[depth_image > 2500] = 0
			depth_image = cv2.GaussianBlur(depth_image, (3, 3), 0)
			
			if True:
				output = np.zeros((480, 640, 3))
				diff = np.subtract(original, depth_image)
				diff[diff < 250] = 0
				cv2.erode(diff, (5, 5), diff, iterations = 5)

				difference = 0
				# Apply colormap on depth image (image must be converted to 8-bit per pixel first)
				image, contours, hireachy = cv2.findContours(np.uint8(diff), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
				for cont in contours:
					if(cv2.contourArea(cont) > 2000):
						difference += cv2.contourArea(cont)
						cv2.fillPoly(output, pts=[cont], color=(255, 255, 255))
						"""
						hull = cv2.convexHull(cont)
						cv2.drawContours(output, cont, -1, (255, 255, 0), 13)
						cv2.drawContours(output, hull, -1, (0, 255, 255), 10)
						M = cv2.moments(cont)
						cx = int(M['m10']/M['m00'])
						cy = int(M['m01']/M['m00'])
						output[cy, cx] = [255, 0, 255]
						temp = []
						for point in cont:
							if(point[0][1] <= cy):
								temp.append(point)
							elif(point[0][1] == cy):
								left = 640
								right = 0
								if(point[0][0] > right):
									right = point[0][0]
								elif(point[0][0] < left):
									left = point[0][0]
								for i in range(right - left):
									point[0][0] = i
									point[0][1] = cy
									temp.append(point)
						cv2.drawContours(output, temp, -1, (255, 255, 255), 5)
						"""
				
				if difference > 1000000:
					return True
				else:
					return False
				
				#depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(diff, alpha=0.13), cv2.COLORMAP_JET)
				#depth_colormap = cv2.GaussianBlur(diff, (5, 5), 0)
				#modif_map = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
				edges = cv2.Canny(np.uint8(diff), 100, 200, apertureSize = 5, L2gradient=False)
				dist = cv2.distanceTransform(255 - edges, cv2.DIST_L2, 5)
				cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
				# Stack both images horizontally
				images = np.hstack((original, edges, diff, dist))
				# Show images
				cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
				#cv2.namedWindow('edges', cv2.WINDOW_AUTOSIZE)
				#cv2.namedWindow('dist', cv2.WINDOW_AUTOSIZE)
				cv2.imshow('RealSense', images)
				cv2.imshow('output', output)
				#cv2.imshow('edges', edges)
				#cv2.imshow('dist', dist)
				#cv2.imshow('diff', diff)
				cv2.waitKey(1)
	finally:

		# Stop streaming
		pipeline.stop()
