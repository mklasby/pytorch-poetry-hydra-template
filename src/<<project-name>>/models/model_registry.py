from typing import Callable, Dict
import logging
import torch

from <<project-name>>.base import FunctionRegistry


class ModelRegistry(FunctionRegistry):
    """Factory to register and get models for each dataset/model pair."""

    _logger: logging.Logger = logging.getLogger(__name__)
    _registry: Dict[str, Dict[str, Callable]] = {}

    @classmethod
    def call(cls, dataset: str, model: str, *args, **kwargs) -> torch.nn.Module:
        return super().call(keys=(dataset, model), *args, **kwargs)
