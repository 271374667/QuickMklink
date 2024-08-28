import gettext
import locale
from pathlib import Path
from typing import Callable, Type

from src.config import cfg
from src.core import paths
from src.utils.singleton import singleton


class Languages:
    _domain: str = 'messages'
    _languages: str = 'en_US'
    _localedir: Path = paths.LOCALE_DIR
    _instance: "Languages" = None
    _installed_languages_list: list[Type["Languages"]] = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._installed_languages_list.append(cls)

    @classmethod
    def get_current_system_language(cls) -> "Languages":
        for i in cls._installed_languages_list:
            if i().is_system_language:
                return i()
        return cls()

    @classmethod
    def get_language_by_name(cls, value: str) -> "Languages":
        for i in cls._installed_languages_list:
            if i().languages == value:
                return i()
        return cls()

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def localedir(self) -> Path:
        return self._localedir

    @property
    def languages(self) -> str:
        return self._languages

    @property
    def is_system_language(self) -> bool:
        """Check if the system language is the same as the language of the application."""
        raise NotImplementedError('You must implement the is_system_language property.')

    @classmethod
    def get_installed_languages_list(cls) -> list[Type['Languages']]:
        return cls._installed_languages_list

    def __repr__(self):
        return f'domain: {self.domain}, localedir: {self.localedir}, languages: {self.languages}'


class LanguagesChinese(Languages):
    _languages: str = 'zh_CN'

    @property
    def is_system_language(self) -> bool:
        locale_setting = locale.getlocale()[0]
        return False if locale_setting is None else 'Chinese' in locale_setting


class LanguagesEnglish(Languages):
    _languages: str = 'en_US'

    @property
    def is_system_language(self) -> bool:
        return False


@singleton
class I18n:
    def __init__(self):
        config_language_name: str = cfg.get(cfg.language)
        self._config_language: Languages = Languages.get_language_by_name(config_language_name)
        self._languages: list[Languages] = [x() for x in Languages.get_installed_languages_list()]

    @property
    def trans(self) -> Callable:
        lang = gettext.translation(
            self._config_language.domain,
            self._config_language.localedir,
            languages=[self._config_language.languages]
        )
        lang.install()
        return lang.gettext

    @property
    def languages(self) -> list[Languages]:
        return self._languages

    def reflush(self):
        self.__init__()

    def __repr__(self):
        return f'config_language: {self._config_language.domain}, config_localdir:{self._config_language.localedir}, config_language:{self._config_language.languages}'


if __name__ == '__main__':
    # print(Languages.get_current_system_language())
    print(I18n())
