from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirements.
    '''
    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace('\n','') for req in requirements]
    
    return requirements

setup(
    name = "ML-Project",
    version= '0.0.1',
    author= "Deep Malusare",
    aurthor_email= "deepmalusare43@gmail.com",
    packages= find_packages(),
    install_requires= get_requirements("requirements.txt")
)