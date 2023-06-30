from src.abstract.stages import clean, download, scrape, split
from src.settings import Settings


def pipeline(settings: Settings, year: int) -> None:
    scrape.run(settings, year)

    if not download.done():
        download.run(settings)

    if not split.done():
        split.run(settings)

    if not clean.done():
        clean.run(settings)
