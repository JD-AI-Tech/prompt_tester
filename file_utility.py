import os
import shutil
from file_clean_up import delete_files


def create_directory(directory_path, clean_flag):
    print(f"jddebug in create_directory  path = {directory_path}  and  clean_flag = {clean_flag}")
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
        else:
            print(f"Directory already exists: {directory_path}")
            if clean_flag:
                delete_files(directory_path)
    except OSError as e:
        print(f"Error creating directory: {directory_path}")
        print(e)


def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Successfully deleted folder: {folder_path}")
    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
    except PermissionError:
        print(f"Permission denied: {folder_path}")
    except Exception as e:
        print(f"An error occurred while deleting folder: {e}")


def check_file_exists(full_file_name):
    try:
        if os.path.isfile(full_file_name):
            return True
        else:
            return False
    except Exception as e:
        print("An error occurred:", e)
        return False


# usage:
if __name__ == "__main__":
    create_directory("./log", True)

    folder_path = './db'
    delete_folder(folder_path)

    file_name = "path/to/myfile.txt"
    exists = check_file_exists(file_name)
    print(exists)
