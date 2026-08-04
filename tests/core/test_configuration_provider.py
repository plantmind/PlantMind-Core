from app.core.configuration.configuration_provider import (
    ConfigurationProvider,
)
from app.config import Settings


def build_settings() -> Settings:
    return Settings(
        APP_NAME="PlantMind",
        VERSION="1.0.0",
        ENVIRONMENT="Development",
        DEPLOYMENT_MODE="On-Premise",
    )


def test_configuration_provider_exposes_settings() -> None:
    provider = ConfigurationProvider(build_settings())

    assert provider.settings.APP_NAME == "PlantMind"
    assert provider.environment == "Development"
    assert provider.deployment == "On-Premise"


def test_configuration_provider_validation() -> None:
    provider = ConfigurationProvider(build_settings())

    provider.validate()
