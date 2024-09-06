# Processor API Reference

## Class Hierarchy

<antArtifact identifier="processor-class-hierarchy" type="application/vnd.ant.mermaid" title="Processor Class Hierarchy">
classDiagram
    AbstractObserver <|-- BaseProcessor
    BaseProcessor <|-- ActionProcessor

    class AbstractObserver {
        <<abstract>>
    }

    class BaseProcessor {
        +int capacity
        +float refresh_time
        +Queue queue
        +Event _stop_event
        +int available_capacity
        +bool execution_mode
        +enqueue(event: Event)
        +dequeue() Event
        +join()
        +stop()
        +start()
        +is_stopped() bool
        +create(**kwargs) BaseProcessor
        +process()*
        +request_permission(**kwargs) bool
        +execute()
    }

    class ActionProcessor {
        +type observation_type
        +process()
    }


## BaseProcessor

`BaseProcessor` is an abstract base class for processing events in the Lion framework.

### Attributes

- `capacity` (int): Maximum number of events processed concurrently.
- `refresh_time` (float): Time interval between processing cycles.
- `queue` (asyncio.Queue): Queue holding events to be processed.
- `_stop_event` (asyncio.Event): Event to signal stopping the processing.
- `available_capacity` (int): The remaining processing capacity.
- `execution_mode` (bool): Flag indicating if processor is executing.

### Methods

#### `__init__(self, capacity: int, refresh_time: float) -> None`

Initializes a BaseProcessor instance.

#### `async enqueue(self, event: Event) -> None`

Enqueues an event to the processor queue.

#### `async dequeue(self) -> Event`

Dequeues an event from the processor queue.

#### `async join(self) -> None`

Blocks until all items in the queue have been processed.

#### `async stop(self) -> None`

Signals the processor to stop processing events.

#### `async start(self) -> None`

Allows the processor to start or continue processing.

#### `is_stopped(self) -> bool`

Indicates whether the processor has been stopped.

#### `@classmethod async create(cls, **kwargs: Any) -> BaseProcessor`

Class method to create an instance of the processor.

#### `@abstractmethod async process(self) -> None`

Abstract method to process events.

#### `async request_permission(self, **kwargs: Any) -> bool`

Placeholder method to request permission before processing an event.

#### `async execute(self) -> None`

Executes the processor, continuously processing events until stopped.

## ActionProcessor

`ActionProcessor` is a concrete implementation of BaseProcessor for processing actions.

### Attributes

Inherits all attributes from BaseProcessor.

- `observation_type` (type): Set to ObservableAction.

### Methods

Inherits all methods from BaseProcessor.

#### `async process(self) -> None`

Processes the work items in the queue. It processes items up to the available capacity, marking each action as `PROCESSING` before execution. After processing, the capacity is reset.
