# Executor API Reference

## Class Hierarchy

<antArtifact identifier="executor-class-hierarchy" type="application/vnd.ant.mermaid" title="Executor Class Hierarchy">
classDiagram
    AbstractObserver <|-- BaseExecutor
    BaseExecutor <|-- ActionExecutor

    class AbstractObserver {
        <<abstract>>
    }

    class BaseExecutor {
        +type[BaseProcessor] processor_class
        +bool strict
        +create_processor()
        +start()
        +stop()
        +forward()*
    }

    class ActionExecutor {
        +Pile[ObservableAction] pile
        +Progression pending
        +ActionProcessor processor
        +pending_action Pile
        +completed_action Pile
        +append(action: ObservableAction)
        +forward()
    }


## BaseExecutor

`BaseExecutor` is an abstract base class for executing tasks with a processor.

### Attributes

- `processor_class` (type[BaseProcessor]): The class of processor to use.
- `strict` (bool): Whether to enforce strict type checking.
- `processor_config` (dict): Configuration parameters for initializing the processor.

### Methods

#### `__init__(self, **kwargs: Any) -> None`

Initializes the BaseExecutor with the provided configuration.

#### `@abstractmethod async forward(self, *args: Any, **kwargs: Any) -> Any`

Abstract method to move onto the next step.

#### `async create_processor(self) -> None`

Factory method for processor creation.

#### `async start(self) -> None`

Starts the event processor.

#### `async stop(self) -> None`

Stops the event processor.

## ActionExecutor

`ActionExecutor` is a concrete implementation of BaseExecutor for managing and processing actions.

### Attributes

Inherits all attributes from BaseExecutor.

- `pile` (Pile[ObservableAction]): A collection of actions managed by the executor.
- `pending` (Progression): A progression tracking the pending actions.
- `processor` (ActionProcessor): The action processor instance.

### Methods

Inherits all methods from BaseExecutor.

#### `__init__(self, **kwargs: Any) -> None`

Initializes the ActionExecutor with the provided configuration.

#### `@property pending_action(self) -> Pile`

Retrieves a pile of all pending actions.

#### `@property completed_action(self) -> Pile`

Retrieves a pile of all completed actions.

#### `async append(self, action: ObservableAction) -> None`

Appends a new action to the executor.

#### `async forward(self) -> None`

Forwards pending actions to the processor.

#### `__contains__(self, action: ObservableAction | str) -> bool`

Checks if an action is present in the pile.

#### `__iter__(self) -> Iterator[ObservableAction]`

Returns an iterator over the actions in the pile.
