import omegaconf
import hydra
import dotenv


@hydra.main(config_path="configs/", config_name="config", version_base="1.3")
def main(cfg: omegaconf.DictConfig) -> None:
    dotenv.load_dotenv(dotenv_path=".env", override=True)
    ...

if __name__ == "__main__":
    main()
