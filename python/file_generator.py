import os
import random
import string
import shutil


def generate_random_filename(extension: str = ".dat") -> str:
    """Generate a random filename."""
    return (
        "".join(random.choices(string.ascii_letters + string.digits, k=15)) + extension
    )


def create_random_file(filename: str, size: int) -> str:
    chunk_size = 1024 * 1024  # 1MB
    chunks = size // chunk_size
    remainder = size % chunk_size

    with open(filename, "wb") as f:
        for _ in range(chunks):
            f.write(os.urandom(chunk_size))
        if remainder:
            f.write(os.urandom(remainder))
    return filename


def create_random_directory(dir_name: str, num_files: int, total_size: int) -> None:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    file_size = total_size // num_files
    for _ in range(num_files):
        file_name = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        file_path = os.path.join(dir_name, file_name)
        create_random_file(file_path, file_size)


def remove_file_or_directory(path: str) -> None:
    """Remove a file or directory."""
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def get_directory_size(dir_path: str) -> float:
    """Get the total size of all files in the directory."""
    return sum(
        os.path.getsize(os.path.join(dir_path, f)) for f in os.listdir(dir_path)
    ) / (1024 * 1024)


if __name__ == "__main__":
    file_name = generate_random_filename()
    dir_name = generate_random_filename(extension="")
    create_random_file(file_name, 2 * 1024 * 1024 * 1024)
    create_random_directory(dir_name, 50, 2 * 1024 * 1024 * 1024)
