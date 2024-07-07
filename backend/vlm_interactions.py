import cv2
import os
import torch

from PIL import Image
from transformers import pipeline
from tqdm import tqdm
from utils import convert_mp4_to_avi, get_filename_no_suffix, clear_text_in_file
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
        generated_text = CAPTIONER(pil_image, max_new_tokens=MAX_TOKEN_LENGTH)[0]['generated_text']
        return generated_text
    elif model_name == "OCR":
        # Prepare image for the model
        pixel_values = PROCESSOR(images=pil_image, return_tensors="pt").pixel_values.to(DEVICE)
        # Generate text
        generated_ids = MODEL.generate(pixel_values)
        generated_text = PROCESSOR.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_text
    return INVALID_ERROR_MESSAGE


def extract_frames_and_generate_text(video_path, model_name="captioner"):

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
    output_file = f"{model_name}_{video_name}.txt"

    clear_text_in_file(output_file)

    frame_count = 0

    with open(output_file, 'w') as f:

        for _ in tqdm(range(total_frames), desc="Processing frames"):
            ret, frame = video.read()
            if not ret:
                break

            if frame_count % 10 == 0:  # Process every 10th frame
                # Convert frame to RGB (captioner expects RGB)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # captioner can only take in PIL image
                pil_image = Image.fromarray(rgb_frame)

                # Generate caption with specific model
                caption = generate_text(pil_image, model_name=model_name)

                # stop if invalid model is used
                if caption == INVALID_ERROR_MESSAGE:
                    print(INVALID_ERROR_MESSAGE)
                    break

                # Write to file
                f.write(f"Frame {frame_count}: {caption}\n")

            frame_count += 1

    # Release the video capture object
    video.release()
    return output_file




if __name__=="__main__":

    # Path to your video
    input_video_path = "input_video/fight_video.mp4"

    # Extract frames and generate captions
    output_file = extract_frames_and_generate_text(input_video_path, model_name="captioner")

    print(f"Captions have been written to {output_file}")