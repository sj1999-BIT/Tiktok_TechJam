from backend.suno_interaction import generate_songs
from backend.vlm_interactions import extract_frames_and_generate_text
from backend.LLM_interactions import generate_suno_prompt

def run(input_video_path, user_prompt):

    # Extract frames and generate captions using vlm
    video_vlm_txt_filepath = extract_frames_and_generate_text(input_video_path, model_name="captioner")

    # interpret the video with user prompt to generate background music prompt using llm
    music_prompt, tags, duration, initial_frame = generate_suno_prompt(video_vlm_txt_filepath, user_prompt)


    # music_prompt = "Hype music, 2 mins long, first min slow, last min increasingly fast"
    # tags =["electric", "jazz"]
    # song_title = ["first_try"]
    out_path = "./output_music_generated"
    return generate_songs(music_prompt, tags=tags, target_music_folder_path=out_path)



if __name__ == "__main__":
    test_video_filepath = "input_video/fight_video.mp4"
    user_prompt = "Dramatic kungfu music, emphasis on fight to the death, more intense, more chinese"

    # # food example
    # user_prompt="I want a background music that is upbeating, delightful, make me feel appetising."
    run(test_video_filepath, user_prompt)