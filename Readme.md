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

Build container: `docker build -t mmdetection openmm`

To train a network using this container run 
```
docker run -it --gpus all --memory 16g --name {uid}-training \
-v {pwd}/users/{uid}/dataset/:/data/input \
-v {pwd}/users/{uid}/training/:/data/output \
-e UID={uid}
-e ENDPOINT={endpoint}
mmdetection configs/_user_/retinanet.py
```

The following post messages are posted:

| Url | Call | Event |
|-----|------|-------|
|{ENPOINT}/training_finished | {'uid': uid} | on training finished | 
|{ENPOINT}/training_failed | {'uid': uid} | on exception in training script | 


## Model Zoo

There are different configs that are currently supported
|Model      | Task  |Model Config                    | <div style="width:700px">Description</div>| Dataset      |
|-----------|-------|---------------------------------|-------------|--------------|
|RetinaNet  | Object Detection |configs/\_user\_/retinanet_r50_fpn.py   | RetinaNet is a state-of-the-art single-stage object detection model that uses a feature pyramid network and a focal loss function to address the issue of class imbalance in object detection. It achieves high accuracy and efficiency in detecting objects at various scales and aspect ratios.| CoCo Format with Keypoints given (Segmentation can be empty)|
Faster-RCNN | Object Detection | configs/\_user\_/faster_rcnn_r50_fpn | Faster-RCNN is a widely used two-stage object detection model that introduces a region proposal network (RPN) to generate object proposals and a Fast R-CNN network to classify and refine these proposals. It achieves high accuracy in detecting objects while also being computationally efficient.| CoCo Format with Keypoints given (Segmentation can be empty)|
Yolo V3 | Object Detection | configs/\_user\_/yolo_v3.py | Yolo V3 (You Only Look Once version 3) is a real-time object detection model that uses a single neural network to detect objects in images and videos. It uses a fully convolutional architecture and predicts bounding boxes and class probabilities directly from full images in a single forward pass. Yolo V3 also employs a feature extractor based on Darknet-53, which is a variant of the Darknet architecture that uses residual connections and skip connections to improve feature extraction. It is known for its high accuracy and fast processing speed.| CoCo Format with Keypoints given (Segmentation can be empty)|
Yolo X  | Object Detection | configs/\_user\_/yolo_x.py | YOLOX is a single-stage object detector that makes several modifications to YOLOv3 with a DarkNet53 backbone. Specifically, YOLO’s head is replaced with a decoupled one. For each level of FPN feature, we first adopt a 1 × 1 conv layer to reduce the feature channel to 256 and then add two parallel branches with two 3 × 3 conv layers each for classification and regression tasks respectively.| CoCo Format with Keypoints given (Segmentation can be empty)|
DETR  | Object Detection | configs/\_user\_/detr_r50.py | The main ingredients of the new framework, called DEtection TRansformer or DETR, are a set-based global loss that forces unique predictions via bipartite matching, and a transformer encoder-decoder architecture. Given a fixed small set of learned object queries, DETR reasons about the relations of the objects and the global image context to directly output the final set of predictions in parallel.| CoCo Format with Keypoints given (Segmentation can be empty)|
TOOD  | Object Detection | configs/\_user\_/tood_r50_fpn.py | The proposed Task-aligned One-stage Object Detection (TOOD) explicitly aligns the two sub-tasks of object classification and localization in a learning-based manner to address the issue of spatial misalignment in predictions. This is achieved through the design of a novel Task-aligned Head (T-Head) and the use of Task Alignment Learning (TAL) which pulls the optimal anchors of the two tasks closer together during training via a task-aligned loss and sample assignment scheme.| CoCo Format with Keypoints given (Segmentation can be empty)|