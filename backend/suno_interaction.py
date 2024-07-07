import os
from dotenv import load_dotenv
from backend.utils import clear_folder, remove_short_mp3_files

load_dotenv()

from suno import Suno, ModelVersions
client = Suno(
  cookie=os.getenv('SUNO_COOKIE'),
  model_version=ModelVersions.CHIRP_V3_5)

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
        prompt=input_prompt[:200],
        tags=tags,
        title=title,
        make_instrumental=make_instrumental,
        is_custom=False,
        wait_audio=True
    )

    # create the target music files
    if target_music_folder_path is not None and not os.path.exists(target_music_folder_path):
        os.makedirs(target_music_folder_path)

    # remove previous music files
    if os.path.exists(target_music_folder_path):
        clear_folder(target_music_folder_path)

    # Download generated songs
    for song in clips:
        if target_music_folder_path is not None:
            file_path = client.download(song=song, path=target_music_folder_path)
        else:
            file_path = client.download(song=song)

        from mutagen.mp3 import MP3

        # remove music that are too shot
        remove_short_mp3_files(target_music_folder_path)

        print(f"Song downloaded to: {file_path}")

    return file_path



