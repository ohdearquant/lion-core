# Instruction API Reference

## Class Hierarchy

<antArtifact identifier="instruction-class-hierarchy" type="application/vnd.ant.mermaid" title="Instruction Class Hierarchy">
classDiagram
    RoledMessage <|-- Instruction

    class RoledMessage {
        +Note content
        +MessageRole role
        +str sender
        +str recipient
    }

    class Instruction {
        +str guidance
        +str instruction
        +__init__(instruction, context, guidance, images, sender, recipient, request_fields, image_detail)
        +update_images(images, image_detail)
        +update_guidance(guidance)
        +update_request_fields(request_fields)
        +update_context(*args, **kwargs)
        +_format_content()
        +from_form(form, sender, recipient, images, image_detail, strict, assignment, task_description, fill_inputs, none_as_valid_value, input_value_kwargs)
    }


## Instruction

`Instruction` represents an instruction message in the system. It inherits from `RoledMessage` and encapsulates details of an instruction, including guidance, context, and request fields.

### Attributes

Inherits all attributes from `RoledMessage`.

- `content` (Note): Contains the instruction details, including guidance, instruction text, context, images, and request fields.

### Properties

- `guidance` (str | None): The guidance content of the instruction.
- `instruction` (str): The main instruction content.

### Methods

#### `__init__(self, instruction: Any | MessageFlag, context: Any | MessageFlag = None, guidance: Any | MessageFlag = None, images: list | MessageFlag = None, sender: Any | MessageFlag = None, recipient: Any | MessageFlag = None, request_fields: dict | MessageFlag = None, image_detail: Literal["low", "high", "auto"] | MessageFlag = None, protected_init_params: dict | None = None) -> None`

Initializes an Instruction instance.

#### `update_images(self, images: list | str, image_detail: Literal["low", "high", "auto"] = None) -> None`

Add new images and update the image detail level.

#### `update_guidance(self, guidance: str) -> None`

Update the guidance content of the instruction.

#### `update_request_fields(self, request_fields: dict) -> None`

Update the requested fields in the instruction.

#### `update_context(self, *args, **kwargs) -> None`

Add new context to the instruction.

#### `_format_content(self) -> dict[str, Any]`

Format the content of the instruction.

#### `@classmethod from_form(cls, *, form: BaseForm | type[Form], sender: str | None = None, recipient: Any = None, images: str | None = None, image_detail: str | None = None, strict: bool = None, assignment: str = None, task_description: str = None, fill_inputs: bool = True, none_as_valid_value: bool = False, input_value_kwargs: dict = None) -> "Instruction"`

Create an Instruction instance from a form.

### Helper Functions

#### `prepare_request_response_format(request_fields: dict) -> str`

Prepare the format for request response.

#### `format_image_content(text_content: str, images: list, image_detail: Literal["low", "high", "auto"]) -> dict[str, Any]`

Format text content with images for message content.

#### `prepare_instruction_content(guidance: str | None = None, instruction: str | None = None, context: str | dict | list | None = None, request_fields: dict | None = None, images: str | list | None = None, image_detail: Literal["low", "high", "auto"] | None = None) -> Note`

Prepare the content for an instruction message.

### Usage Example

```python
from lion_core.communication.instruction import Instruction

# Create a basic instruction
instruction = Instruction(
    instruction="Perform task X",
    context="Context for task X",
    guidance="Guidance for performing task X",
    sender="user_id",
    recipient="assistant_id"
)

# Access properties
print(instruction.instruction)  # Output: "Perform task X"
print(instruction.guidance)  # Output: "Guidance for performing task X"

# Update the instruction
instruction.update_guidance("Updated guidance for task X")
instruction.update_context(additional_info="This is additional context")
instruction.update_images(["image1.jpg", "image2.jpg"], image_detail="high")

# Create an instruction from a form
from lion_core.form import Form

class TaskForm(Form):
    task_name: str
    task_description: str

form_instance = TaskForm(task_name="Task Y", task_description="Description of Task Y")
form_instruction = Instruction.from_form(
    form=form_instance,
    sender="user_id",
    recipient="assistant_id"
)

print(form_instruction.instruction)  # Output will depend on the Form's instruction_dict
```

This Instruction class provides a flexible way to represent instruction messages within the system. It can handle various types of content, including text instructions, guidance, context, images, and form-based instructions. The class offers methods to update different aspects of the instruction, making it adaptable to changing requirements during a conversation or task execution.

### Notes

- The `Instruction` class uses the `USER` role from the `MessageRole` enum, indicating that instructions typically come from the user side of the conversation.
- The `from_form` class method allows creation of instructions directly from Form objects, facilitating integration with form-based workflows.
- Image handling includes support for multiple images and different detail levels, useful for instructions that require visual context.
- The `update_context` method allows for flexible addition of context, supporting both positional and keyword arguments.
