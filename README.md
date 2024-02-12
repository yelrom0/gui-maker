# gui-maker
Makes creates pretty images of GUIs using AI

## Installation

The project is built and tested with python 3.12.1
It is recommended to use a virtual environment to install the dependencies.

`python -m venv venv`

The requirements can be installed using pip and all the dependencies are listed in the requirements.txt file.

`pip install -r requirements.txt`

The project uses GPT4 to generate the image prompts where it uses the OpenAI API. The API key is required to use the project and can be obtained from the [OpenAI website](https://platform.openai.com/api-keys). The API key should be stored in a .env file in the root directory of the project.

The default.env file can be used as a template for the .env file.

## Usage

The project is a command line tool and can be used by running the main.py file.

`python main.py`

The tool will prompt the user to input a description of the GUI and the tool will generate an image of the GUI in the "out" directory.

## Credits

The project uses the OpenAI API to generate the images and the GPT4 model to generate the prompts.

The idea for the project was given to me by [a-folino](https://github.com/a-folino) and I decided to build it as a fun project.

The image generation is done using Stable Diffusion models and the code is based on the [Stable Diffusion]() repository.

I am using a custom embedding model to generate the prompts and the code is based on the [WEBUI Helper embedding model](https://civitai.com/models/2502/webui-helper)