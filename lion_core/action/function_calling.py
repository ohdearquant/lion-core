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
from lion_core.libs import ucall, CallDecorator as cd
from lion_core.action.base import ObservableAction

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
    async def invoke(self):

        @cd.pre_post_process(
            preprocess=self.func_tool.pre_processor,
            postprocess=self.func_tool.post_processor,
            preprocess_kwargs=self.func_tool.pre_processor_kwargs,
            postprocess_kwargs=self.func_tool.post_processor_kwargs,
        )
        async def _inner(**kwargs):
            return await ucall(self.func_tool.function, **kwargs)

        result = await _inner(**self.arguments)
        if self.func_tool.parser is not None:
            return self.func_tool.parser(result)
        return result

    def __str__(self) -> str:
        return f"{self.func_tool.function_name}({self.arguments})"

    def __repr__(self) -> str:
        return (
            f"FunctionCalling(function={self.func_tool.function_name}, "
            f"arguments={self.arguments})"
        )


# File: lion_core/action/function_calling.py
