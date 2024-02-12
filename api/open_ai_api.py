# Package Imports
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from json import loads as json_loads

# Local Imports
from api.settings import get_settings

# Load Settings
settings = get_settings()

# Constants
FILE = open("debug_log.txt", "w")

init_prompt = """
        You are to generate a prompt for Stable Diffusion image generation for
        a user interface using the user's prompt, each users prompt will be
        for a new AI image.
        You are not to output any other text other than the prompt and it is
        to be in the JSON format of:
        {
            "Prompt": "{input_prompt}",
            "NegativePrompt": "{negative_prompt}"
        }
        Where the input prompt is the prompt to be put into the AI and must
        include the key word WEBUI at the beginning, followed by a sentance
        prompt based on the user input and further followed by key words
        deliminated by commas.
        The negative prompt are keywords to guide the AI for things to avoid.
        The first sentance of the prompt MUST NOT include commas and must
        include all of the details of the the user's prompt in that initial
        sentance in a way that removes any of the user's commas used for the
        sentance.
        The prompt is then to be followed by key words that are deliminated by
        commas. An example is the following where the user has input the
        literal phrase "a chat system with green, blue, and red colors and a
        modern look and feel":
        {
            "Prompt": "WEBUI design of a chat system with a modern look and
            feel which also uses green colors for the sender blue for the
            receiver and red for system messages, UI, UX, Sleek design, Modern,
            Very detailed, Complimentary colors, 8K, Chat, Messaging,",
            "NegativePrompt": "Messy text, low resolution, blurry, ugly
            details,"
        }
        The AI will then generate an image based on the prompt and negative
        prompt.
        Again, do not output any other text other than the prompt and negative
        prompt.
    """

# OpenAI Chat Type
UIChat = list[dict[str, str]]
ImagePrompt = dict[str, str]


class OpenAIChat:

    def __init__(self):
        # Init openai interface
        self.__client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        # Init chat log
        self.__sys_chat_log: UIChat = [
            {
                "role": "system",
                "content": " ".join(init_prompt.split()),
            }
        ]

    async def respond(self, text: str) -> ImagePrompt:
        chat_arr = self.__sys_chat_log
        chat_arr.append(
            {
                "role": "user",
                "content": text,
            }
        )
        print(f"sys_chat_log: {self.__sys_chat_log}")
        print(f"chat_arr: {chat_arr}")
        # get response from openai interface
        response: ChatCompletion = await self.__client.chat.completions.create(
            model="gpt-4",
            messages=chat_arr,
        )

        return json_loads(response.choices[0].message.content)
