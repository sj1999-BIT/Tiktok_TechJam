import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# get openai Key to access service
openai_key = os.getenv("OPENAI_KEY")

client = OpenAI(
    api_key=openai_key
)


def generate_suno_prompt(video_vlm_txt_filepath, user_prompt):
    with open(video_vlm_txt_filepath, 'r') as file:
        vlm_desc_data = file.read()

    LLM_PROMPT = f"I need to generate a description for song to be generated by AI as background music for a video." \
                 f"video descripted at different frames {vlm_desc_data}. " \
                 f"My user wish for following effect {user_prompt}" \
                 f"Assume description remains unchange between frames, video is 30fps. " \
                 f"Generate with following format:" \
                 f" music prompt: describe the music, pacing and instruments used, under 200 characters" \
                 f" tags for the music: [ in format [x, y, ]]," \
                 f" duration of music: single int value, must be between 10 to 240 seconds" \
                 f" which frame music start: single int value." \
                 f"No need detail explanation"

    # print(LLM_PROMPT)

    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": LLM_PROMPT}]
    )

    LLM_response_content = chat_completion.choices[0].message.content

    print(f"LLM response: {LLM_response_content}")

    output_filpath = os.path.join(os.path.dirname(video_vlm_txt_filepath), "suno_summary.txt")
    with open(output_filpath, 'w') as outfile:
        outfile.writelines(LLM_response_content)

    return parse_LLM_to_suno_inputs(output_filpath)

def parse_LLM_to_suno_inputs(LLM_response_filepath):
    # Extract relevant information
    with open(LLM_response_filepath, 'r') as outfile:
        LLM_response_str = outfile.read().lower()

    prompt_start = LLM_response_str.find("music prompt:")
    prompt_end = LLM_response_str.find("tags for the music:")
    prompt = LLM_response_str[prompt_start + len("music prompt:"):prompt_end].strip()

    tags_start = LLM_response_str.find("tags for the music: [")
    tags_end = tags_start + LLM_response_str[tags_start:].find("]\n")
    tags = LLM_response_str[tags_start + len("tags for the music: ["):tags_end]
    tags = tags.split(",")
    cleaned_array = [item.strip().strip('"') for item in tags if item.strip()]

    duration_start = LLM_response_str.find("duration of music: ")
    duration_end = LLM_response_str.find("which frame music starts:")
    duration = LLM_response_str[duration_start + len("duration of music: "):duration_end].split(" ")[0]

    initial_frame_start = LLM_response_str.find("which frame music starts: ")
    initial_frame_end = LLM_response_str[initial_frame_start:].find("\n") + initial_frame_start
    initial_frame = LLM_response_str[initial_frame_start + len("which frame music starts: "):]


    print("Prompt:", len(prompt))
    print("Tags:", cleaned_array)
    print("duration:", duration)
    print("initial_frame:", initial_frame)

    return prompt, cleaned_array, duration, initial_frame


if __name__=="__main__":


    video_vlm_txt_filepath = "../past examples/fighting/captioner_fight_video.txt"
    user_prompt = "intense background music for kungfu fighting scene"

    generate_suno_prompt(video_vlm_txt_filepath, user_prompt)

    parse_LLM_to_suno_inputs("../past examples/fighting/suno_summary.txt")