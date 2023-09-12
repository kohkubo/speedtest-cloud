import os
import time
import argparse
from google.cloud import storage
import file_generator
from results_writer import save_to_file

from file_details_dataclass import FileDetails


def transfer_blob(
    bucket_name, source_path, destination_path, file_size_mb, operation="upload"
) -> FileDetails:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_path)

    start_time = time.time()

    if operation == "upload":
        with open(source_path, "rb") as source_file:
            blob.upload_from_file(source_file)
    elif operation == "download":
        blob.download_to_filename(source_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    speed = file_size_mb / elapsed_time

    print(f"Total time: {elapsed_time:.2f} seconds")
    print(f"Total speed: {speed:.2f} MB/s")
    print(f"Total size: {file_size_mb:.2f} MB")
    return FileDetails(
        path=source_path, size=file_size_mb, time=elapsed_time, speed=speed
    )


def transfer_directory(
    bucket_name, source_dir, destination_dir, file_size_mb, operation="upload"
) -> FileDetails:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    start_time = time.time()

    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            blob_path = os.path.join(destination_dir, file)

            if operation == "upload":
                blob = bucket.blob(blob_path)
                with open(file_path, "rb") as source_file:
                    blob.upload_from_file(source_file)
            elif operation == "download":
                blob = bucket.blob(blob_path)
                blob.download_to_filename(file_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    speed = file_size_mb / elapsed_time

    print(f"Total time: {elapsed_time:.2f} seconds")
    print(f"Total speed: {speed:.2f} MB/s")
    print(f"Total size: {file_size_mb:.2f} MB")
    return FileDetails(
        path=source_dir, size=file_size_mb, time=elapsed_time, speed=speed
    )


def main(bucket_name):
    print(f"Bucket name: {bucket_name}")
    file_name = file_generator.generate_random_filename()
    dir_name = file_generator.generate_random_filename(extension="")

    # ファイルとディレクトリの作成
    print("Creating random file and directory...")
    file_generator.create_random_file(file_name, 2 * 1024 * 1024 * 1024)
    file_generator.create_random_directory(dir_name, 50, 2 * 1024 * 1024 * 1024)

    # ファイルサイズの取得
    print("Getting file and directory sizes...")
    file_size_mb = os.path.getsize(file_name) / (1024 * 1024)
    dir_size_mb = file_generator.get_directory_size(dir_name)
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"Directory size: {dir_size_mb:.2f} MB")

    # ファイルの送受信速度の計測
    print("Measuring upload and download speeds...")
    print("Uploading file...")
    upload_file_details = transfer_blob(
        bucket_name, file_name, file_name, file_size_mb, operation="upload"
    )
    file_generator.remove_file_or_directory(file_name)  # アップロード後にファイルを削除

    print("Downloading file...")
    download_file_details = transfer_blob(
        bucket_name,
        "downloaded_" + file_name,
        file_name,
        file_size_mb,
        operation="download",
    )
    file_generator.remove_file_or_directory(
        "downloaded_" + file_name
    )  # ダウンロード後にファイルを削除

    # ディレクトリの送受信速度の計測
    print("Uploading and downloading directory...")
    print("Uploading directory...")
    upload_dir_details = transfer_directory(
        bucket_name, dir_name, dir_name, dir_size_mb, operation="upload"
    )
    file_generator.remove_file_or_directory(dir_name)  # アップロード後にディレクトリを削除

    print("Downloading directory...")
    download_dir_details = transfer_directory(
        bucket_name,
        dir_name,
        "downloaded_" + dir_name,
        dir_size_mb,
        operation="download",
    )
    file_generator.remove_file_or_directory(
        "downloaded_" + dir_name
    )  # ダウンロード後にディレクトリを削除

    # 計測結果をファイルに保存
    print("Saving results to file...")
    save_to_file(
        upload_file_details, download_file_details, filename="file_results.txt"
    )
    save_to_file(upload_dir_details, download_dir_details, filename="dir_results.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload and download files to/from GCS and measure the time."
    )
    parser.add_argument("bucket_name", help="The name of the GCS bucket.")
    args = parser.parse_args()

    main(args.bucket_name)
