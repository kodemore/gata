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
    for filename in sorted(DOCS_DIRECTORY.glob("**/*.md")):
        file = open(filename)
        yield filename, file.read()


def find_code_blocks(contents: str) -> Iterable:
    return CODE_BLOCK_REGEX.findall(contents)


def find_topics(contents: str) -> Iterable[Tuple[int, str]]:
    # remove code blocks before finding topics
    for code_block in find_code_blocks(contents):
        contents = contents.replace(code_block, "")

    for item in TOPIC_REGEX.findall(contents):
        yield len(item[0]), item[1]


def replace_code_block_in_file(file: Path, code_block: str) -> None:
    reference = FILE_REFERENCE_REGEX.search(code_block)
    try:
        sample_code_filename = reference.group(1)
        sample_code = open(PROJECT_DIR / sample_code_filename).read()
        sample_code += "\n" + reference.group(0)
        doc_file = file.open("r+")
        doc_contents = doc_file.read().replace(code_block, sample_code)
        doc_file.write(doc_contents)

    except IndexError:
        return None


if __name__ == '__main__':
    index = []
    for file, contents in get_all_md_files():
        section_name = convert_filename_to_text(file.name)
        section_topics = []
        for level, topic in find_topics(contents):
            if level > 3:
                continue
            section_topics.append({"name": topic, "level": level})

        index.append({
            "section": section_name,
            "topics": section_topics,
            "file": file.name,
        })

        for code_block in find_code_blocks(contents):
            replace_code_block_in_file(file, code_block)

    readme_contents = open(PROJECT_DIR / ".README.md").read()
    toc = ""
    for section in index:
        toc += f"\n### [{section['section']}](docs/{section['file']})\n"
        for topic in section['topics']:
            toc += "\n" + ("  " * topic["level"]) + f"* [{topic['name']}](docs/{section['file']}#{slugify(topic['name'])})"

    readme_contents += toc

    with open(PROJECT_DIR / "README.md", "w") as readme_file:
        readme_file.write(readme_contents)
