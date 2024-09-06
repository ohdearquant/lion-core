# AssistantResponse API Reference

## Class Hierarchy

<antArtifact identifier="assistant-response-class-hierarchy" type="application/vnd.ant.mermaid" title="AssistantResponse Class Hierarchy">
classDiagram
    RoledMessage <|-- AssistantResponse

    class RoledMessage {
        +Note content
        +MessageRole role
        +str sender
        +str recipient
    }

    class AssistantResponse {
        +Any response
        +__init__(assistant_response, sender, recipient)
    }


## AssistantResponse

`AssistantResponse` represents a response from an assistant in the system. It inherits from `RoledMessage` and encapsulates the content of the assistant's response.

### Attributes

Inherits all attributes from `RoledMessage`.

- `content` (Note): Contains the assistant response details.

### Properties

- `response` (Any): The content of the assistant's response.

### Methods

#### `__init__(self, assistant_response: dict | MessageFlag, sender: Any | MessageFlag, recipient: Any | MessageFlag, protected_init_params: dict | None = None) -> None`

Initializes an AssistantResponse instance.

Args:
- `assistant_response`: The content of the assistant's response.
- `sender`: The sender of the response, typically the assistant.
- `recipient`: The recipient of the response.
- `protected_init_params`: Optional parameters for protected initialization.

#### `response(self) -> Any`

Get the assistant response content.

Returns:
- The content of the assistant's response.

### Usage Example

```python
from lion_core.communication.assistant_response import AssistantResponse

# Create an assistant response
assistant_response = AssistantResponse(
    assistant_response="This is the assistant's response to the user's query.",
    sender="assistant_id",
    recipient="user_id"
)

# Access the response content
print(assistant_response.response)
# Output: "This is the assistant's response to the user's query."

# Create an assistant response with a structured content
structured_response = AssistantResponse(
    assistant_response={
        "content": "Structured response",
        "additional_info": {
            "confidence": 0.95,
            "sources": ["source1", "source2"]
        }
    },
    sender="assistant_id",
    recipient="user_id"
)

# Access the structured response content
print(structured_response.response)
# Output: {"content": "Structured response", "additional_info": {...}}
```

This AssistantResponse class provides a flexible way to represent responses from an AI assistant within the system. It can handle both simple string responses and more complex structured responses, allowing for rich interactions between the assistant and users.

### Notes

- The `assistant_response` parameter in the constructor can be either a string or a dictionary. If it's a string, it will be wrapped in a dictionary with a "content" key. If it's a dictionary without a "content" key, the entire dictionary will be treated as the content.
- The `response` property returns the content of the assistant's response, which can be a string or a more complex structure, depending on how the response was initialized.
- AssistantResponse uses the `ASSISTANT` role from the `MessageRole` enum, distinguishing it from other types of messages in the system.
