"""Mail module for the Lion framework's communication system."""

from typing import Any
from pydantic import Field, field_validator
from lion_core.exceptions import LionValueError
from lion_core.communication.base import BaseMail
from lion_core.communication.package import PackageCategory, Package


class Mail(BaseMail):
    """a mail component with sender, recipient, and package."""

    sender: str = Field(
        ...,
        title="Sender",
        description="The ID of the sender node, or 'system', 'user', "
        "or 'assistant'.",
    )

    recipient: str = Field(
        ...,
        title="Recipient",
        description="The ID of the recipient node, or 'system', 'user', "
        "or 'assistant'.",
    )

    package: Package = Field(
        ...,
        title="Package",
        description="The package to be delivered.",
    )

    @property
    def category(self) -> PackageCategory:
        """Return the category of the package."""
        return self.package.category

    @field_validator("sender", "recipient", mode="before")
    @classmethod
    def _validate_sender_recipient(cls, value: Any) -> str:
        """Validate the sender and recipient fields."""
        value = super()._validate_sender_recipient(value)
        if value == "N/A":
            raise LionValueError(f"Invalid sender or recipient for Mail")
        return value


# File: lion_core/communication/mail.py
