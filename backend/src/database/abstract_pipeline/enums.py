from enum import StrEnum, auto


class Status(StrEnum):
    NOT_RUN = "not run"
    COMPLETE = auto()
    FAILED = auto()


class Stage(StrEnum):
    DOWNLOAD = "download_stage"
    SPLIT = "split_stage"
    CLEAN = "clean_stage"
    LOAD = "load_stage"
