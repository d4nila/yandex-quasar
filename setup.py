from setuptools import setup

with open("README.md", 'r', encoding = 'utf-8') as file:
    read_me_description = file.read()

setup(name='yandex_quasar',
      version='0.1',
      description='Yandex Quasar API',
      packages=['quasar_api'],
      author_email='me@biteof.space',
      long_description=read_me_description,
      long_description_content_type="text/markdown",
      url="https://github.com/btfspace/yandex-quasar",
      zip_safe=False,
      install_requires=['httpx', 'dacite'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
)