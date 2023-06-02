from setuptools import setup 

setup(
    name="custom_operators",
    version="0.0.3",
    author="Crhistian David Montes Castañeda",
    author_email="david.montes@talentpitch.co",
    description="",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://gitlab.com/interacpedia_modules/interacpedia_file_storage",
    packages=['custom_operators'],
    license="MIT",
    # classifiers=[
    #     "Development Status :: 3 - Beta",
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    install_requires=[ 
        'kubernetes',
        'apache-airflow-providers-cncf-kubernetes==1.0.0'
    ],
    # include_package_data=True,
    # package_data={
    #     '': ['*.ini'],
    # },
)
