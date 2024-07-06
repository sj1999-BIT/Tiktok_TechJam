import os
import shutil
from dotenv import load_dotenv

load_dotenv()

from suno import Suno, ModelVersions
client = Suno(
  cookie=os.getenv('SUNO_COOKIE'),
  model_version=ModelVersions.CHIRP_V3_5)

# class SunoServiceHandler:
#     def __init__(self):
#         self.api_url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
#         # self.headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
#         self.headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def clear_folder(folder_path):
    """
    delete all folder and files given folder
    :param folder_path: path to folder
    :return:
    """
    # Check if the directory exists
    if os.path.exists(folder_path):
        # Remove all files and subdirectories
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

        print(f"All contents of '{folder_path}' folder have been deleted.")
    else:
        print(f"The '{folder_path}' folder does not exist.")


def generate_songs(input_prompt, tags=None, title=None, make_instrumental=True, target_music_folder_path=None):
    """
    Generates songs using the Suno API based on the given parameters and downloads them.

    :param input_prompt: str, The main prompt to guide the song generation.
    :param tags: list or None, Optional tags to categorize or influence the song generation.
    :param title: str or None, Optional title for the generated song.
    :param make_instrumental: bool, Whether to generate an instrumental version (default is True).
    :param target_music_folder_path: str or None, Optional path to save the downloaded songs.
    :return: None
    """

    clips = client.generate(
        prompt=input_prompt,
        tags=tags,
        title=title,
        make_instrumental=make_instrumental,
        is_custom=False,
        wait_audio=True
    )

    if target_music_folder_path is not None and not os.path.exists(target_music_folder_path):
        os.makedirs(target_music_folder_path)

    # Download generated songs
    for song in clips:
        if target_music_folder_path is not None:
            file_path = client.download(song=song, path=target_music_folder_path)
        else:
            file_path = client.download(song=song)

        print(f"Song downloaded to: {file_path}")



