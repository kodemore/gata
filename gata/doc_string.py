import re
from inspect import cleandoc
from typing import Any, List, Match


DOC_COMPONENT_REGEX = re.compile(r"^:([^:]+):(.*?)$", re.I | re.M)


class DocComponent:
    def __init__(self, component_type: str, attributes: List[str], description: str = ""):
        self.type = component_type
        self.attributes = attributes
        self.description = description


class DocString:
    """
    Simple ReST doc string parser.
    """

    def __init__(self, target: Any):
        """
        Reads doc string of classes and functions and parses it into components.
        """
        self.raw_doc = cleandoc(target.__doc__ or "")
        self._components: List[DocComponent] = []
        self._short_description = ""
        self._long_description = ""
        self._parse()

    @property
    def components(self) -> List[DocComponent]:
        return self._components

    def find_component_by_type(self, *component_type: str) -> List[DocComponent]:
        result = []
        for component in self._components:
            if component.type in component_type:
                result.append(component)
                continue

        return result

    @property
    def short_description(self) -> str:
        return self._short_description

    @property
    def long_description(self) -> str:
        return self._long_description

    def _parse(self) -> None:
        parts = self.raw_doc.split("\n")
        description: List[str] = []
        components: List[DocComponent] = []

        for part in parts:  # type: str
            clean_part: str = part.strip()

            matches = DOC_COMPONENT_REGEX.match(clean_part)
            if matches:
                component = self._parse_component(matches)
                components.append(component)
                continue

            description.append(part)

        if description:
            self._long_description = "\n".join(description[1:]).strip("\n")
            self._short_description = description[0]
        self._components = components

    @staticmethod
    def _parse_component(matches: Match[str]) -> DocComponent:
        component_parts = matches[1].split(" ")
        if len(component_parts) > 1:
            return DocComponent(component_parts[0], component_parts[1:], matches[2].strip())
        else:
            return DocComponent(component_parts[0], [], matches[2].strip())
