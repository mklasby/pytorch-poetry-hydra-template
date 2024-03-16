import logging


class RankFilter(logging.Filter):

    def __init__(self, global_rank: int):
        super().__init__(name="")
        self.global_rank = global_rank

    def filter(self, _) -> bool:
        if self.global_rank == 0:
            return True
        return False


def add_rank_filter_to_logging(global_rank: int) -> None:
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(RankFilter(global_rank))
