import os

import pytest

from py_selenium_auto_core.configurations.logger_configuration import (
    LoggerConfiguration,
)
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper
from tests.test_without_application import TestWithoutApplication


class DynamicConfiguration(LoggerConfiguration):
    def __init__(self, language: str):
        super().__init__({"logger": {"language": language}})

    @property
    def language(self) -> str:
        return self._node.get("language", "en")


class TestLocalizationManager(TestWithoutApplication):
    clicking_key: str = "loc.clicking"
    clicking_value_en: str = "Clicking"
    clicking_value_ru: str = "Клик"
    supported_languages = ["ru", "en"]

    keys_without_params = [
        clicking_key,
        "loc.get.text",
        "loc.el.state.displayed",
        "loc.el.state.not.displayed",
        "loc.el.state.exist",
        "loc.el.state.not.exist",
        "loc.el.state.enabled",
        "loc.el.state.not.enabled",
        "loc.el.state.clickable",
        "loc.el.visual.getimage",
        "loc.el.visual.getlocation",
        "loc.el.visual.getsize",
    ]
    keys_with_params = [
        "loc.el.getattr",
        "loc.el.attr.value",
        "loc.text.value",
        "loc.text.sending.keys",
        "loc.no.elements.found.in.state",
        "loc.no.elements.with.name.found.by.locator",
        "loc.elements.were.found.but.not.in.state",
        "loc.elements.with.name.found.but.should.not",
        "loc.search.of.elements.failed",
        "loc.wait.for.state",
        "loc.wait.for.state.failed",
        "loc.el.visual.image.value",
        "loc.el.visual.location.value",
        "loc.el.visual.size.value",
        "loc.el.visual.getdifference",
        "loc.el.visual.getdifference.withthreshold",
        "loc.el.visual.difference.value",
        "loc.form.dump.save",
        "loc.form.dump.imagenotsaved",
        "loc.form.dump.compare",
        "loc.form.dump.elementnotfound",
        "loc.form.dump.elementsmissedindump",
        "loc.form.dump.elementsmissedonform",
        "loc.form.dump.unprocessedelements",
        "loc.form.dump.compare.result",
    ]

    def test_use_localization_manager_for_clicking_custom_config(self):
        os.environ["profile"] = "custom"
        self.setup_method()
        os.environ["profile"] = ""
        assert self.clicking_value_ru == self.service_provider.localization_manager().get_localized_message(
            self.clicking_key
        )

    def test_use_localization_manager_for_clicking(self):
        assert self.clicking_value_en == self.service_provider.localization_manager().get_localized_message(
            self.clicking_key
        )

    def test_use_localization_manager_for_unknown(self):
        unknown_key = "loc.unknown.fake.key"
        assert unknown_key == self.service_provider.localization_manager().get_localized_message(unknown_key)

    @pytest.mark.parametrize("language", supported_languages)
    @pytest.mark.parametrize("message_key", keys_without_params)
    def test_return_non_key_values_and_not_empty_values_for_keys_without_params(self, language, message_key):
        configuration = DynamicConfiguration(language)
        localized_value = LocalizationManager(configuration, Logger()).get_localized_message(message_key)
        assert localized_value != message_key, "Value should be defined in resource files"
        assert len(localized_value) > 0, "Value should not be empty"

    def test_return_non_key_value_for_keys_present_in_core_if_language_missed_in_sibling_assembly(
        self,
    ):
        configuration = DynamicConfiguration("en")
        localized_value = LocalizationManager(
            configuration, Logger(), RootPathHelper.calling_root_path()
        ).get_localized_message(self.clicking_key)
        assert self.clicking_value_en == localized_value, "Value should match to expected"

    def test_return_non_key_value_for_keys_present_in_core_if_key_missed_in_sibling_assembly(
        self,
    ):
        configuration = DynamicConfiguration("ru")
        localized_value = LocalizationManager(
            configuration, Logger(), RootPathHelper.calling_root_path()
        ).get_localized_message(self.clicking_key)
        assert self.clicking_value_ru == localized_value, "Value should match to expected"

    @pytest.mark.parametrize("language", supported_languages)
    @pytest.mark.parametrize("message_key", keys_with_params)
    def test_return_non_key_values_and_not_empty_values_for_keys_with_params(self, language, message_key):
        configuration = DynamicConfiguration(language)
        try:
            LocalizationManager(configuration, Logger()).get_localized_message(message_key)
        except IndexError:
            return
        assert False, "There must be an error"

    @pytest.mark.parametrize("language", supported_languages)
    @pytest.mark.parametrize("message_key", keys_with_params)
    def test_throws_format_exception_when_keys_require_params(self, language, message_key):
        configuration = DynamicConfiguration(language)
        params = ["a", "b", "c"]
        localized_value = LocalizationManager(configuration, Logger()).get_localized_message(message_key, *params)
        assert message_key != localized_value, "Value should be defined in resource files"
        assert len(localized_value) > 0, "Value should not be empty"
