from typing import Any

from pydantic import BaseModel, Field

from lion_core.abc._characteristic import Real
from lion_core.abc._concept import AbstractElement
from lion_core.sys_utils import SysUtil


class RealElement(BaseModel, AbstractElement, Real):
    """Base class in the Lion framework."""

    ln_id: str = Field(
        default_factory=SysUtil.id,
        title="Lion ID",
        description="Unique identifier for the element",
        frozen=True,
    )

    timestamp: float = Field(
        default_factory=lambda: SysUtil.time(type_="timestamp"),
        title="Creation Timestamp",
        frozen=True,
        alias="created",
    )

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict, /, **kwargs) -> "RealElement":
        return cls.model_validate(data, **kwargs)
