## How to use the Blender container:
Build the container: `docker build -t blender blender` 

To generate images, provide the data in the user directory in the form, given by https://github.com/CV-Bench/blender-gen directory.

The Blender container expects two directories to be mounted into `/data/input` and `/data/output` directory.
An examplatory call is given by:
```
docker run -it --gpus all \
-v ${pwd}/users/19938882/blender:/data/input \
-v ${pwd}/users/19938882/dataset:/data/output \
blender`

## How to start the Training:
* Generate two datasets using the blender container `train` and `val` 
* Fix the image paths from the blender container

Build container: `docker build -t mmdetection openmmm`

To train a network using this container run 
```
docker run -it --gpus all --memory 16g --name {uid}-training \
-v {pwd}/users/{uid}/dataset/:/data/input \
-v {pwd}/users/{uid}/training/:/data/output \
mmdetection configs/_user_/retinanet.py
```

There are different configs that are currently supported
| Object Detection              |
|-------------------------------|
| configs/\_user\_/retinanet.py   |
| configs/\_user\_/faster-rcnn.py |