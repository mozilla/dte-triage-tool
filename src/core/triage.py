from src.core.intergrations.testrail_integration import TestRail
from src.config.setting import Settings
class Triage:
    def __init__(self):
        local = Settings.testrail_base_url.split("/")[2].startswith("127")
        self.tr_session = TestRail(
        Settings.testrail_base_url,
        Settings.testrail_username,
        Settings.testrail_api_key,
        local,
    )

