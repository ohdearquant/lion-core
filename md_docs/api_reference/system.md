# System API Reference

## Class Hierarchy

<antArtifact identifier="system-class-hierarchy" type="application/vnd.ant.mermaid" title="System Class Hierarchy">
classDiagram
    RoledMessage <|-- System

    class RoledMessage {
        +Note content
        +MessageRole role
        +str sender
        +str recipient
    }

    class System {
        +Any system_info
        +__init__(system, sender, recipient, system_datetime)
    }


## System

`System` represents a system message in a language model conversation. It inherits from `RoledMessage` and encapsulates system-level instructions or information.

### Attributes

Inherits all attributes from `RoledMessage`.

- `content` (Note): Contains the system message details.

### Properties

- `system_info` (Any): The system information stored in the message content.

### Methods

#### `__init__(self, system: Any | MessageFlag = None, sender: str | None | MessageFlag = None, recipient: str | None | MessageFlag = None, system_datetime: bool | str | None | MessageFlag = None, protected_init_params: dict | None = None) -> None`

Initializes a System message instance.

Args:
- `system`: The system message content.
- `sender`: The sender of the system message (default is "system").
- `recipient`: The recipient of the system message (default is "N/A").
- `system_datetime`: Boolean, string, or None to indicate whether to include datetime information.
- `protected_init_params`: Protected initialization parameters.

### Helper Functions

#### `format_system_content(system_datetime: bool | str | None, system_message: str) -> Note`

Format the system content with optional datetime information.

Args:
- `system_datetime`: Boolean, string, or None to indicate whether to include datetime information.
- `system_message`: The main system message content.

Returns:
- A Note object containing the formatted system content.

### Constants

- `DEFAULT_SYSTEM` (str): A default system message used when no specific message is provided.

### Usage Example

```python
from lion_core.communication.system import System

# Create a basic system message
system_message = System(
    system="You are a helpful AI assistant. Be concise and clear in your responses.",
    sender="system",
    recipient="assistant_id",
    system_datetime=True
)

# Access the system info
print(system_message.system_info)
# Output: "You are a helpful AI assistant. Be concise and clear in your responses. System Date: [current date and time]"

# Create a system message with a custom datetime string
custom_datetime_message = System(
    system="This is a custom dated system message.",
    system_datetime="2023-06-01 10:00:00"
)

print(custom_datetime_message.system_info)
# Output: "This is a custom dated system message. Date: 2023-06-01 10:00:00"

# Create a system message without datetime
no_datetime_message = System(
    system="This is a system message without date information.",
    system_datetime=False
)

print(no_datetime_message.system_info)
# Output: "This is a system message without date information."
```

This System class provides a way to represent system-level messages within a conversation. It's particularly useful for setting up the initial context or providing ongoing guidance to an AI model during a conversation.

### Notes

- The `System` class uses the `SYSTEM` role from the `MessageRole` enum, distinguishing it from user or assistant messages.
- The `system_datetime` parameter allows flexible handling of date and time information:
  - If `True`, it includes the current date and time.
  - If a string is provided, it uses that string as the date information.
  - If `False` or `None`, no date information is included.
- When no system message is provided, it uses a default message defined by `DEFAULT_SYSTEM`.
- The class supports the message flag system for cloning and loading, consistent with other message types in the framework.
