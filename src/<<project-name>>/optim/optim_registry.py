import logging
from typing import Callable, Dict
import torch.optim as optim
import torch.nn as nn

from <<project-name>>.base import FunctionRegistry


class OptimRegistry(FunctionRegistry):
    """Factory to register and get optimizers for each dataset/model pair."""

    _logger: logging.Logger = logging.getLogger(__name__)
    _registry: Dict[str, Dict[str, Callable]] = {}

    @classmethod
    def call(cls, dataset: str, model: str, *args, **kwargs) -> optim.Optimizer:
        return super().call(keys=(dataset, model), *args, **kwargs)


@OptimRegistry.register(dataset="cifar10", model="wide_resnet22")
@OptimRegistry.register(dataset="cifar10", model="resnet20")
def sgd(module: nn.Module, *args, **kwargs) -> optim.SGD:
    return optim.SGD(module.parameters(), *args, **kwargs)
