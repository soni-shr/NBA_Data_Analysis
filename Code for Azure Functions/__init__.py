import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from kaggle.api.kaggle_api_extended import KaggleApi

def main(req: func.TimerRequest, outputBlob: func.Out[func.InputStream]) -> str:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    api = KaggleApi()
    api.authenticate()
    
    # Download the dataset (replace 'dataset-id' with the actual ID of the dataset you want to download)
    api.dataset_download_files('wyattowalsh/basketball', path="/tmp")
    
    # Specify the absolute path of the target directory
    target_dir = "/tmp"

    # Unzip the downloaded files
    import zipfile
    with zipfile.ZipFile('/tmp/basketball.zip', 'r') as zip_ref:
        zip_ref.extractall(target_dir)

    # Change this to nbadataset once code is finalized. Not adding it now because it will trigger storage based event
    # trigger.
    container_name = 'nbadataset'
    directory_path = '/tmp/csv'
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)

    for filename in os.listdir(directory_path):
        if filename != "play_by_play.csv":
            file_name = filename
            logging.info('%s is being uploaded.....', filename)
            file_path = os.path.join(directory_path, filename)
            blob_path = file_name
            blob_client = container_client.get_blob_client(blob_path)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
