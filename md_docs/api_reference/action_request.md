# ActionRequest API Reference

## Class Hierarchy

<antArtifact identifier="action-request-class-hierarchy" type="application/vnd.ant.mermaid" title="ActionRequest Class Hierarchy">
classDiagram
    RoledMessage <|-- ActionRequest

    class RoledMessage {
        +Note content
        +MessageRole role
        +str sender
        +str recipient
    }

    class ActionRequest {
        +str action_response_id
        +bool is_responded
        +dict request_dict
        +dict arguments
        +str function
        +__init__(func, arguments, sender, recipient)
    }


## ActionRequest

`ActionRequest` represents a request for an action in the system. It inherits from `RoledMessage` and encapsulates the details of a function call request.

### Attributes

Inherits all attributes from `RoledMessage`.

- `content` (Note): Contains the action request details.

### Properties

- `action_response_id` (str | None): The ID of the corresponding action response, if any.
- `is_responded` (bool): Indicates if the action request has been responded to.
- `request_dict` (dict[str, Any]): The action request content as a dictionary.
- `arguments` (dict[str, Any]): The arguments for the action request.
- `function` (str): The function name for the action request.

### Methods

#### `__init__(self, func: str | Callable | MessageFlag, arguments: dict | MessageFlag, sender: Any | MessageFlag, recipient: Any | MessageFlag, protected_init_params: dict | None = None) -> None`

Initializes an ActionRequest instance.

Args:
- `func`: The function to be invoked.
- `arguments`: The arguments for the function.
- `sender`: The sender of the request.
- `recipient`: The recipient of the request.
- `protected_init_params`: Protected initialization parameters.

#### `action_response_id(self) -> str | None`

Get the ID of the corresponding action response, if any.

Returns:
- The ID of the action response, or None if not responded.

#### `is_responded(self) -> bool`

Check if the action request has been responded to.

Returns:
- True if the action request has been responded to, else False.

#### `request_dict(self) -> dict[str, Any]`

Get the action request content as a dictionary.

Returns:
- The action request content.

#### `arguments(self) -> dict[str, Any]`

Get the arguments for the action request.

Returns:
- The arguments for the action request.

#### `function(self) -> str`

Get the function name for the action request.

Returns:
- The function name for the action request.

### Helper Functions

#### `prepare_action_request(func: str | Callable, arguments: dict) -> Note`

Prepares the content for an action request.

Args:
- `func`: The function to be invoked.
- `arguments`: The arguments for the function.

Returns:
- A Note object containing the prepared action request.

### Usage Example

```python
from lion_core.communication.action_request import ActionRequest

# Create an action request
action_request = ActionRequest(
    func="example_function",
    arguments={"arg1": "value1", "arg2": 42},
    sender="user_id",
    recipient="system_id"
)

# Access properties
print(action_request.function)  # Output: "example_function"
print(action_request.arguments)  # Output: {"arg1": "value1", "arg2": 42}
print(action_request.is_responded)  # Output: False
```

This ActionRequest class provides a structured way to represent and manage action requests within the system, encapsulating the function name, arguments, and metadata related to the request's status and response.
