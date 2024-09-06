# ActionResponse API Reference

## Class Hierarchy

<antArtifact identifier="action-response-class-hierarchy" type="application/vnd.ant.mermaid" title="ActionResponse Class Hierarchy">
classDiagram
    RoledMessage <|-- ActionResponse

    class RoledMessage {
        +Note content
        +MessageRole role
        +str sender
        +str recipient
    }

    class ActionResponse {
        +Any func_output
        +dict response_dict
        +str action_request_id
        +__init__(action_request, sender, func_output)
        +update_request(action_request, func_output)
    }


## ActionResponse

`ActionResponse` represents a response to an action request in the system. It inherits from `RoledMessage` and encapsulates the details of a function call response.

### Attributes

Inherits all attributes from `RoledMessage`.

- `content` (Note): Contains the action response details.

### Properties

- `func_output` (Any): The function output from the action response.
- `response_dict` (dict[str, Any]): The action response as a dictionary.
- `action_request_id` (str | None): The ID of the corresponding action request.

### Methods

#### `__init__(self, action_request: ActionRequest | MessageFlag, sender: Any | MessageFlag, func_output: Any | MessageFlag, protected_init_params: dict | None = None) -> None`

Initializes an ActionResponse instance.

Args:
- `action_request`: The original action request to respond to.
- `sender`: The sender of the action response.
- `func_output`: The output from the function in the request.
- `protected_init_params`: Protected initialization parameters.

#### `func_output(self) -> Any`

Get the function output from the action response.

Returns:
- The function output.

#### `response_dict(self) -> dict[str, Any]`

Get the action response as a dictionary.

Returns:
- The action response dictionary.

#### `action_request_id(self) -> str | None`

Get the ID of the corresponding action request.

Returns:
- The ID of the corresponding action request.

#### `update_request(self, action_request: ActionRequest, func_output: Any) -> None`

Update the action response with new request and output.

Args:
- `action_request`: The original action request being responded to.
- `func_output`: The output from the function in the request.

### Helper Functions

#### `prepare_action_response_content(action_request: ActionRequest, func_output: Any) -> Note`

Prepares the content for an action response.

Args:
- `action_request`: The original action request.
- `func_output`: The output from the function.

Returns:
- A Note object containing the prepared action response.

Raises:
- `LionValueError`: If the action request has already been responded to.

### Usage Example

```python
from lion_core.communication.action_request import ActionRequest
from lion_core.communication.action_response import ActionResponse

# Assume we have an existing action_request
action_request = ActionRequest(
    func="example_function",
    arguments={"arg1": "value1", "arg2": 42},
    sender="user_id",
    recipient="system_id"
)

# Create an action response
action_response = ActionResponse(
    action_request=action_request,
    sender="system_id",
    func_output="Function execution result"
)

# Access properties
print(action_response.func_output)  # Output: "Function execution result"
print(action_response.action_request_id)  # Output: [ID of the action_request]

# Update the response
action_response.update_request(action_request, "Updated result")
print(action_response.func_output)  # Output: "Updated result"
```

This ActionResponse class provides a structured way to represent and manage responses to action requests within the system. It encapsulates the function output, links back to the original request, and allows for updating the response if needed.
