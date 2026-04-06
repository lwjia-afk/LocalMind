from omegaconf import OmegaConf

class ConfigManager:
    _config = None

    @staticmethod
    def load_config(config_path="config.yaml"):
        ConfigManager._config = OmegaConf.load(config_path)
    
    @staticmethod
    def get(path:str = None):
        if ConfigManager._config is None:
            raise Exception("Config not loaded. Please call ConfigManager.load_config() first.")
        keys = path.split(".") if path else []
        config = ConfigManager._config  

        for key in keys:
            if key not in config:
                raise KeyError(f"Key '{key}' not found in config at path '{path}'")
            config = config[key]
        return config