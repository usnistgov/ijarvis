from django.apps import AppConfig
from core_explore_keyword_app.permissions import discover


class ExploreKeywordAppConfig(AppConfig):
    """Core application settings"""

    name = "core_explore_keyword_app"

    def ready(self):
        """Run when the app is ready.

        Returns:

        """
        if "migrate" not in sys.argv:
            discover.init_permissions(self.apps)


class BdftConfig(AppConfig):
    name = 'bdft'
