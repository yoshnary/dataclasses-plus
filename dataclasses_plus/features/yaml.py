import fsspec
import yaml


def get_yaml_feature_attrs():
    return {
        "to_yaml_str": to_yaml_str,
        "from_yaml_str": from_yaml_str,
        "dump_yaml": dump_yaml,
        "load_yaml": load_yaml,
        "_dcplus_yaml_feature": True,
    }


def to_yaml_str(self) -> str:
    data = self.to_primitive()
    return yaml.safe_dump(data)


@classmethod
def from_yaml_str(cls, yaml_str: str):
    primitive_data = yaml.safe_load(yaml_str)
    return cls.from_primitive(primitive_data)


def dump_yaml(self, file_name: str) -> None:
    data = self.to_primitive()
    with fsspec.open(file_name, "w") as f:
        yaml.safe_dump(data, f)


@classmethod
def load_yaml(cls, file_name: str, **kwargs) -> None:
    with fsspec.open(file_name, "r") as f:
        primitive_data = yaml.safe_load(f, **kwargs)
    return cls.from_primitive(primitive_data)
