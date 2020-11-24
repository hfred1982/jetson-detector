# Jetson detector

Custom detector running on jetson Nano using https://github.com/dusty-nv/jetson-inference

Run nginx server :
```bash
sudo /usr/local/nginx/sbin/nginx -c /home/fred/Projets/jetson-detector/conf/nginx_text.conf
```

Command to launch on first webcam:
```bash
./detectnet-camera.py csi://0 --input-flip=clockwise --headless
```

