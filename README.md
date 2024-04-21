# dataclasses-plus

dataclass with enhanced features

## Features

dataclasses-plus currently supports following features:

- convert to and load from JSON/YAML string and file

## Install

```sh
pip install git+https://github.com/yoshnary/dataclasses-plus.git
```

You may install it with PyYAML to enable the YAML features.

```sh
pip install "dataclasses-plus[yaml] @ git+https://github.com/yoshnary/dataclasses-plus.git"
```

## Usage

Just replace `dataclasses` with `dataclasses_plus` and the features are unlocked.

```diff
-from dataclasses import dataclass
+from dataclasses_plus import dataclass
```

```python
>>> @dataclass
... class Data:
...     foo: int
...     bar: str
...     baz: bool
...
>>> data = Data(1, "one", True)
>>> data.to_json_str()
'{"foo":1,"bar":"one","baz":true}'
>>> another_data = Data.from_json_str(data.to_json_str())
>>> another_data
Data(foo=1, bar='one', baz=True)
```

## API Reference

### JSON feature

#### to_json_str / from_json_str

- Convert dataclass to JSON string
- Create a new instance from JSON string

#### dump_json / load_json

- Save dataclass to file in JSON format
- Create a new instance from JSON file

### YAML feature

#### to_yaml_str / from_yaml_str

- Convert dataclass to YAML string
- Create a new instance from YAML string

#### dump_yaml / load_yaml

- Save dataclass to file in YAML format
- Create a new instance from JSON file

You may find details in [dataclasses_plus/features](dataclasses_plus/features).
