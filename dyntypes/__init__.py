"Create type hints dynamically with ease"

__version__ = "1.0.2"

from .codegen import Codegen
from .errors import TypegenFailureWarning

__all__ = [
    "Codegen",
    "TypegenFailureWarning",
]
