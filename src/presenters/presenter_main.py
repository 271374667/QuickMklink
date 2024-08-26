from src.config import cfg
from src.i18n import I18n
from src.models.model_main import ModelMain
from src.views.view_main import ViewMain


class PresenterMain:
    def __init__(self):
        self._view = ViewMain()
        self._model = ModelMain()

        self._view.show_cmd_var.set(cfg.get(cfg.is_close_cmd_after_finished))
        self._view.cb_language.items = [x.languages for x in I18n().languages]
        self._view.cb_language.set_current_item(cfg.get(cfg.language))

        self._connect_signal()

    @property
    def view(self) -> ViewMain:
        return self._view

    @property
    def model(self) -> ModelMain:
        return self._model

    def show(self):
        self._view.root.mainloop()

    def _show_cmd_changed(self, *_):
        cfg.set(cfg.is_close_cmd_after_finished, self._view.show_cmd_var.get())
        cfg.save()

    def _language_changed(self, *_):
        cfg.set(cfg.language, self._view.cb_language.current_item)
        cfg.save()

    def _connect_signal(self):
        self._view.show_cmd_var.trace('w', self._show_cmd_changed)
        self._view.pb_register_right_click_menu.config(command=self._model.register_right_click_menu)
        self._view.pb_uninstall_right_click_menu.config(command=self._model.unregister_right_click_menu)
        self._view.cb_language.connect(self._language_changed)


if __name__ == '__main__':
    p = PresenterMain()
    p.show()
