FROM nytimes/blender:3.3.1-gpu-ubuntu18.04 AS blender
RUN echo ${TRAINDIR}
COPY ./blender-gen-for-docker /workspace/blender_gen
WORKDIR /workspace/blender_gen
# ENTRYPOINT ls
ENTRYPOINT blender --background --python main.py