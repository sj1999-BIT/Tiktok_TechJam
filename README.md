# Tiktok_TechJam
## Quick Start

Follow these steps to get the Suno API up and running on your local machine:

1. **setup environment**
   1. pip install python-dotenv
   2. pip install SunoAI
   3. 
2. **use suno ai** 
   2. `generate_songs` Function

      This function generates songs using the Suno API based on given parameters and downloads them.

### Function Signature

```python
def generate_songs(
    input_prompt, 
    tags=None, 
    title=None, 
    make_instrumental=True, 
    target_music_folder_path=None
):
```

### example
```python
from backend.suno_interaction import generate_songs
if __name__ == "__main__":
    music_prompt = "Hype music, 2 mins long, first min slow, last min increasingly fast"
    tags =["electric", "jazz"]
    song_title = ["first_try"]
    out_path = "./new_music"
    generate_songs(music_prompt, tags=tags, title=song_title, target_music_folder_path=out_path)
```

