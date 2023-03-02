## How to use the Blender container:
Build the container: `docker build -t blender blender` 

To generate images, provide the data in the user directory in the form, given by https://github.com/CV-Bench/blender-gen directory.

The Blender container expects two directories to be mounted into `/data/input` and `/data/output` directory.
An examplatory call is given by:
```
docker run -it --gpus all \
-v ${pwd}/users/19938882/blender:/data/input \
-v ${pwd}/users/19938882/dataset:/data/output \
blender
```

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
|Model      | Model Config                | Description | Dataset      |
|-----------|---------------------------------|-------------|--------------|
|RetinaNet  | configs/\_user\_/retinanet.py   | RetinaNet is a state-of-the-art single-stage object detection model that uses a feature pyramid network and a focal loss function to address the issue of class imbalance in object detection. It achieves high accuracy and efficiency in detecting objects at various scales and aspect ratios.| CoCo Format with Keypoints given (Segmentation can be empty)|
Faster-RCNN | configs/\_user\_/faster-rcnn.py | Faster-RCNN is a widely used two-stage object detection model that introduces a region proposal network (RPN) to generate object proposals and a Fast R-CNN network to classify and refine these proposals. It achieves high accuracy in detecting objects while also being computationally efficient.| CoCo Format with Keypoints given (Segmentation can be empty)|

