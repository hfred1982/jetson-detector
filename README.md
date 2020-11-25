# Jetson detector

Custom detector running on jetson Nano using https://github.com/dusty-nv/jetson-inference

Run nginx server :
```bash
sudo /usr/local/nginx/sbin/nginx -c /home/fred/Projets/jetson-detector/conf/nginx.conf
```

Command to launch on first webcam:
```bash
./detectnet-camera.py csi://0 --input-flip=clockwise --headless
```

Check result on http://192.168.0.20:8080/live.html
