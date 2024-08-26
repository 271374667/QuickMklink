import subprocess
from pathlib import Path

import loguru

from src.utils.file_controller import FileController


class SymlinkManager:
    def __init__(self):
        self._file_controller = FileController()

    def paste(self, src: Path, dst: Path):
        """
        Create a symbolic link at the destination pointing to the source.
        """
        if dst.name != src.name:
            dst = dst / src.name

        if dst.exists():
            loguru.logger.error(f'Target path {dst} already exists.')
            return
        try:
            command = f'mklink /D "{dst}" "{src}"'
            loguru.logger.debug(f'Command: {command}')
            subprocess.run(command, check=True, encoding='utf-8', shell=True)
            loguru.logger.success(f'Successfully created symlink from {dst} to {src}')
        except subprocess.CalledProcessError as e:
            loguru.logger.error(f'Failed to create symlink: {e}\nOutput: {e.output}\nError: {e.stderr}')

    def cut(self, src: Path, dst: Path):
        """
        Move the source file to the destination and create a symbolic link at the source pointing to the destination.
        """
        if dst.name != src.name:
            dst_after_move = dst / src.name
        else:
            dst_after_move = dst

        if dst_after_move.exists():
            loguru.logger.error(f'Target path {dst_after_move} already exists.')
            return

        try:
            command = f'mklink /D "{src}" "{dst_after_move}"'
            loguru.logger.debug(f'Command: {command}')
            # Move the source file to the destination
            self._file_controller.move_files_with_progress(str(src), str(dst))

            # Create a symbolic link at the source pointing to the destination
            subprocess.run(command, check=True, encoding='utf-8', shell=True)
            loguru.logger.success(f'Successfully created symlink from {src} to {dst}')
        except (subprocess.CalledProcessError, OSError) as e:
            loguru.logger.error(f'Failed to cut and create symlink: {e}')


if __name__ == '__main__':
    symlink_manager = SymlinkManager()
    # symlink_manager.paste(Path(r"E:\load\python\MyWheel\我的轮子"),
    #                       Path(r'E:\load\python\Project\QuickMklink\locale\zh_CN\LC_MESSAGES'))
    symlink_manager.cut(Path(r'D:\aa'),
                        Path(r'E:\load\python\Tools\i18n'))
