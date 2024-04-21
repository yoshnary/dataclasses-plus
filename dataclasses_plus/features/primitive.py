import dataclasses
import types
import typing

PRIMITIVE_TYPE = dict | list | tuple | str | int | float | bool | None


def get_primitive_feature_attrs():
    return {
        "to_primitive": to_primitive,
        "from_primitive": from_primitive,
        "_dcplus_primitive_feature": True,
    }


def to_primitive(self) -> dict[str, PRIMITIVE_TYPE]:
    param_dict = {}
    for field in dataclasses.fields(self):
        value = getattr(self, field.name)
        if getattr(value, "_dcplus_primitive_feature", False):
            value = value.to_primitive()
        param_dict[field.name] = value
    _validate_primitive_type(param_dict)
    return param_dict


@classmethod
def from_primitive(cls, param_dict: dict[str, PRIMITIVE_TYPE]):
    if not isinstance(param_dict, dict):
        raise TypeError(
            f"param_dict must be a dict: found {type(param_dict).__qualname__}"
        )

    _validate_primitive_type(param_dict)

    fields = dataclasses.fields(cls)
    invalid_keys = param_dict.keys() - {f.name for f in fields}
    if invalid_keys:
        raise KeyError(f"unexpected keywords: {invalid_keys}")

    data = {}
    for field in fields:
        if field.name not in param_dict:
            continue

        value = param_dict[field.name]
        field_types = _normalize_type(field.type)

        if len(field_types) >= 3 or (
            len(field_types) == 2 and types.NoneType not in field_types
        ):
            # Due to ambiguity of types that have the same attributes,
            # we restrict union type.
            raise TypeError(
                "currently, union type except optional is not supported:"
                f" found {field.type}"
            )

        for field_type in field_types:
            if issubclass(field_type, types.NoneType):
                if value is None:
                    data[field.name] = value
                    break
            else:
                if getattr(field_type, "_dcplus_primitive_feature", False):
                    data[field.name] = field_type.from_primitive(value)
                    break
                elif isinstance(value, field_type):
                    data[field.name] = value
                    break
                elif isinstance(value, list | tuple) and issubclass(
                    field_type, list | tuple
                ):
                    # cast list ↔︎ tuple
                    data[field.name] = field_type(value)
                    break
                elif isinstance(value, int) and issubclass(field_type, float):
                    # cast int → float
                    data[field.name] = field_type(value)
                    break
        else:
            raise TypeError(
                f"{field.name} should be a {field.type}:"
                f" found {type(value).__qualname__}"
            )

    return cls(**data)


def _validate_primitive_type(obj) -> None:
    if not isinstance(obj, PRIMITIVE_TYPE):
        raise TypeError(f"type {type(obj)} is not primitive")
    if isinstance(obj, dict):
        for value in obj.values():
            _validate_primitive_type(value)
    elif isinstance(obj, tuple | list):
        for value in obj:
            _validate_primitive_type(value)


def _normalize_type(cls) -> tuple[type, ...]:
    if typing.get_origin(cls) in (typing.Union, types.UnionType):
        # convert union to tuple of classes, e.g., `str | int` → `(str, int)`
        return sum([_normalize_type(c) for c in typing.get_args(cls)], tuple())

    # remove generic parameter, e.g., `list[str]` → `list`
    return (typing.get_origin(cls) or cls,)
