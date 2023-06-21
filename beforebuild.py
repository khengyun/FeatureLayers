import shutil

folder_path = ["dist", "FeatureLayers.egg-info"]  # Đường dẫn đến thư mục dist

for folder in folder_path:
    try:
        shutil.rmtree(folder)
        print('The {} has been deleted successfully.'.format(folder))
    except FileNotFoundError:
        print("The dist directory does not exist.")
    except Exception as e:
        print("An error occurred while deleting the dist folder:", str(e))
