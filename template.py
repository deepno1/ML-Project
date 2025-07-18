import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

Project_name = "ml-project"

list_of_files = [
    ".github/workflows/.gitkeep",
    "src/{}/__init__.py".format(Project_name),
    "src/{}/components/__init__.py".format(Project_name),
    "src/{}/components/data_ingestion.py".format(Project_name),
    "src/{}/components/data_transformation.py".format(Project_name),
    "src/{}/components/model_trainer.py".format(Project_name),
    "src/{}/components/data_Monitoring.py".format(Project_name),
    "src/{}/pipelines/__init__.py".format(Project_name),
    "src/{}/pipelines/training_pipeline.py".format(Project_name),
    "src/{}/pipelines/Prediction_pipeline.py".format(Project_name),
    "src/{}/exception.py".format(Project_name),
    "src/{}/logger.py".format(Project_name),
    "src/{}/utils.py".format(Project_name),
    "main.py",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py"
]

for file_path in list_of_files:
    file_path = Path(file_path)
    file_dir , file_name = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir,exist_ok = True)
        logging.info("Creating a new dir : {dir} for the file : {f_name} .".format(dir = file_dir, f_name = file_name ))

    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):

        with open(file_path,'w') as f:
            pass
            logging.info("Creating a empty file : {}".format(file_name))

    else:
        logging.info("{} already exists.".format(file_name))