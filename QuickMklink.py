import argparse
from datetime import timedelta
from pathlib import Path

import loguru

from src import i18n
from src import settings
from src.common.clipboard_manager import ClipboardManager
from src.common.context_menu_manager import ContextMenuManager
from src.common.symlink_manager import SymlinkManager
from src.common.tag_parser import get_tag_name, tag_parser_factory
from src.config import cfg
from src.core.paths import LOG_FILE
from src.exceptions.exception_tag import ExceptionTagNoFoundError
from src.presenters.presenter_main import PresenterMain
from src.utils.permission import Permission

# [QuickMklink]"E:\load\python\Project\VideoFusion\assets\images\logo.png"[/QuickMklink]
# 1223 是取消移动文件时候的错误代码
# nuitka QuickMklink.py --standalone --enable-plugin=tk-inter --output-dir=output --windows-icon-from-ico="E:\load\python\Project\QuickMklink\assets\images\logo.ico"
_ = i18n.I18n().trans
loguru.logger.add(LOG_FILE, rotation=timedelta(days=1), retention=timedelta(days=7), level='DEBUG')

Permission().update_to_admin_permission()


@loguru.logger.catch(reraise=True)
def main():
    current_system_language: i18n.Languages = i18n.Languages.get_current_system_language()
    is_first_time_start: bool = cfg.get(cfg.is_first_time)
    if is_first_time_start:
        cfg.set(cfg.language, current_system_language.languages)
        cfg.set(cfg.is_first_time, False)
        cfg.save()
        loguru.logger.debug(f'First time start, set language to {current_system_language.languages}')

    loguru.logger.debug(i18n.I18n())

    parser = argparse.ArgumentParser(description='QuickMklink')
    parser.add_argument('--path', type=str, help=_('The path to the file'))
    parser.add_argument('--setup-right-click-menu', action='store_true', help=_('Setup right click menu'))
    parser.add_argument('--uninstall', action='store_true', help=_('Uninstall right click menu'))

    args = parser.parse_args()
    loguru.logger.debug(args)

    if not args.setup_right_click_menu and not args.uninstall and not args.path:
        presenter = PresenterMain()
        presenter.show()
        return

    if not args.path:
        raise FileNotFoundError('The path to the file is required.')

    context_menu_manager = ContextMenuManager()
    if args.setup_right_click_menu:
        context_menu_manager.setup_right_click_menu()
        return

    if args.uninstall:
        context_menu_manager.uninstallation()
        return

    clipboard_manager = ClipboardManager()
    tag = get_tag_name(clipboard_manager.get_current_text())
    loguru.logger.debug(f'Tag: {tag}')
    tag_parser = tag_parser_factory(tag)
    source_file_path_list: list[Path] = tag_parser.get_paths(clipboard_manager.get_current_text())

    symlink_manager = SymlinkManager()
    source_path: Path = Path(str(args.path).replace('"', '').replace("'", ''))
    if tag == settings.TAGCOPY:
        loguru.logger.debug(f'Paste {source_file_path_list} to {source_path}')
        for i in source_file_path_list:
            symlink_manager.paste(i, source_path)
            loguru.logger.success(f'Paste {i} to {source_path}')
    elif tag == settings.TAGMOVE:
        loguru.logger.debug(f'Cut {source_file_path_list} to {source_path}')
        for i in source_file_path_list:
            symlink_manager.cut(i, Path(source_path))
            loguru.logger.success(f'Cut {i} to {source_path}')
    else:
        loguru.logger.error('Tag not found')
        raise ExceptionTagNoFoundError(f"Tag {tag} not found.")

    # overwrite the clipboard text
    clipboard_manager.clear()
    if not cfg.get(cfg.is_close_cmd_after_finished):
        input(_('Press any key to exit.'))
    MessageDialog().info(_('Mklink'), _('Success'))


if __name__ == '__main__':
    from src.dialog.message_dialog import MessageDialog

    try:
        main()
    except ExceptionTagNoFoundError:
        messages_dialog = MessageDialog()
        messages_dialog.error(_('Mklink Error'),
                              _('You have not copied or cut the file, please copy or cut the file first.'))
    except FileNotFoundError:
        messages_dialog = MessageDialog()
        messages_dialog.error(_('Mklink Error'), _('The path to the file is required.'))
    except FileExistsError:
        messages_dialog = MessageDialog()
        messages_dialog.error(_('Mklink Error'), _('Target path already exists.'))
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error('An error occurred, please check the log for details.')
        messages_dialog = MessageDialog()
        messages_dialog.error(_('Mklink Error'), str(e))
