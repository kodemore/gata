import glob, os
from pathlib import Path
from typing import Generator, Iterable, Tuple
import re
import unicodedata

PROJECT_DIR = Path(__file__).parent.parent
DOCS_DIRECTORY = PROJECT_DIR / "docs"

CODE_BLOCK_REGEX = re.compile(r"```[^`]+```")
FILE_REFERENCE_REGEX = re.compile(r"[^\n]*file://([^\n]*)")
TOPIC_REGEX = re.compile(r"(\#+)([^\n]*)")

MARKDOWN_ID_SEPARATOR = "-"


def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore")
    value = re.sub(r"[^\w\s-]", "", value.decode("ascii")).strip().lower()
    return re.sub(r"[%s\s]+" % MARKDOWN_ID_SEPARATOR, MARKDOWN_ID_SEPARATOR, value)


def convert_filename_to_text(filename: str) -> str:
    text = filename.split(".")[0]
    return " ".join(text.split("_")[1:]).capitalize()


def get_all_md_files() -> Generator:
    for filename in DOCS_DIRECTORY.glob("**/*.md"):
        file = open(filename)
        yield filename, file.read()


def find_code_blocks(contents: str) -> Iterable:
    return CODE_BLOCK_REGEX.findall(contents)


def find_topics(contents: str) -> Iterable[Tuple[int, str]]:
    for item in TOPIC_REGEX.findall(contents):
        yield len(item[0]), item[1]


def has_file_reference(code_block: str) -> bool:
    reference = FILE_REFERENCE_REGEX.search(code_block)

    return False


if __name__ == '__main__':
    index = []
    for file, contents in get_all_md_files():
        section_name = convert_filename_to_text(file.name)
        section_topics = []
        for level, topic in find_topics(contents):
            section_topics.append({"name": topic, "level": level})

        index.append({
            "section": section_name,
            "topics": section_topics,
        })

        for code_block in find_code_blocks(contents):
            if has_file_reference(code_block):
                a = 1


    a = 1
