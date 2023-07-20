import subprocess
from pathlib import Path


def sync_to_s3(
    rclone_remote: str, bucket: str, sync_dir: Path
) -> None:
    source = str(sync_dir)
    destination = f"{rclone_remote}:{bucket}"
    subprocess.run(
        [
            "rclone",
            "--progress",
            "sync",
            f"{source}",
            f"{destination}",
        ]
    )


def sync_from_s3(
    rclone_remote: str, bucket: str, sync_dir: Path
) -> None:
    source = f"{rclone_remote}:{bucket}"
    destination = str(sync_dir)
    subprocess.run(
        [
            "rclone",
            "--progress",
            "sync",
            f"{source}",
            f"{destination}",
        ]
    )
