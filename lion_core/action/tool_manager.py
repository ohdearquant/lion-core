"""Defines the ToolManager class for managing tools in the system."""

from functools import singledispatchmethod
from typing import Any, Callable

from lion_core.libs import fuzzy_parse_json
from lion_core.abc.observer import Manager
from lion_core.libs import ucall, to_list
from .function_calling import FunctionCalling
from .tool import Tool, func_to_tool
from lion_core.communication.action_request import ActionRequest

ToolType = bool | Tool | str | list[Tool | str | dict[str, Any]] | dict[str, Any]


class ToolManager(Manager):
    """Manages tools in the system.

    Provides functionality to register tools, invoke them based on
    various input formats, and retrieve tool schemas.
    """

    def __init__(self, registry: dict[str, Tool] | None = None) -> None:
        """Initialize a new instance of ToolManager.

        Args:
            registry: Initial tool registry. Defaults to None.
        """
        self.registry: dict[str, Tool] = registry or {}

    def __contains__(self, tool: Tool | str | Callable[..., Any]) -> bool:
        """Check if a tool is registered.

        Args:
            tool: The tool to check for.

        Returns:
            bool: True if the tool is registered, False otherwise.
        """
        if isinstance(tool, Tool):
            return tool.function_name in self.registry
        elif isinstance(tool, str):
            return tool in self.registry
        elif callable(tool):
            return tool.__name__ in self.registry
        return False

    def register_tool(
        self, tool: Tool | Callable[..., Any], update: bool = False
    ) -> bool:
        """Register a single tool.

        Args:
            tool: The tool to register.
            update: Whether to update an existing tool. Defaults to False.

        Returns:
            bool: True if registration was successful.

        Raises:
            ValueError: If the tool is already registered and update is False.
            TypeError: If the provided tool is not a Tool object or callable.
        """
        if not update and tool in self:
            raise ValueError(
                f"Tool {getattr(tool, 'function_name', tool)} is already registered."
            )

        if callable(tool):
            tool = func_to_tool(tool)[0]
        if not isinstance(tool, Tool):
            raise TypeError("Please register a Tool object or callable.")

        self.registry[tool.function_name] = tool
        return True

    def register_tools(
        self, tools: list[Tool | Callable[..., Any]] | Tool | Callable[..., Any]
    ) -> bool:
        """Register multiple tools.

        Args:
            tools: The tools to register.

        Returns:
            bool: True if all tools were registered successfully.
        """
        tools_list = to_list(tools)
        print(tools_list)
        return all(self.register_tool(tool) for tool in tools_list)

    @singledispatchmethod
    def match_tool(self, func_call: Any) -> "FunctionCalling":
        raise TypeError(f"Unsupported type {type(func_call)}")

    @match_tool.register(tuple)
    def _(self, func_call: tuple) -> "FunctionCalling":
        if len(func_call) == 2:
            function_name = func_call[0]
            arguments = func_call[1]
            tool = self.registry.get(function_name)
            if not tool:
                raise ValueError(f"Function {function_name} is not registered.")
            return FunctionCalling(func_tool=tool, arguments=arguments)
        else:
            raise ValueError(f"Invalid function call {func_call}")

    @match_tool.register(dict)
    def _(self, func_call: dict[str, Any]) -> "FunctionCalling":
        if len(func_call) == 2 and ({"function", "arguments"} <= func_call.keys()):
            function_name = func_call["function"]
            tool = self.registry.get(function_name)
            if not tool:
                raise ValueError(f"Function {function_name} is not registered.")
            return FunctionCalling(func_tool=tool, arguments=func_call["arguments"])
        raise ValueError(f"Invalid function call {func_call}")

    @match_tool.register(ActionRequest)
    def _(self, func_call: ActionRequest) -> "FunctionCalling":
        tool = self.registry.get(func_call.function)
        if not tool:
            raise ValueError(f"Function {func_call.function} is not registered.")
        return FunctionCalling(func_tool=tool, arguments=func_call.arguments)

    @match_tool.register(str)
    def _(self, func_call: str) -> "FunctionCalling":
        _call = None
        try:
            _call = fuzzy_parse_json(func_call)
        except Exception as e:
            raise ValueError(f"Invalid function call {func_call}") from e

        if isinstance(_call, dict):
            return self.match_tool(_call)
        raise ValueError(f"Invalid function call {func_call}")

    async def invoke(self, func_call: Any):
        function_calling = self.match_tool(func_call)
        return await function_calling.invoke()

    @property
    def schema_list(self) -> list[dict[str, Any]]:
        """List all tool schemas currently registered in the ToolManager.

        Returns:
            list[dict[str, Any]]: List of tool schemas.
        """
        return [tool.schema_ for tool in self.registry.values()]

    def get_tool_schema(self, tools: ToolType = False, **kwargs) -> dict[str, Any]:
        """Retrieve the schema for specific tools or all tools.

        Args:
            tools: Specification of which tools to retrieve schemas for.
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, Any]: Tool schemas.
        """
        if isinstance(tools, bool) and tools is True:
            tool_kwarg = {"tools": self.schema_list}
        else:
            tool_kwarg = {"tools": self._get_tool_schema(tools)}
        return tool_kwarg | kwargs

    def _get_tool_schema(self, tool: Any) -> dict[str, Any] | list[dict[str, Any]]:
        """Retrieve the schema for a specific tool or list of tools.

        Args:
            tool: The tool or tools to retrieve schemas for.

        Returns:
            dict[str, Any] | list[dict[str, Any]]: Tool schema(s).

        Raises:
            ValueError: If a specified tool is not registered.
            TypeError: If an unsupported tool type is provided.
        """
        if isinstance(tool, dict):
            return tool
        elif isinstance(tool, Tool) or isinstance(tool, str):
            name = tool.function_name if isinstance(tool, Tool) else tool
            if name in self.registry:
                return self.registry[name].schema_
            raise ValueError(f"Tool {name} is not registered.")
        elif isinstance(tool, list):
            return [self._get_tool_schema(t) for t in tool]
        raise TypeError(f"Unsupported type {type(tool)}")


# File: lion_core/action/tool_manager.py
