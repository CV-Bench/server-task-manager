FROM nytimes/blender:3.3.1-gpu-ubuntu18.04 AS blender
# install git and pull the blender generation script
RUN apt-get update && apt-get install -y git
RUN echo 1
RUN git clone https://github.com/CV-Bench/blender-gen.git /workspace/blender_gen
# move to the git repo 
WORKDIR /workspace/blender_gen
# run the blender generation script
ENTRYPOINT blender --background --python main.py