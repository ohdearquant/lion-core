from __future__ import annotations
from typing import Any, TypeVar, ClassVar, Type

from pydantic import Field, field_serializer, field_validator
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from lion_core.sys_util import SysUtil
from lion_core.setting import LN_UNDEFINED
from lion_core.exceptions import LionValueError
from lion_core.class_registry import LION_CLASS_REGISTRY
from lion_core.converter import ConverterRegistry, Converter
from .element import Element
from .note import Note


T = TypeVar("T", bound=Element)

DEFAULT_SERIALIZATION_INCLUDE: set[str] = {
    "metadata",
    "content",
    "ln_id",
    "timestamp",
    "extra_fields",
    "embedding",
}


class Component(Element):
    """Extended base class for components in the Lion framework."""

    metadata: Note = Field(
        default_factory=Note,
        description="Additional metadata for the component",
    )

    content: Any = Field(
        default=None,
        description="The main content of the Component",
    )

    embedding: list[float] = Field(default_factory=list)

    extra_fields: dict[str, Any] = Field(default_factory=dict)

    _converter_registry: ClassVar = ConverterRegistry

    @field_serializer("extra_fields")
    def _serialize_extra_fields(self, value: dict[str, FieldInfo]) -> dict[str, Any]:
        """Custom serializer for extra fields."""
        output_dict = {}
        for k in value.keys():
            k_value = self.__dict__.get(k)
            output_dict[k] = k_value
        return output_dict

    @field_validator("extra_fields")
    def _validate_extra_fields(cls, value: Any) -> dict[str, FieldInfo]:
        """Custom validator for extra fields."""
        if not isinstance(value, dict):
            raise LionValueError("Extra fields must be a dictionary")
        return {k: Field(**v) if isinstance(v, dict) else v for k, v in value.items()}

    @property
    def all_fields(self) -> dict[str, FieldInfo]:
        """
        Get all fields including model fields and extra fields.

        Returns:
            dict[str, FieldInfo]: A dictionary containing all fields.
        """
        return {**self.model_fields, **self.extra_fields}

    def add_field(
        self,
        name: str,
        value: Any = LN_UNDEFINED,
        annotation: Any = LN_UNDEFINED,
        field_obj: FieldInfo = LN_UNDEFINED,
        **kwargs,
    ) -> None:
        """
        Add a new field to the component's extra fields.

        Args:
            name: The name of the field to add.
            value: The value of the field. Defaults to `LN_UNDEFINED`.
            annotation: Type annotation for the field. Defaults to `LN_UNDEFINED`.
            field_obj: A pre-configured FieldInfo object. Defaults to `LN_UNDEFINED`.
            **kwargs: Additional keyword arguments for Field configuration.

        Raises:
            LionValueError: If the field already exists.
        """
        if name in self.all_fields:
            raise LionValueError(f"Field '{name}' already exists")

        self.update_field(
            name=name, value=value, annotation=annotation, field_obj=field_obj, **kwargs
        )

    def update_field(
        self,
        name: str,
        value: Any = LN_UNDEFINED,
        annotation: Any = LN_UNDEFINED,
        field_obj: FieldInfo | Any = LN_UNDEFINED,
        **kwargs,
    ) -> None:
        """
        Update an existing field or create a new one if it doesn't exist.

        Args:
            name: The name of the field to update or create.
            value: The new value for the field. Defaults to LN_UNDEFINED.
            annotation: Type annotation for the field. Defaults to LN_UNDEFINED.
            field_obj: A pre-configured FieldInfo object. Defaults to LN_UNDEFINED.
            **kwargs: Additional keyword arguments for Field configuration.

        Raises:
            ValueError: If both 'default' and 'default_factory' are provided in kwargs.
        """

        # pydanitc Field object cannot have both default and default_factory
        if "default" in kwargs and "default_factory" in kwargs:
            raise ValueError("Cannot provide both 'default' and 'default_factory'")

        # if passing kwargs
        if field_obj is LN_UNDEFINED:
            # check if field exists
            field_obj = self.all_fields.get(name, LN_UNDEFINED)

            if field_obj:  # existing field
                for k, v in kwargs.items():
                    setattr(field_obj, k, v)
            else:
                field_obj = Field(**kwargs)

        else:  # passing field_obj directly
            if not isinstance(field_obj, FieldInfo):
                raise ValueError(
                    "Invalid field_obj. It should be a pydantic FieldInfo object."
                )

        if annotation is not LN_UNDEFINED:
            field_obj.annotation = annotation
        if not field_obj.annotation:
            field_obj.annotation = Any

        self.extra_fields[name] = field_obj

        if value is not LN_UNDEFINED:
            value = SysUtil.copy(value)

        else:
            if getattr(self, name, LN_UNDEFINED) is not LN_UNDEFINED:
                value = getattr(self, name)

            elif getattr(field_obj, "default") is not PydanticUndefined:
                value = SysUtil.copy(field_obj.default)

            elif getattr(field_obj, "default_factory"):
                value = field_obj.default_factory()

            else:
                value = LN_UNDEFINED

        setattr(self, name, value)
        self._add_last_update(name)

    def _add_last_update(self, name: str) -> None:
        """
        Add or update the last update timestamp for a field.

        Args:
            name: The name of the field being updated.
        """
        current_time = SysUtil.time()
        self.metadata.set(["last_updated", name], current_time)

    def to_dict(self, **kwargs) -> dict:
        """
        Convert the component to a dictionary representation.

        Args:
            **kwargs: Additional arguments to pass to model_dump.

        Returns:
            dict[str, Any]: A dictionary representation of the component.
        """
        dict_ = self.model_dump(**kwargs)
        extra_fields = dict_.pop("extra_fields", {})
        dict_ = {**dict_, **extra_fields, "lion_class": self.class_name()}
        return dict_

    @classmethod
    def from_dict(
        cls, data: dict, include=DEFAULT_SERIALIZATION_INCLUDE, **kwargs
    ) -> T:
        """
        Create a component instance from a dictionary.

        Args:
            data: The dictionary containing component data.
            include: Fields to include in the reconstruction. Defaults to DEFAULT_SERIALIZATION_INCLUDE.
            **kwargs: Additional arguments for Pydantic model validation.

        Returns:
            T: An instance of the Component class or its subclass.
        """
        if "lion_class" in data:
            cls = LION_CLASS_REGISTRY.get(data.pop("lion_class"), cls)

        extra_fields = data.pop("extra_fields", {})
        d_ = {}

        for k, v in data.items():
            if not k in include:
                extra_fields[k] = v
            else:
                d_[k] = v

        d_["extra_fields"] = extra_fields
        return cls.model_validate(d_, **kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Custom attribute setter to handle extra fields and update timestamps.

        Args:
            name: The name of the attribute to set.
            value: The value to set.

        Raises:
            AttributeError: If attempting to directly assign to metadata.
        """
        if name == "metadata":
            raise AttributeError("Cannot directly assign to metadata.")
        if name in self.extra_fields:
            object.__setattr__(self, name, value)
        else:
            super().__setattr__(name, value)

        self._add_last_update(name)

    def __getattr__(self, name: str) -> Any:
        """
        Custom attribute getter to handle extra fields.

        Args:
            name: The name of the attribute to get.

        Returns:
            The value of the attribute.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        if name in self.extra_fields:
            return (
                self.extra_fields[name].default
                if self.extra_fields[name].default is not PydanticUndefined
                else LN_UNDEFINED
            )
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __str__(self) -> str:
        """Return a concise string representation of the component."""
        content_preview = str(self.content)[:50]
        if len(content_preview) == 50:
            content_preview += "..."

        return (
            f"{self.__class__.__name__}("
            f"ln_id={self.ln_id[:8]}..., "
            f"timestamp={str(self._created_datetime)[:-6]}, "
            f"content='{content_preview}', "
            f"metadata_keys={list(self.metadata.keys())}, "
            f"extra_fields_keys={list(self.extra_fields.keys())})"
        )

    def __repr__(self) -> str:
        """Return a detailed string representation of the component."""

        def truncate_dict(
            d: dict[str, Any], max_items: int = 5, max_str_len: int = 50
        ) -> dict[str, Any]:
            items = list(d.items())[:max_items]
            truncated = {
                k: (
                    v[:max_str_len] + "..."
                    if isinstance(v, str) and len(v) > max_str_len
                    else v
                )
                for k, v in items
            }
            if len(d) > max_items:
                truncated["..."] = f"({len(d) - max_items} more items)"
            return truncated

        content_repr = repr(self.content)
        if len(content_repr) > 100:
            content_repr = content_repr[:97] + "..."

        dict_ = self.model_dump()
        extra_fields = dict_.pop("extra_fields", {})

        return (
            f"{self.class_name()}("
            f"ln_id={repr(self.ln_id)}, "
            f"timestamp={str(self._created_datetime)[:-6]}, "
            f"content={content_repr}, "
            f"metadata={truncate_dict(self.metadata.content)}, "
            f"extra_fields={truncate_dict(extra_fields)})"
        )

    @classmethod
    def get_converter_registry(cls) -> ConverterRegistry:
        """
        Get the converter registry for the class.

        Returns:
            ConverterRegistry: The ConverterRegistry instance for the class.
        """
        if isinstance(cls._converter_registry, type):
            cls._converter_registry = cls._converter_registry()
        return cls._converter_registry

    def convert_to(self, key: str = "dict", /, **kwargs: Any) -> Any:
        """
        Convert the component to a specified type using the ConverterRegistry.

        Args:
            key: The key of the converter to use. Defaults to "dict".
            **kwargs: Additional keyword arguments for conversion.

        Returns:
            Any: The converted component in the specified type.
        """
        return self.get_converter_registry().convert_to(self, key, **kwargs)

    @classmethod
    def convert_from(cls, obj: Any, key: str = "dict", /, **kwargs) -> T:
        """
        Convert data to create a new component instance using the ConverterRegistry.

        Args:
            obj: The object to convert from.
            key: The key of the converter to use.
            **kwargs: Additional keyword arguments for conversion.

        Returns:
            T: A new instance of the Component class or its subclass.
        """
        data = cls.get_converter_registry().convert_from(cls, obj, key)
        return cls.from_dict(data, **kwargs)

    @classmethod
    def register_converter(cls, key: str, converter: Type[Converter]) -> None:
        """Register a new converter. Can be used for both a class and/or an instance."""
        cls.get_converter_registry().register(key, converter)


# File: lion_core/generic/component.py
