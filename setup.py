from setuptools import setup, find_packages
setup(
    name="nba_shotcharts",
    version="0.1",
    packages=find_packages(exclude=['tests', 'images']),

    install_requires=['docutils>=0.3', 'pandas>=0.20.3', 'matplotlib>=2.2.2',
                      'numpy>=1.14.2', 'seaborn>=0.8.1'],

    include_package_data=True,

    # metadata for upload to PyPI
    author="Daniel Bratulic",
    author_email="danielbratulic@gmail.com",
    description="Package which is used for plotting shotcharts by NBA players.",
    license="MIT",
    keywords="nba stats analytics sports",
    url="https://github.com/danchyy/nba_shotcharts",
    project_urls={
        "Source Code": "https://github.com/danchyy/nba_shotcharts"
    },
    zip_safe=False
)