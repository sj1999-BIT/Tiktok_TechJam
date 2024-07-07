import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# get openai Key to access service
openai_key = os.getenv("OPENAI_KEY")

client = OpenAI(
    api_key=openai_key
)



def summarise_video_description(vlm_txt_filepath):
    with open(vlm_txt_filepath, 'r') as file:
        data = file.read()

    print(data)
    LLM_PROMPT = {}


if __name__=="__main__":
    # chat_completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": "Hello world"}]
    # )
    # print(chat_completion)

    summarise_video_description("output/captioner_fight_video.txt")
