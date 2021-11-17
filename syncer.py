import os
import time
import argparse
import tqdm
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def read_files_online(folder_id):
    """
        Function that takes in the folder ID at Google Drive and 
        returns the list of the contents in that folder.
        Arguments:
            folder_id (string): Google Drive ID of that particular folder
        Returns:
            file_list_titles (List): List of strings of files names present on the folder
    """
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    file_list_titles = []
    for file in file_list:
        file_list_titles.append(file['title'])
    return file_list_titles

def push_file_online(local_path, folder_id):
    """
        Function that takes in the local path of a file and uploads it to the target
        Google Drive folder ID.
        Arguments:
            local_path (string): Local path of the desired file to upload.
            remote_id (string): Google Drive ID of the target folder.
        Returns:
            None
    """
    gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(local_path)
    gfile.Upload() # Upload the file.

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_local_folder", default= "target_local_folder")
    parser.add_argument("--sync_period", default=60, type= int)
    args = parser.parse_args()

    # Create Google Auth Objects
    gauth = GoogleAuth(settings_file="settings.yaml")  
    drive = GoogleDrive(gauth)

    # Specifying target folders and sync periods
    target_local_folder = args.target_local_folder
    online_folder_id = "1OtXmAr-Tzr5w26OqA0AMxHC1E7S9AQp-"
    sync_period = args.sync_period                  # 60 seconds between each sync trial

    try:
        while True:
            print("Starting one sync cycle.")
            file_list_to_upload = os.listdir(target_local_folder)
            files_already_online = read_files_online(online_folder_id)
            online_updated = True
            for file_to_upload in tqdm.tqdm(file_list_to_upload):              # For each file in the target folder
                if target_local_folder + "/" + file_to_upload not in files_already_online:      # Make sure it isn't already uploaded before
                    online_updated = False
                    push_file_online(target_local_folder + "/" + file_to_upload, online_folder_id)    # Then upload
            
            if online_updated == True:
                print("Online file already updated, didn't push anything online.")

            print("Done one sync cycle.")
            time.sleep(sync_period)                                 # Sleep to achieve desired sync-ing frequency 
            

    except KeyboardInterrupt:
        exit()