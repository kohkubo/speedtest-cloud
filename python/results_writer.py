import platform
import matplotlib.pyplot as plt

from file_details_dataclass import FileDetails


def save_to_file(
    upload_details: FileDetails,
    download_details: FileDetails,
    concurrent: bool,
    filename="results.txt",
):
    with open(filename, "w") as file:
        file.write("Execution Environment:\n")
        file.write(f"OS: {platform.system()} {platform.release()}\n")
        file.write(f"Machine: {platform.machine()}\n")
        file.write(f"Python Version: {platform.python_version()}\n\n")

        file.write(f"Concurrent Execution: {'Yes' if concurrent else 'No'}\n\n")

        file.write("Uploaded file details:\n")
        file.write(f"File path: {upload_details.path}\n")
        file.write(f"File size: {upload_details.size:.2f} MB\n")
        file.write(f"Time taken: {upload_details.time:.2f} seconds\n")
        file.write(f"Upload speed: {upload_details.speed:.2f} MB/s\n\n")

        file.write("Downloaded file details:\n")
        file.write(f"Blob path: {download_details.path}\n")
        file.write(f"File size: {download_details.size:.2f} MB\n")
        file.write(f"Time taken: {download_details.time:.2f} seconds\n")
        file.write(f"Download speed: {download_details.speed:.2f} MB/s\n")

        # 図を作成
        plot_results(upload_details, download_details, concurrent)


def plot_results(
    upload_details: FileDetails,
    download_details: FileDetails,
    concurrent: bool,
    title="Results",
):
    labels = ["Upload", "Download"]
    speeds = [upload_details.speed, download_details.speed]

    fig, ax = plt.subplots()
    ax.bar(labels, speeds, color=["blue", "green"])

    ax.set_ylabel("Speed (MB/s)")
    ax.set_title(f'{title} - Concurrent: {"Yes" if concurrent else "No"}')
    ax.legend()

    plt.show()
