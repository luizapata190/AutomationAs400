from setuptools import setup, find_packages

setup(
    name="as400_automation",
    version="0.1.0",
    description="Librería profesional para automatización de AS400 (Pantalla y Base de Datos)",
    author="Antigravity",
    packages=find_packages(),
    install_requires=[
        "JPype1>=1.5.0",
        "pyodbc>=5.0.0",
        "pyte>=0.8.0",
        "Pillow>=10.0.0",
    ],
)
