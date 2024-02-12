# Local Imports

from api.open_ai_api import OpenAIChat, ImagePrompt

user_text = """A forum with the ability to post, comment, like"
and reply to comments"""


class UIGenerator:

    def __init__(self):
        self.__openai_chat = OpenAIChat()

    async def __generate_ui_prompt(self, user_text) -> ImagePrompt:
        return await self.__openai_chat.respond(user_text)

    async def generate_ui(self):
        response: ImagePrompt = await self.__generate_ui_prompt(user_text)
        print(f"prompt: {response['Prompt']}")
        print(f"negative prompt: {response['NegativePrompt']}")
