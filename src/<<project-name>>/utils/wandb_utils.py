
from typing import Callable, Any, Optional
import logging
from datetime import datetime
import omegaconf
import wandb
from wandb.sdk.wandb_run import Run


class WandbRunNameException(Exception):
    def __init__(self, message, name) -> None:
        super().__init__(f"Wandb run name of {name} is invalid! " f"{message}")


class WandbRunName:
    def __init__(self, name: str):
        self.name = name
        self._verify_name()

    def _verify_name(self):
        if " " in self.name:
            raise WandbRunNameException(
                message="No spaces allowed in name", name=self.name
            )
        if len(self.name) > 128:
            raise WandbRunNameException(
                message="Name must be <= 128 chars", name=self.name
            )


def _wandb_log_check(fn: Callable, log_to_wandb: bool = True) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        if log_to_wandb:
            return fn(*args, **kwargs)
        else:
            return None

    return wrapper


def _disable_wandb() -> None:
    wandb.log = _wandb_log_check(wandb.log, False)
    wandb.log_artifact = _wandb_log_check(wandb.log_artifact, False)
    wandb.watch = _wandb_log_check(wandb.watch, False)
    wandb.init = _wandb_log_check(wandb.init, False)
    wandb.Settings = _wandb_log_check(wandb.Settings, False)


def init_wandb(cfg: omegaconf.DictConfig, global_rank: int):
    _logger = logging.getLogger(__name__)
    # We override logging functions now to avoid any calls
    if global_rank != 0:
        _disable_wandb()
        return None
    if not cfg.wandb.ENABLE:
        _disable_wandb()
        _logger.warning("No logging to WANDB! See cfg.wandb.ENABLE")
        return None
    _ = WandbRunName(name=cfg.wandb.name)  # Verify name is OK
    run = wandb.init(
        name=cfg.wandb.name,
        entity=cfg.wandb.entity,
        project=cfg.wandb.project,
        config=omegaconf.OmegaConf.to_container(
            cfg=cfg, resolve=True, throw_on_missing=True
        ),
        settings=wandb.Settings(start_method=cfg.wandb.start_method),
        dir=cfg.paths.logs,
    )
    return run


def parse_wandb_run_id(run: Optional[Run]) -> str:
    if run is None:
        return datetime.now().strftime("%h-%m-%d-%H-%M")
    else:
        return run.id
