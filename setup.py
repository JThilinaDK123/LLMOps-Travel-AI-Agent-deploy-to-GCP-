from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Multi AI Agents - Travel Partner",
    version="0.1",
    author="Thilina",
    packages=find_packages(),
    install_requires = requirements,
)