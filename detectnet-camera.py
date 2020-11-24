#!/usr/bin/python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import argparse
import sys
from datetime import datetime
import requests

import jetson.inference
import jetson.utils

from streamer.videoStreamer import videoStreamer
from tools import analyse_image


class textStream():
	def __init__(self,opt):
		self.url = opt.text_url
		self.send_text(datetime.now().strftime("%d-%b-%Y (%H:%M:%S)") + " - Stream began")
	
	def send_text(self,text):   
		requests.post(self.url, data=text)


# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 
parser.add_argument("--input-width", type=int, default=1280, help="width of image")
parser.add_argument("--input-height", type=int, default=720, help="height of image")
parser.add_argument("--input-rate", type=int, default=30, help="framerate")
parser.add_argument("--rtmp-url", type=str, default="rtmp://192.168.0.20:1935/show/live", help="rtmp url to stream video")
parser.add_argument("--text-url", type=str, default="http://192.168.0.20:8080/pub?id=ch1", help="url to stream text")


is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)

# create streamers
stream = videoStreamer(opt)
text_stream = textStream(opt)
informations = []

# process frames until the user exits
while True:
	st = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
	
	# capture the next image
	img = input.Capture()
	
	# launch detection with network
	detections = net.Detect(img, overlay='none')

	output_image, informations = analyse_image(net, img, opt.input_width, opt.input_height, detections, st, informations)

	stream.send_image(output_image)

	for information in informations:
		text_stream.send_text(information)

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break

stream.end()