import os
import shutil

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