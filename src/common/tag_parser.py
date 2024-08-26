import re
from pathlib import Path

from src import settings
from src.exceptions.exception_tag import ExceptionTagNoFoundError


class TagParser:
    pattern = re.compile(rf'\[{settings.TAG}](.*?)\[/{settings.TAG}]')

    def get_paths(self, value: str) -> list[Path]:
        x: list[str] = self.pattern.findall(value)
        return [Path(i.replace('"', '').replace("'", '')) for i in x]

    def get_tag(self) -> str:
        return settings.TAG


class TagParserCopy(TagParser):
    pattern = re.compile(rf'\[{settings.TAGCOPY}](.*?)\[/{settings.TAGCOPY}]')

    def get_tag(self) -> str:
        return settings.TAGCOPY


class TagParserMove(TagParser):
    pattern = re.compile(rf'\[{settings.TAGMOVE}](.*?)\[/{settings.TAGMOVE}]')

    def get_tag(self) -> str:
        return settings.TAGMOVE


def tag_parser_factory(tag: str) -> TagParser:
    if tag == settings.TAG:
        return TagParser()
    elif tag == settings.TAGCOPY:
        return TagParserCopy()
    elif tag == settings.TAGMOVE:
        return TagParserMove()
    else:
        raise ExceptionTagNoFoundError(f"Tag {tag} not found.")


def get_tag_name(tag: str) -> str:
    if settings.TAGCOPY in tag:
        return settings.TAGCOPY
    elif settings.TAGMOVE in tag:
        return settings.TAGMOVE
    elif settings.TAG in tag:
        return settings.TAG
    else:
        raise ExceptionTagNoFoundError(tag)


if __name__ == '__main__':
    test_text = r'[QuickMklinkCopy]"E:\load\即将删除\代码\群友解决问题\Nuitka获取打包后的exe\exam4.dist"[/QuickMklinkCopy] '
    print(get_tag_name(test_text))
    # tag_parser = TagParser()
    # result = tag_parser.get_paths(
    #     '[QuickMklink]"E:\load\python\Project\VideoFusion\assets\images\logo.png"[/QuickMklink]')
    #
    # for each in result:
    #     print(each.name)
