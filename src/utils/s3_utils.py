import boto3


def upload_file_to_bucket(file_path: str, new_file_name: str) -> None:
    try:
        print(f'Saving file ({new_file_name}) in s3 bucket.')
        s3_bucket = boto3.resource('s3').Bucket('mrmgmt')
        data = open(file_path, 'rb')
        s3_bucket.put_object(Key=new_file_name, Body=data)
    except Exception as e:
        raise RuntimeError(f'Error while trying to save file to s3 bucket: {e}.')


def remove_files_from_bucket(file_names: list) -> None:
    try:
        print(f'Removing this file(s) from bucket: {file_names}.')
        client = boto3.client('s3')
        for file_name in file_names:
            client.delete_object(Bucket='mrmgmt', Key=file_name)
    except Exception as e:
        raise RuntimeError(f'Error while deleting files from S3: {e}.')


def download_file_from_bucket(s3_file_name: str) -> None:
    try:
        print(f'Downloading {s3_file_name} from S3.')
        client = boto3.client('s3')
        client.download_file('mrmgmt', s3_file_name, s3_file_name)
    except Exception as e:
        raise RuntimeError(f'Error while trying to download file from S3: {e}.')
