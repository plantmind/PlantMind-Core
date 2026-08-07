import pytest

from app.core.plugins import InvalidPluginVersionError, PluginMetadata


def test_plugin_version_rejects_missing_patch_component() -> None:
    with pytest.raises(InvalidPluginVersionError):
        PluginMetadata(
            plugin_version="1.2",
        )


def test_plugin_version_accepts_zero_major_version() -> None:
    metadata = PluginMetadata(plugin_version="0.1.0")

    assert metadata.plugin_version == "0.1.0"


def test_plugin_version_accepts_standard_version() -> None:
    metadata = PluginMetadata(plugin_version="1.0.0")

    assert metadata.plugin_version == "1.0.0"


def test_plugin_version_accepts_multi_digit_components() -> None:
    metadata = PluginMetadata(plugin_version="12.4.27")

    assert metadata.plugin_version == "12.4.27"


def test_plugin_version_rejects_additional_component() -> None:
    with pytest.raises(InvalidPluginVersionError):
        PluginMetadata(
            plugin_version="1.2.3.4",
        )


def test_plugin_version_rejects_leading_zero_component() -> None:
    with pytest.raises(InvalidPluginVersionError):
        PluginMetadata(
            plugin_version="01.2.3",
        )


def test_plugin_version_rejects_v_prefix() -> None:
    with pytest.raises(InvalidPluginVersionError):
        PluginMetadata(
            plugin_version="v1.2.3",
        )


def test_plugin_version_rejects_surrounding_whitespace() -> None:
    with pytest.raises(InvalidPluginVersionError):
        PluginMetadata(
            plugin_version=" 1.2.3 ",
        )


def test_plugin_version_rejects_prerelease_and_build_suffixes() -> None:
    invalid_versions = (
        "1.2.3-beta",
        "1.2.3+build",
    )

    for plugin_version in invalid_versions:
        with pytest.raises(InvalidPluginVersionError):
            PluginMetadata(
                plugin_version=plugin_version,
            )


def test_plugin_version_error_semantics_and_valid_metadata_are_preserved() -> None:
    with pytest.raises(InvalidPluginVersionError) as exc_info:
        PluginMetadata(
            plugin_version="invalid",
        )

    assert isinstance(exc_info.value, ValueError)

    metadata = PluginMetadata(
        plugin_version="2.3.4",
    )

    assert metadata.plugin_version == "2.3.4"
    assert metadata.contract_version == "1.0"
