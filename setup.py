#Setup setup.py to build package

from setuptools import find_packages,setup
from typing import List

#removing -e . from pacakages list as constant variable
hyp="-e ."

def get_requirements(file_path:str)->List[str]:
    '''
This function returns a list of requirements and removes nextline character in the list

    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

    if hyp in requirements:
        requirements.remove(hyp)
    return requirements

#package metdata
setup(
    name="end2end",
    version="0.0.1",
    author="Sameer Sharma",
    author_email="samy.sharmaa@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)