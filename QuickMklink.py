from src import i18n
from src.config import cfg
import loguru


def main():
    current_system_language: i18n.Languages = i18n.Languages.get_current_system_language()
    is_first_time_start: bool = cfg.get(cfg.is_first_time)
    if is_first_time_start:
        cfg.set(cfg.language, current_system_language.languages)
        cfg.set(cfg.is_first_time, False)
        cfg.save()

    loguru.logger.debug(i18n.I18n())


if __name__ == '__main__':
    main()
