from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    testrail_base_url: str = os.environ.get("TESTRAIL_BASE_URL", "")
    testrail_username: str = os.environ.get("TESTRAIL_USERNAME", "")
    testrail_api_key: str = os.environ.get("TESTRAIL_API_KEY", "")
    project_id: int = int(os.environ.get("TESTRAIL_PROJECT_ID", "17"))
