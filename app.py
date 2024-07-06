from backend.suno_interaction import generate_songs

def main():
    music_prompt = "Hype music, 2 mins long, first min slow, last min increasingly fast"
    tags =["electric", "jazz"]
    song_title = ["first_try"]
    out_path = "./new_music"
    generate_songs(music_prompt, tags=tags, title=song_title, target_music_folder_path=out_path)



if __name__ == "__main__":
    main()