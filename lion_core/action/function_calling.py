"""
Copyright 2024 HaiyangLi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Any
from typing_extensions import override
from lion_core.libs import ucall
from lion_core.abc import ObservableAction

from lion_core.action.tool import Tool


class FunctionCalling(ObservableAction):
    """Represents a callable function with its arguments."""

    def __init__(
        self, func_tool: Tool, arguments: dict[str, Any] | None = None
    ) -> None:
        super().__init__()
        self.func_tool: Tool = func_tool
        self.arguments: dict[str, Any] = arguments or {}

    @override
    async def invoke(self) -> Any:
        """Asynchronously invoke the stored function with the arguments."""
        kwargs = self.arguments
        if self.func_tool.pre_processor:
            kwargs = await ucall(
                self.func_tool.pre_processor,
                self.arguments,
                **self.func_tool.pre_processor_kwargs,
            )
            if not isinstance(kwargs, dict):
                raise ValueError("Pre-processor must return a dictionary.")

        try:
            result = await ucall(
                self.func_tool.function,
                **kwargs,
            )
        except Exception:
            raise

        if self.func_tool.post_processor:
            post_process_kwargs = self.func_tool.post_processor_kwargs or {}
            result = await ucall(
                self.func_tool.post_processor,
                result,
                **post_process_kwargs,
            )

        return (
            result if self.func_tool.parser is None else self.func_tool.parser(result)
        )

    def __str__(self) -> str:
        return f"{self.func_tool.function_name}({self.arguments})"

    def __repr__(self) -> str:
        return (
            f"FunctionCalling(function={self.func_tool.function_name}, "
            f"arguments={self.arguments})"
        )


# File: lion_core/action/function_calling.py
