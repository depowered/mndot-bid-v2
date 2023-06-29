import pytest

from src.abstract.stages.scrape.scrape_contract_ids import (
    ScrapeError,
    scrape_contract_ids,
)
from src.settings import Settings


def test_incorrect_url() -> None:
    settings = Settings()
    settings.mndot_abstracts_app = "https://httpstat.us/404"
    with pytest.raises(ScrapeError) as e:
        scrape_contract_ids(settings, 2023)
        assert e.args[0] == "Request failed with status code 404"


@pytest.mark.skipif(
    "not config.getoption('--run-slow')",
    reason="Only run when --run-slow is given",
)
def test_request_timeout() -> None:
    settings = Settings()
    settings.mndot_abstracts_app = "https://httpstat.us/200?sleep=5000"
    with pytest.raises(ScrapeError) as e:
        scrape_contract_ids(settings, 2023)
        assert e.args[0] == "Request timed out"


def test_html_parse_fail() -> None:
    settings = Settings()
    settings.mndot_abstracts_app = "https://httpstat.us/200"
    with pytest.raises(ScrapeError) as e:
        scrape_contract_ids(settings, 2023)
        assert e.args[0] == "Failed to parse HTML"
