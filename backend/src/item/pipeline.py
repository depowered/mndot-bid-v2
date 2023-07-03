from src.item.stages import clean, download, load, scrape
from src.settings import Settings


def pipeline(settings: Settings) -> None:
    if not scrape.done():
        scrape.run(settings)

    if not download.done():
        download.run(settings)

    if not clean.done():
        clean.run(settings)

    if not load.done():
        load.run(settings)
