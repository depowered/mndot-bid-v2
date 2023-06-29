import pytest

from src.abstract.stages.download.download_abstract import (
    DownloadError,
    download_abstract_csv,
)
from src.settings import Settings


def test_download_fail() -> None:
    settings = Settings()
    settings.download_abstract_url = "https://httpstat.us/404"
    with pytest.raises(DownloadError) as e:
        download_abstract_csv(settings, 12345)
        assert e.args[0] == "Failed to download abstract 12345. Status code: 404"
