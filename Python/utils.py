import logging
import os

from dotenv import load_dotenv
from pathlib import Path


class Paths:
    def __init__(self) -> None:
        self.root_dir = Path(__file__).parent.parent 
        self.prompt_dir = self.root_dir / "Prompts"
        self.county_lookup_prompt_file = self.prompt_dir / "CountyLookupSystemPrompt.txt"
        self.log_dir = self.root_dir / "Logs"
        self.log_file = self.log_dir / "application.log"
        self.secrets_dir = self.root_dir / "Secrets"
        self._ca_certificate = self.secrets_dir / "ca-certificate.crt"  
        self._env_file = self.secrets_dir / ".env"

    @property
    def ca_certificate(self) -> Path:
        if not self._ca_certificate.is_file():
            raise FileNotFoundError(f"CA certificate file not found: {self._ca_certificate.resolve()}")
        return self._ca_certificate
    
    @property
    def env_file(self) -> Path:
        if not self._env_file.is_file():
            raise FileNotFoundError(f".env file not found: {self._env_file.resolve()}")
        return self._env_file

paths = Paths()
load_dotenv(dotenv_path=paths.env_file, override=True)

class Constants:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DB_URI = os.getenv("DB_URI")
    
    @staticmethod
    def debug_env():
        logger = Logger().get_logger()
        logger.debug(f".env file path: {paths.env_file.resolve()}")
        logger.debug(f"OPENAI_API_KEY: {Constants.OPENAI_API_KEY}")
        logger.debug(f"DB_URI: {Constants.DB_URI}")


class Utilities:

    def read_text_file(input_file: Path) -> str:
        with open(input_file) as f:
            return f.read()


class Logger:
    def __init__(self):
        # Ensure the log directory exists
        log_path = paths.log_dir
        log_path.mkdir(parents=True, exist_ok=True)

        # Set up logging configuration
        self.logger = logging.getLogger(paths.log_file.name)
        self.logger.setLevel(logging.DEBUG)

        # Create handlers
        file_handler = logging.FileHandler(paths.log_file)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatters and add to handlers
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
    

logger = Logger().get_logger()