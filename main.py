import omegaconf
from omegaconf import OmegaConf
import hydra
import dotenv


@hydra.main(config_path="configs/", config_name="config", version_base="1.3")
def main(cfg: omegaconf.DictConfig) -> None:
    OmegaConf.resolve(cfg)
    print(cfg)


if __name__ == "__main__":
    # Override env vars using .env BEFORE initializating hydra config!
    dotenv.load_dotenv(dotenv_path=".env", override=True)
    main()
