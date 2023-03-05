# ARG PYTORCH="1.8.0"
# ARG CUDA="11.1"
# ARG CUDNN="8"

# FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

# ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0+PTX"
# ENV TORCH_NVCC_FLAGS="-Xfatbin -compress-all"
# ENV CMAKE_PREFIX_PATH="$(dirname $(which conda))/../"

# # To fix GPG key error when running apt-get update
# RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
# RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

# RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Install MMCV
# # RUN pip install --no-cache-dir --upgrade pip wheel setuptools
# # RUN pip install --no-cache-dir mmcv-full

# #==1.3.17 -f https://download.openmmlab.com/mmcv/dist/cu101/torch1.6.0/index.html

# # Install MMDetection
# # RUN conda clean --all
# # RUN git clone https://github.com/open-mmlab/mmdetection.git /mmdetection
# # WORKDIR /mmdetection
# # ENV FORCE_CUDA="1"
# # RUN pip install --no-cache-dir -r requirements/build.txt
# # RUN pip install --no-cache-dir -e .


# RUN pip install mmcv-full==1.3.9
# RUN pip install mmdet==2.16.0

# ENTRYPOINT bash

ARG PYTORCH="1.9.0"
ARG CUDA="11.1"
ARG CUDNN="8"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0 8.0"
# 8.5+PTX"
ENV TORCH_NVCC_FLAGS="-Xfatbin -compress-all"
ENV CMAKE_PREFIX_PATH="$(dirname $(which conda))/../"

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


############# Install MMCV
# RUN pip install mmcv-full==1.3.9 -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.9.0/index.html
RUN pip install --no-cache-dir mmcv-full==1.3.17 -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.9.0/index.html

############# Install MMDetection
RUN conda clean --all

RUN echo 3

RUN git clone https://github.com/CV-Bench/mmdetection.git /mmdetection
WORKDIR /mmdetection

ENV FORCE_CUDA="1"
RUN pip install -r requirements/build.txt
RUN pip install --no-cache-dir -e .

# COPY ./configs configs/_user_

ENTRYPOINT ["python", "tools/train.py"]
CMD ["configs/_user_/faster-rccn.py"]
