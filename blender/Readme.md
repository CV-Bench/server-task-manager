
## Build Docker Image
`docker build -t blender .`
This build the blender dockerfile

## Run Docker Image
`docker run --gpus all -v ${pwd}/../users/EXAMPLE_ID:/data blender`
This runs the blender docker container.

The docker container writes its outputs into the bind mount that is mounted onto the `/data` directory. It also expects a file called `object.ply` and `parameters.json` to be in that directory.

`parameters.json` is currently not used. At the moment the container only uses the `config.py` configuration. Later on this should be more flexbile so that the backend sets the json file and the container utilizes it.