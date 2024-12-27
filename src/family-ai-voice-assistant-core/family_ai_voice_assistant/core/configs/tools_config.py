from dataclasses import dataclass
from typing import List

from .config import Config


@dataclass
class ToolsConfig(Config):

    # list of packages to be included
    packages: List[str] = None

    # if include_functions and exclude_functions are both None,
    # all @tool_function will be included
    include_functions: List[str] = None
    exclude_functions: List[str] = None
