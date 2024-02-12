# System Imports
from os.path import isfile
from os import environ
from requests import get as req_get, Response
from tqdm import tqdm


# TODO: Make this nested in the ImageGen class
class ModelMap:
    WEBUI_EMBEDDING: str = "WEBUI_EMBEDDING"
    CHECKPOINT: str = "CHECKPOINT"

    def __init__(self):
        self.__model_url_map = {
            self.WEBUI_EMBEDDING: "https://civitai.com/api/download/models/2786",
            self.CHECKPOINT: "https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.safetensors",
        }
        self.__model_file_name_map = {
            self.WEBUI_EMBEDDING: "WEBUI.pt",
            self.CHECKPOINT: "CHECKPOINT.safetensors",
        }

    async def __download_model(self, model: str):
        print("Downloading model...")
        # streaming response for progress update
        resp: Response = req_get(
            self.get_model_url(model),
            stream=True,
        )
        # Sizes in bytes.
        total_size = int(resp.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        # print(f"Status: {resp.status_code}")
        # if resp.status_code != 200:
        #     print("Failed to download model")
        #     return
        file_path = f"./models/{self.get_model_file_name(model)}"
        with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
            with open(file_path, "wb") as f:
                for data in resp.iter_content(block_size):
                    pbar.update(len(data))
                    f.write(data)

        if total_size != 0 and pbar.n != total_size:
            raise RuntimeError(f"Could not download model: {model}")

    async def check_models(self):
        # check if the models are downloaded, if not download them
        for model in self.__model_file_name_map.keys():
            if not isfile(f"./models/{model}"):
                await self.__download_model(model)

    def get_model_url(self, model: str) -> str:
        return self.__model_url_map.get(model, "")

    def get_model_file_name(self, model: str) -> str:
        return self.__model_file_name_map.get(model, "")


class ImageGen:
    def __init__(self):
        # Workaround for urllib request issue on MacOS
        environ["no_proxy"] = "*"

        # create model map
        self.__model_map = ModelMap()

    async def generate(self, pos_prompt: str = "", neg_prompt: str = ""):
        await self.__model_map.check_models()
        # return "Image Generated"
