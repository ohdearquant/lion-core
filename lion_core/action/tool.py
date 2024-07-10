"""Defines the Tool class for callable tools with processing capabilities."""

import json
from typing import Any, Callable

from pydantic import Field, field_serializer

from lion_core.generic.component import Component
from lion_core.abc.element import Element
from lion_core.libs import function_to_schema, to_list


class Tool(Element):
    """Represents a callable tool with pre/post-processing capabilities.

    Encapsulates a function with its metadata, schema, and processing
    functions.

    Attributes:
        function: The callable function of the tool.
        schema_: Schema of the function in OpenAI format.
        pre_processor: Function to preprocess input arguments.
        pre_processor_kwargs: Keyword arguments for the pre-processor.
        post_processor: Function to post-process the result.
        post_processor_kwargs: Keyword arguments for the post-processor.
        parser: Function to parse the result to JSON serializable format.
    """

    function: Callable[..., Any] = Field(
        ...,
        description="The callable function of the tool.",
    )
    schema_: dict[str, Any] | None = Field(
        default=None,
        description="Schema of the function in OpenAI format.",
    )
    pre_processor: Callable[..., dict[str, Any]] | None = Field(
        default=None,
        description="Function to preprocess input arguments.",
    )
    pre_processor_kwargs: dict[str, Any] | None = Field(
        default=None,
        description="Keyword arguments for the pre-processor.",
    )
    post_processor: Callable[..., Any] | None = Field(
        default=None,
        description="Function to post-process the result.",
    )
    post_processor_kwargs: dict[str, Any] | None = Field(
        default=None,
        description="Keyword arguments for the post-processor.",
    )
    parser: Callable[[Any], Any] | None = Field(
        default=None,
        description="Function to parse result to JSON serializable format.",
    )

    def __init__(self, **data):
        """Initialize a Tool instance."""
        super().__init__(**data)
        if self.schema_ is None:
            self.schema_ = function_to_schema(self.function)

    @field_serializer(
        "function",
        "pre_processor",
        "post_processor",
        "parser",
        "pre_processor_kwargs",
        "post_processor_kwargs",
    )
    def serialize_field(self, v: Any) -> str | None:
        """Serialize various fields of the Tool class.

        Args:
            v: The value to serialize.

        Returns:
            Serialized representation of the value, or None if not applicable.
        """
        if callable(v):
            return v.__name__
        elif isinstance(v, dict):
            return json.dumps(v)
        return None

    @property
    def function_name(self) -> str:
        """Get the name of the function from the schema.

        Returns:
            str: The name of the function.
        """
        return self.schema_["function"]["name"]

    def __str__(self) -> str:
        """Return a string representation of the Element.

        Returns:
            str: A string representation of the Element.
        """
        timestamp_str = self.timestamp.isoformat(timespec="minutes")
        return (
            f"{self.class_name()}(ln_id={self.ln_id[:6]}.., "
            f"timestamp={timestamp_str}), "
            f"schema_={json.dumps(self.schema_, indent=4)}"
        )


def func_to_tool(
    func_: Callable[..., Any] | list[Callable[..., Any]],
    parser: Callable[[Any], Any] | list[Callable[[Any], Any]] | None = None,
    docstring_style: str = "google",
    **kwargs,
) -> list[Tool]:
    """Convert functions to Tool objects.

    Args:
        func_: The function(s) to convert into tool(s).
        parser: Parser(s) to associate with the function(s).
        docstring_style: The style of the docstring parser to use.
        **kwargs: Additional keyword arguments for the Tool constructor.

    Returns:
        A list of Tool objects created from the provided function(s).

    Raises:
        ValueError: If the length of parsers doesn't match the functions.
    """
    funcs = to_list(func_)
    parsers = to_list(parser)

    if parser and len(funcs) != len(parsers):
        raise ValueError("Length of parser must match length of func, ")

    tools = []
    for idx, func in enumerate(funcs):
        tool = Tool(
            function=func,
            schema_=function_to_schema(func, style=docstring_style),
            parser=parsers[idx] if parser else None,
            **kwargs,
        )
        tools.append(tool)

    return tools


# File: lion_core/action/tool.py
