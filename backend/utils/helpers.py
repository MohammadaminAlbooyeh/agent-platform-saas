import time
import functools
import logging
from typing import Any, Callable

logger = logging.getLogger("neural_search")


def timer_decorator(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} took {elapsed * 1000:.1f}ms")
        return result

    return wrapper


def chunk_list(lst: list, chunk_size: int):
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


def truncate_text(text: str, max_chars: int = 200) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."
