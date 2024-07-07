import cv2
import os
import torch

from PIL import Image
from transformers import pipeline
from tqdm import tqdm
from backend.utils import convert_mp4_to_avi, get_filename_no_suffix, clear_text_in_file, summarise_file
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

INVALID_ERROR_MESSAGE="INVALID MODEL SELECTED"
MAX_TOKEN_LENGTH = 100

# Load the TrOCR model and processor

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
PROCESSOR = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
MODEL = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten').to(DEVICE)

# Load the image captioning model
# device = 0 is to pass the model to GPU
CAPTIONER = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base", device=0)


def generate_text(pil_image, model_name="captioner"):
    if model_name == "captioner":
        generated_text_arr = CAPTIONER(pil_image, max_new_tokens=MAX_TOKEN_LENGTH)
        return generated_text_arr
    elif model_name == "OCR":
        # Prepare image for the model
        pixel_values = PROCESSOR(images=pil_image, return_tensors="pt").pixel_values.to(DEVICE)
        # Generate text
        generated_ids = MODEL.generate(pixel_values)
        generated_text = PROCESSOR.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_text
    return INVALID_ERROR_MESSAGE


def extract_frames_and_generate_text(video_path, model_name="captioner"):
    """

    :param video_path:
    :param model_name:
    :return:
    """
    # convert video to avi format
    avi_video_path = convert_mp4_to_avi(video_path)

    # Open the video file
    video = cv2.VideoCapture(avi_video_path)

    # Get total number of frames for progress bar
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"total frame count in {avi_video_path} is {total_frames}")

    # Get video name without extension
    video_name = get_filename_no_suffix(avi_video_path)

    # Create output text file
    output_file = os.path.join("output", f"{model_name}_{video_name}.txt")

    clear_text_in_file(output_file)

    frame_count = 0

    # create a dataset to be passed into the pipeline
    pil_img_dataset = []

    # go through the video, extract sparse frames, process into PIL for pipeline
    for _ in tqdm(range(total_frames), desc="Processing frames"):
        ret, frame = video.read()
        if not ret:
            break

        if frame_count % 10 == 0:  # Process every 10th frame
            # Convert frame to RGB (captioner expects RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # captioner can only take in PIL image
            pil_image = Image.fromarray(rgb_frame)
            pil_img_dataset.append(pil_image)


        frame_count += 1


    # Generate caption with specific model over all frames
    # each element is a dictionary, with one key: generated_text
    print("converting video to text, this will take up to a few minutes")
    caption_dict_arr = generate_text(pil_img_dataset, model_name=model_name)

    # write all frames into a file
    with open(output_file, 'w') as f:
        for cur_frame in tqdm(range(len(caption_dict_arr)), desc="VLM convert frame to text"):

            # get the content from each output
            caption = caption_dict_arr[cur_frame][0]['generated_text']
            print(caption)

            # stop if invalid model is used
            if caption == INVALID_ERROR_MESSAGE:
                print(INVALID_ERROR_MESSAGE)
                break
            # Write to file
            f.write(f"Frame {cur_frame * 10}: {caption}\n")

    # Release the video capture object
    video.release()

    # remove duplicates to reduce token length
    summarise_file(output_file)

    return output_file



if __name__=="__main__":

    # Path to your video
    input_video_path = "../past examples/fighting/fight_video.mp4"

    # Extract frames and generate captions
    output_file = extract_frames_and_generate_text(input_video_path, model_name="captioner")

    # print(f"Captions have been written to {output_file}")

