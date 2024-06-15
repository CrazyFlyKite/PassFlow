from random import choice
from typing import Optional, Final

from GlobalKit import english, digits

# Window
PAGE_TITLE: Final[str] = 'Pass Flow'
PAGE_WIDTH: Final[int] = 400
PAGE_HEIGHT: Final[int] = 500
PAGE_RESIZABLE: Final[bool] = False

# Other
DEFAULT_LENGTH: Final[int] = 12
MAX_LENGTH: Final[int] = 10 ** 5


# Functions
def generate_password(length: int, lowercase: Optional[bool] = True, uppercase: Optional[bool] = True,
                      numbers: Optional[bool] = True, special: Optional[bool] = True) -> Optional[str]:
	characters: str = ''
	characters += english.full_lowercase if lowercase else ''
	characters += english.full_uppercase if uppercase else ''
	characters += digits if numbers else ''
	characters += '*%$&@:;/,._+!?' if special else ''

	return None if not characters else ''.join(choice(characters) for _ in range(length))
