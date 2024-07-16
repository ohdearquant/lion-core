"""
Provide decorators to enhance function calls with various features.

This module offers the CallDecorator class with methods for retries,
throttling, concurrency limits, composition, and pre/post processing.
"""

import asyncio
from functools import wraps
from typing import Any, Callable, Sequence, TypeVar

from lion_core.libs.function_handlers._throttle import Throttle
from lion_core.libs.function_handlers._util import is_coroutine_func, force_async
from lion_core.libs.function_handlers._ucall import ucall
from lion_core.libs.function_handlers._rcall import rcall
from lion_core.setting import LN_UNDEFINED

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])
ErrorHandler = Callable[[Exception], None]


class CallDecorator:
    """
    A collection of decorators to enhance function calls with features
    like retries, throttling, concurrency limits, composition, and caching.
    """

    @staticmethod
    def retry(
        retries: int = 0,
        initial_delay: float = 0,
        delay: float = 0,
        backoff_factor: float = 1,
        default: Any = LN_UNDEFINED,
        timeout: float | None = None,
        timing: bool = False,
        verbose: bool = True,
        error_msg: str | None = None,
        error_map: dict[type, ErrorHandler] | None = None,
    ) -> Callable[[F], F]:
        """
        Decorator to automatically retry a function call on failure.

        Args:
            retries: Number of retry attempts.
            initial_delay: Initial delay before retrying.
            delay: Delay between retries.
            backoff_factor: Factor to increase delay after each retry.
            default: Default value to return on failure.
            timeout: Timeout for each function call.
            timing: If True, logs the time taken for each call.
            verbose: If True, logs the retries.
            error_msg: Custom error message on failure.
            error_map: A map of exception types to handler functions.

        Returns:
            The decorated function.
        """

        def decorator(func: F) -> F:
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                return await rcall(
                    func,
                    *args,
                    retries=retries,
                    initial_delay=initial_delay,
                    delay=delay,
                    backoff_factor=backoff_factor,
                    default=default,
                    timeout=timeout,
                    timing=timing,
                    verbose=verbose,
                    error_msg=error_msg,
                    error_map=error_map,
                    **kwargs,
                )

            return wrapper

        return decorator

    @staticmethod
    def throttle(period: float) -> Callable[[F], F]:
        """
        Decorator to limit the execution frequency of a function.

        Args:
            period: Minimum time in seconds between function calls.

        Returns:
            The decorated function.
        """

        def decorator(func: F) -> F:
            if not is_coroutine_func(func):
                func = force_async(func)
            throttle_instance = Throttle(period)

            @wraps(func)
            async def wrapper(*args, **kwargs):
                await throttle_instance(func)(*args, **kwargs)
                return await func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def max_concurrent(limit: int) -> Callable[[F], F]:
        """
        Decorator to limit the maximum number of concurrent executions.

        Args:
            limit: Maximum number of concurrent executions.

        Returns:
            The decorated function.
        """

        def decorator(func: F) -> F:
            if not is_coroutine_func(func):
                func = force_async(func)
            semaphore = asyncio.Semaphore(limit)

            @wraps(func)
            async def wrapper(*args, **kwargs):
                async with semaphore:
                    return await func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def compose(*functions: Callable[[T], T]) -> Callable[[F], F]:
        """
        Decorator to compose multiple functions, applying them in sequence.

        Args:
            functions: Functions to apply in sequence.

        Returns:
            The decorated function.
        """

        def decorator(func: F) -> F:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                value = await ucall(func, *args, **kwargs)
                for function in functions:
                    try:
                        value = await ucall(function, value)
                    except Exception as e:
                        raise ValueError(f"Error in function {function.__name__}: {e}")
                return value

            return async_wrapper

        return decorator

    @staticmethod
    def pre_post_process(
        preprocess: Callable[..., Any] | None = None,
        postprocess: Callable[..., Any] | None = None,
        preprocess_args: Sequence[Any] = (),
        preprocess_kwargs: dict[str, Any] = {},
        postprocess_args: Sequence[Any] = (),
        postprocess_kwargs: dict[str, Any] = {},
    ) -> Callable[[F], F]:
        """
        Decorator to apply pre-processing and post-processing functions.

        Args:
            preprocess: Function to apply before the main function.
            postprocess: Function to apply after the main function.
            preprocess_args: Arguments to pass to the preprocess function.
            preprocess_kwargs: Keyword arguments for the preprocess function.
            postprocess_args: Arguments to pass to the postprocess function.
            postprocess_kwargs: Keyword arguments for the postprocess function.

        Returns:
            The decorated function.
        """

        def decorator(func: F) -> F:

            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                preprocessed_args = (
                    [
                        await ucall(
                            preprocess, arg, *preprocess_args, **preprocess_kwargs
                        )
                        for arg in args
                    ]
                    if preprocess
                    else args
                )
                preprocessed_kwargs = (
                    {
                        k: await ucall(
                            preprocess, v, *preprocess_args, **preprocess_kwargs
                        )
                        for k, v in kwargs.items()
                    }
                    if preprocess
                    else kwargs
                )
                result = await ucall(func, *preprocessed_args, **preprocessed_kwargs)

                return (
                    await ucall(
                        postprocess, result, *postprocess_args, **postprocess_kwargs
                    )
                    if postprocess
                    else result
                )

            return async_wrapper

        return decorator


# Path: lion_core/libs/function_handlers/_call_decorator.py
