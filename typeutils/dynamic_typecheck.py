from functools import wraps
from inspect import signature
from typing import Callable, List, Dict, Any, Tuple

AnyList = List[Any]
AnyDict = Dict[Any, Any]
AnyTuple = Tuple[Any, ...]
AnyCallable = Callable[..., Any]

_follow_wrapped = True


def _failure_handler(msg: str) -> None:
    raise ValueError(msg)


def configure_module():
    pass


def dynamic_typecheck(*, follow_wrapped: bool = _follow_wrapped):
    def _dynamic_typecheck_wrap(func: AnyCallable) -> AnyCallable:
        sig_args, sig_kwargs, sig_return = _get_signature(func, follow_wrapped)

        @wraps(func)
        def _typechecked_function_call(*args: AnyTuple, **kwargs: AnyDict) -> Any:
            _validate_all_args(sig_args, sig_kwargs, args, kwargs)
            val = func(*args, **kwargs)
            _check_return(sig_return, val)
            return val

        return _typechecked_function_call

    return _dynamic_typecheck_wrap


def _get_signature(func: AnyCallable, follow_wrapped: bool) -> Tuple[List[Any], Dict[str, Any], Any]:
    sig = signature(func, follow_wrapped=follow_wrapped)
    sig_args = [v for k, v in sig.parameters.items() if v.kind in (v.POSITIONAL_ONLY, v.POSITIONAL_OR_KEYWORD)]
    sig_kwargs = {k: v for k, v in sig.parameters.items() if v.kind in (v.KEYWORD_ONLY, v.POSITIONAL_OR_KEYWORD)}
    sig_return = sig.return_annotation
    return sig_args, sig_kwargs, sig_return


def _validate_all_args(sig_args: AnyList, sig_kwargs: AnyDict, args: AnyTuple, kwargs: AnyDict) -> None:
    for arg, sig_arg in zip(args, sig_args):
        _validate_type(arg, sig_arg.annotation)

    for key, kwarg in kwargs.items():
        sig_kwarg = sig_kwargs[key]
        _validate_type(kwarg, sig_kwarg.annotation)


def _check_return(sig_return: Any, value: Any) -> None:
    _validate_type(value, sig_return)


def _validate_type(value: Any, value_type: Any) -> None:
    # None is not a type, so we have to compare it to None directly instead of a type
    if value_type is None and value is None:
        return

    # Checks where value_type is of a primitive type like "int" or "str" - this behaves covariantly!
    if isinstance(value_type, type) and isinstance(value, value_type):
        return

    # Types can also be declared as strings in order to "forward-declare" them,
    # most often used for not-yet-imported custom classes
    if isinstance(value_type, str) and True:
        # The easiest check: Does the class name match up?
        # However, this approach always behaves invariantly (matches up with PEP-484 though)
        if type(value).__name__ == value_type:
            return
        # An alternative approach would be to parse the full class name, import it
        # and then compare the value to the imported class
        # Checking sys.modules does not help since the module might not be imported at that time

    _failure_handler(f"Return value {value} should be of type {value_type} but is {type(value)}")
