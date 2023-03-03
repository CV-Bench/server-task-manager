import os
import json
import shutil
import glob
from pathlib import Path
import subprocess
import traceback

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

    class Dataset:

        def get_and_save_dataset_configuration(base_path, id):
            Utils.make_dir(base_path)

            config = Database.get_dataset_configuration(id)

            with open(os.path.join(base_path, "config.json"), "w") as f:
                json.dump(config["configuration"], f)

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
