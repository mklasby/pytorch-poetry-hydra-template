import logging
from typing import Callable, Dict
import torch

from <<project-name>>.base import FunctionRegistry


class DataLoaderRegistry(FunctionRegistry):
    """Factory to register and get dataloaders for each dataset/model pair."""

    _logger: logging.Logger = logging.getLogger(__name__)
    _registry: Dict[str, Dict[str, Callable]] = {}

    @classmethod
    def call(
        cls, dataset: str, model: str, *args, **kwargs
    ) -> torch.utils.data.DataLoader:
        return super().call(keys=(dataset, model), *args, **kwargs)
