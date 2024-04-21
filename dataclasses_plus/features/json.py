import json

import fsspec


def get_json_feature_attrs():
    return {
        "to_json_str": to_json_str,
        "from_json_str": from_json_str,
        "dump_json": dump_json,
        "load_json": load_json,
        "_dcplus_json_feature": True,
    }


def to_json_str(
    self,
    ensure_ascii: bool = False,
    separators: tuple[str, str] | None = (",", ":"),
    **kwargs,
) -> str:
    data = self.to_primitive()
    kwargs["ensure_ascii"] = ensure_ascii
    kwargs["separators"] = separators
    return json.dumps(data, **kwargs)


@classmethod
def from_json_str(cls, json_str: str, **kwargs):
    primitive_data = json.loads(json_str, **kwargs)
    return cls.from_primitive(primitive_data)


def dump_json(
    self,
    file_name: str,
    ensure_ascii: bool = False,
    indent=4,
    **kwargs,
) -> None:
    data = self.to_primitive()
    kwargs["ensure_ascii"] = ensure_ascii
    kwargs["indent"] = indent
    with fsspec.open(file_name, "w") as f:
        json.dump(data, f, **kwargs)


@classmethod
def load_json(cls, file_name: str, **kwargs) -> None:
    with fsspec.open(file_name, "r") as f:
        primitive_data = json.load(f, **kwargs)
    return cls.from_primitive(primitive_data)
