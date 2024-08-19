from typing import Any
from pydantic import Field
from lion_core.abc import Action
from lion_core.generic.log import BaseLog
from lion_core.generic.element import Element
from lion_core.action.status import ActionStatus
from lion_core.log_manager import log_manager


class ObservableAction(Element, Action):
    """
    Represents an action that can be observed, with a trackable status.

    The `ObservableAction` class extends `Action` and `Element` to provide a
    structure for actions whose status can be monitored. It includes a status
    field to indicate the current state of the action, and a request property
    that can be used to check for permission before the action is performed.

    Attributes:
        status (ActionStatus): The current status of the action. Defaults to `ActionStatus.PENDING`.

    Properties:
        request (dict): A dictionary representing the request for permission to perform the action, if any.
    """

    status: ActionStatus = ActionStatus.PENDING
    execution_time: float = None
    response: Any = None
    error: str = None
    retry_config: dict = Field(default_factory=dict, exclude=True)
    content_fields: list = ["response"]

    def __init__(self, retry_config: dict = None):
        super().__init__()
        self.retry_config = retry_config or {}

    @property
    def request(self) -> dict:
        """
        The request to get permission for, if any.

        This property returns a dictionary representing the request for
        permission before the action is performed. It can be overridden in
        subclasses to provide specific request details.

        Returns:
            dict: A dictionary containing the request details.
        """
        return {}

    async def to_log(self) -> BaseLog:
        try:
            log_ = self._to_log()
            await log_manager.alog(log_)
            return log_
        finally:
            del self

    def _to_log(self) -> BaseLog:
        dict_ = super().to_dict()
        content = {k: dict_[k] for k in self.content_fields if k in dict_}
        loginfo = {k: dict_[k] for k in dict_ if k not in self.content_fields}
        return BaseLog(content=content, loginfo=loginfo)
