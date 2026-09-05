"""Configuration file.
Configuration of project variables that we want to have available
everywhere and considered configuration.
"""
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import ClassVar, Optional
from maikol_utils.file_utils import make_dirs


@dataclass
class Configuration:
    """Configuration class for the project."""
    # ===================================================================
    #                       PATHS
    # ===================================================================
    WORKSPACE_PATH: ClassVar[Path] = Path(__file__).resolve().parents[3]
    DATA_PATH: ClassVar[Path] = WORKSPACE_PATH / "data"
    OUTPUT_PATH: ClassVar[Path] = WORKSPACE_PATH / "outputs"
    MODELS_PATH: ClassVar[Path] = WORKSPACE_PATH / "models"
    CONFIG_PATH: ClassVar[Path] = WORKSPACE_PATH / "config"
    LOGS_PATH: ClassVar[Path] = WORKSPACE_PATH / "logs"

    yaml_config_name: Optional[str] = None
    # ===================================================================
    #                       PARAMETER
    # ===================================================================
    exp_name: str = "base_name"
    seed: int = 42
    gym_id: Optional[str] = None
    learning_rate: float = 2.5e-4
    total_timesteps: int = 25_000
    torch_deterministic: bool = True
    cuda: bool = True
    track_run: bool = False
    wandb_project_name: str = "RL"
    wandb_entity: Optional[str] = None

    def __post_init__(self):
        # Basic setup: create folders and load yaml config if provided
        make_dirs([self.DATA_PATH, self.MODELS_PATH, self.LOGS_PATH, self.CONFIG_PATH])
        if self.yaml_config_name:
            self._load_yaml_configuration(self.yaml_config_name)
        # More stuff
        ...

    def _load_yaml_configuration(self, yaml_file: str) -> None:
        """Load config values from a YAML file under MODELS_PATH."""
        config_path = self.MODELS_PATH / yaml_file
        with open(config_path, "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file) or {}
        for key, value in yaml_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
