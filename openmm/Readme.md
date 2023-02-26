(base) PS C:\Users\Lorenz\EigeneDokumente\Universität\Semester 11\Robotik Blockseminar\mmdetection> docker run -it --gpus all  --memory="16g" -v ${pwd}/data:/data mmdetection:v0
root@8ea21acccc7e:/mmdetection# cp /data/detection_config.py configs/faster_rcnn/
root@8ea21acccc7e:/mmdetection# python tools/train.py --gpu-id 0 configs/faster_rcnn/detection_config.py