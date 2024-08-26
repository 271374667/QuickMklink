from src.core import paths
from src.utils import config_base


class LanguageValidator(config_base.ConfigValidator):
    def validate(self, value):
        """ Verify whether the value is legal """
        available_language: list[str] = [item.name for item in paths.LOCALE_DIR.iterdir() if item.is_dir()]
        return value in available_language

    def correct(self, value):
        """ correct illegal value """
        if not self.validate(value):
            return 'en_US'
        return value


class Config(config_base.QConfig):
    is_first_time = config_base.ConfigItem('General', "FirstTimeStart", True, config_base.BoolValidator())
    is_close_cmd_after_finished = config_base.ConfigItem('General', "CloseAfterFinished", True, config_base.BoolValidator())
    language = config_base.ConfigItem('General', "Language", "en_US", LanguageValidator())


cfg = Config()
cfg.file = paths.CONFIG_FILE
if not paths.CONFIG_FILE.exists():
    cfg.save()
config_base.qconfig.load(paths.CONFIG_FILE, cfg)

if __name__ == '__main__':
    print(cfg.get(cfg.language))
    cfg.set(cfg.language, 'zh_CN')
    cfg.save()
