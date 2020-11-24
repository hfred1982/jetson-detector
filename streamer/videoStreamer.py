import subprocess as sp

class videoStreamer():
	def __init__(self,opt):
		command = ['ffmpeg',
			'-y',
			'-f', 'rawvideo',
			'-vcodec', 'rawvideo',
			'-pix_fmt', 'rgb24',
			'-s', "{}x{}".format(opt.input_height, opt.input_width),
			'-r', str(opt.input_rate),
			'-i', '-',
			'-c:v', 'libx264',
			'-pix_fmt', 'yuv420p',
			'-preset', 'ultrafast',
			'-f', 'flv',
			'-b:v', '256k',
			'-b:a', '32k',
			opt.rtmp_url]

		self.proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)
	
	def end(self):   
		self.proc.stdin.close()
		self.proc.stderr.close()
		self.proc.wait()

	def send_image(self,image):
		self.proc.stdin.write(image)   