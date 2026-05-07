"Create type hints dynamically with ease"

__version__ = "0.0.3"

from .codegen import Codegen
from .errors import TypegenFailureWarning

__all__ = [
    "Codegen",
    "TypegenFailureWarning",
]
