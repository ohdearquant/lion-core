from typing_extensions import override
from lion_core.libs import validate_boolean
from lion_core.rule.base import Rule
from lion_core.exceptions import LionOperationError


class BooleanRule(Rule):
    """
    Rule for validating that a value is a boolean.

    Attributes:
        apply_type (str): The type of data to which the rule applies.
    """

    @override
    async def check_value(self, value, /) -> bool:
        if isinstance(value, bool):
            return value
        raise ValueError(f"Invalid boolean value.")

    @override
    async def fix_value(self, value) -> bool:
        try:
            return validate_boolean(value)
        except ValueError as e:
            raise LionOperationError(f"Failed to validate field: ") from e
