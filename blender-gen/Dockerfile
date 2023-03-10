FROM nytimes/blender:3.3.1-gpu-ubuntu18.04 AS blender
# install git and pull the blender generation script
RUN apt-get update && apt-get install -y git python3
RUN echo 14
# RUN git clone -b test https://github.com/CV-Bench/blender-gen.git /workspace/blender_gen
RUN git clone https://github.com/CV-Bench/blender-gen.git /workspace/blender_gen

WORKDIR /workspace/blender_gen
RUN pip3.10 install -r requirements.txt

# move to the git repo 
# run the blender generation script
ENTRYPOINT ["python3.10", "main.py"]