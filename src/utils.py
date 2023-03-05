import os
import json
import shutil
import glob
from pathlib import Path
import subprocess
import traceback
from io import BytesIO
import zipfile


from src.database import Database
from src.s3 import S3

from src.logger import logger


class Utils:
    def make_dir(dir):
        try:
            Path(dir).mkdir(parents=True, exist_ok=True)
        except:
            pass

    def copy_dir(src, dest):
        shutil.rmtree(dest)
        
        shutil.copytree(src, dest)

    def rm_path(path):
        try:
            shutil.rmtree(path)
        except:
            os.remove(path)

    class Dataset:

        def get_and_save_dataset_configuration(base_path, id, model_ids):
            Utils.make_dir(base_path)

            config = Database.get_dataset_configuration(id)

            new_config = Utils.Dataset.build_config(config["configuration"], model_ids)

            with open(os.path.join(base_path, "config.json"), "w") as f:
                json.dump(new_config, f)

        def build_config(config, model_ids):
            new_config = {
                **config
            }

            min_max_keys = ["azi", "metallic", "roughness", "inc", "x_pos", "y_pos", "z_pos"]

            new_random = {}

            for key in min_max_keys:
                min_key = f"min_{key}"
                max_key = f"max_{key}"

                new_random[key] = [config["random"].get(min_key), config["random"].get(max_key)]

            new_config["random"] = {
                **new_random,
                "distractors": [0, 0]
            }

            objects = []

            models = Database.get_model_list(model_ids)

            for model in models:
                objects.append({
                    "label": model["name"],
                    "model": str(model["_id"])
                })

            new_config["input"] = {
                "object": objects,
                "environment": [],
                "distractor": []
            }

            return new_config

        def get_and_save_models(base_path, models):
            """
                For all models: Check in local file system if model
                    exists, if so, do nothing, if not, download it.

                Returns list with paths to all models
            """
            model_paths = []

            for model_id in models:
                model_path = os.path.join(base_path, model_id)

                exists = os.path.exists(model_path)

                model_paths.append(model_path)

                if exists:
                    logger.debug(f"Model {model_id} exists ... skipping")
                    continue

                Utils.make_dir(model_path)

                contents = S3.Model.list(model_id)["Contents"]

                for file_identifier in contents:
                    key = file_identifier["Key"].split("/")[-1]

                    file_content = S3.Model.get(
                        os.path.join(model_id, key)
                    ).read()

                    with open(os.path.join(model_path, key), "wb") as f:
                        f.write(file_content)

                        f.close()

                logger.debug(f"download completed for {model_id}")
                    
            return model_paths
        
        def get_and_save_backgrounds(base_path, backgrounds):
            """
                For all backgrounds: Check in local file system if background
                    exists, if so, do nothing, if not, download it.

                Returns list with paths to all backgrounds
            """
            background_paths = []

            for background_id in backgrounds:
                files = glob.glob(os.path.join(base_path, background_id + ".*"))

                if len(files) > 0:
                    background_paths = background_paths + files

                    logger.debug(f"Background {background_id} exists ... skipping")

                    continue

                contents = S3.Background.list(
                    background_id
                )["Contents"]

                for background in contents:
                    key = background["Key"].split("/")[-1]

                    file_content = S3.Background.get(key).read()

                    background_path = os.path.join(base_path, key)

                    background_paths.append(background_path)

                    with open(background_path, "wb") as f:
                        f.write(file_content)

                        f.close()

                logger.debug(f"Background {background_id} downloaded")

            return background_paths
        
    class Network:
        pass

    class Docker:
        def stop_and_remove(id):
            try:
                subprocess.check_output([f"docker stop {id}"], shell=True)
                subprocess.check_output([f"docker rm {id}"], shell=True)

                return True
            except:
                return False

        def start(startup_command):
            subprocess.Popen([startup_command], shell=True)

    class Upload:
        def get_dir_as_zip(dir_path):
            memory_file = BytesIO()

            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                Utils.Upload.zipdir(dir_path, zf)

            memory_file.seek(0)

            return memory_file

        def zipdir(path, ziph):
            # ziph is zipfile handle
            for root, dirs, files in os.walk(path):
                for file in files:
                    ziph.write(os.path.join(root, file), 
                            os.path.relpath(os.path.join(root, file), 
                                            os.path.join(path, '..')))

