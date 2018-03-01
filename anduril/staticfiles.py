from django.contrib.staticfiles.apps import StaticFilesConfig


class CustomStaticFilesConfig(StaticFilesConfig):
    """Override the static files config to ignore raw SCSS files."""

    ignore_patterns = StaticFilesConfig.ignore_patterns + ["*.scss"]
