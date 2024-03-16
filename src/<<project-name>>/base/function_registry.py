from typing import Callable, Any, Tuple


class FunctionRegistry:
    """Registry of callables to register with any depth of strings.
    For example, each dataset/model pair.

    Maintains an internal mapping of callables in the form
    {keys[0]: {keys[n]: Callable}}. cls.register() will wrap functions to enable
    dynamic loading based on configurations.
    """

    _registry = None

    @classmethod
    def register(cls, *args, **kwargs) -> Callable:
        """Decorator to register decorated function in a function registry.

        Args:
            keys (Tuple[str]): tuple of keys to nest into the registry.

        Returns:
            Callable: Wrapped function after adding to registry.
        """

        def wrapper(fn: Callable) -> Callable:
            """Wrapper for callable used to populate cls._registry.

            Args:
                fn (Callable): Function to wrap

            Returns:
                Callable: Original function after registration.
            """
            keys = args + tuple(kwargs.values())
            if args not in cls._registry:
                cls._registry[keys] = fn
                cls._logger.debug(
                    f"Registered {fn.__name__} in {cls.__name__} "
                    f"registry for {args}..."
                )
            return fn

        return wrapper

    @classmethod
    def call(cls, keys: Tuple[str], *args, **kwargs) -> Any:
        """Calls function registry for dataset/model with *args and **kwargs.

        If dataset not registered, will raise error. If dataset/model not
        registered, will return dataset/_DEFAULT, which is the first callable
        added to this registry.

        Args:
            dataset (str): Dataset name
            model (str): Model name
        Returns:
            Any: The object returned by the function loaded from registry.
        Raises:
            ValueError: If dataset not found in registry.
        """
        if keys not in cls._registry:
            raise ValueError(
                f"No registry entry in {cls.__name__} for key {keys}"
            )
        cls._logger.debug(
            f"Calling {cls._registry[keys].__name__} from "
            f"{cls.__name__} for registry entry {keys} with args: "
            f"{args} and kwargs: {kwargs}"
        )
        return cls._registry[keys](*args, **kwargs)
