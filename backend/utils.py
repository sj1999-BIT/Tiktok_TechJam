import os
import shutil
import imageio


def get_filename_no_suffix(filepath):
    """
    Extracts the filename without its extension from a given file path.

    :param filepath: str, the full path to the file including filename and extension
    :return: str, the filename without the extension
    """
    filename = os.path.basename(filepath)

    # Split the filename and extension
    name, _ = os.path.splitext(filename)

    return name


def convert_mp4_to_avi(input_video_path):
    """
    Main purpose cause cv2 videocapture cannot read mp4 format video.
    Converts an MP4 video file to AVI format.

    :param input_video_path: str, path to the input MP4 video file
    :return: str, path where the output AVI file will be saved
    """
    # Get the directory and filename of the input video
    directory = os.path.dirname(input_video_path)

    # get the filename of video without suffix
    filename = get_filename_no_suffix(input_video_path)

    # Create the output path with .avi extension
    output_path = os.path.join(directory, "avi_format_videos", f"{filename}.avi")

    if os.path.exists(output_path):
        print(f"video already exists at {output_path}")
        return output_path

    reader = imageio.get_reader(input_video_path)
    fps = reader.get_meta_data()['fps']
    writer = imageio.get_writer(output_path, fps=fps)

    for im in reader:
        writer.append_data(im[:, :, :])
    writer.close()

    print(f"video converted to avi format at {output_path}")
    return output_path

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


def clear_text_in_file(file_path):
    """
    Clears the content of a text file if it exists.
    :param file_path: Path to the file.
    :return:
    """
    if os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.truncate(0)  # Clears the file content
        print(f"File '{file_path}' has been cleared.")
    else:
        print(f"File '{file_path}' does not exist.")