# System Imports
import os
from shlex import quote as os_quote
from typing import Union

# Package Imports
import asyncio
from openai import AsyncOpenAI

# Local Imports
from api.settings import get_settings

# Load Settings
settings = get_settings()

# Constants
FILE = open("debug_log.txt", "w")

# Init chat log
chat_log = ""

# Init openai interface
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

init_prompt = """
    You are to generate a prompt for Stable Diffusion image generation for a user interface using the user's prompt, each users prompt will be for a new AI image.
    You are not to output any other text other than the prompt and it is to be in the JSON format of:
    {
        "Prompt": "{input_prompt}", 
        "NegativePrompt": "{negative_prompt}"
    }
    Where the input prompt is the prompt to be put into the AI and must include the key word WEBUI at the beginning, followed by a sentance prompt based on the user input and further followed by key words deliminated by commas. 
    The negative prompt are keywords to guide the AI for things to avoid.
    The first sentance of the prompt MUST NOT include commas and must include all of the details of the the user's prompt in that initial sentance in a way that removes any of the user's commas used for the sentance.
    The prompt is then to be followed by key words that are deliminated by commas.
    An example is the following where the user has input the literal phrase "a chat system with green, blue, and red colors and a modern look and feel": 
    {
        "Prompt": "WEBUI design of a chat system with a modern look and feel which also uses green colors for the sender blue for the receiver and red for system messages, UI, UX, Sleek design, Modern, Very detailed, Complimentary colors, 8K, Chat, Messaging,",
        "NegativePrompt": "Messy text, low resolution, blurry, ugly details,"
    }
    The AI will then generate an image based on the prompt and negative prompt. Again, do not output any other text other than the prompt and negative prompt.
"""


async def main():
    print(init_prompt)
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": init_prompt,
            },
            {
                "role": "user",
                "content": "A forum with the ability to post, comment, like and reply to comments",
            },
        ],
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")


asyncio.run(main())
# def openai_respond(text: str, chat_log: str) -> Union[str, str]:

#     # get response from openai interface
#     prompt = f"{chat_log}Human: {text}\n"
#     response = completion.create(
#         prompt=prompt,
#         engine="davinci",
#         stop=["\nHuman"],
#         temperature=0.9,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0.6,
#         best_of=1,
#         max_tokens=150,
#     )

#     return [response.choices[0].text.strip(), chat_log]


# def respond(text: str, chat_log: str) -> Union[str, str]:
#     if text == "hi":
#         return ["hello, how are you?", chat_log]
#     elif text == "bye":
#         return ["goodbye", chat_log]
#     else:
#         # if response not hard coded, get the chatbot to respond
#         return openai_respond(text, chat_log)


# def output(text: str) -> None:
#     print("\n" + text)

#     # check if TTS enabled, if so, speak text
#     if TTS_ENABLED:
#         os.system(f"say {os_quote(text)}")


# output(FIRST_OUTPUT)

# while True:
#     # get some text from the user
#     print("Enter some text: ")
#     text = input()

#     # get a response
#     response_arr = respond(text, chat_log)
#     response_text = response_arr[0]
#     chat_log = response_arr[1]

#     # output the response
#     output(response_text)

#     chat_log = f"{chat_log}Human: {text}\n{response_text}\n"
#     FILE.write(chat_log)

#     if text == "bye":
#         FILE.close()
#         break
