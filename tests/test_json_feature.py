import tempfile

import pytest

import dataclasses_plus


@dataclasses_plus.dataclass
class ChildConfig:
    c_a: int


@dataclasses_plus.dataclass
class ParConfig:
    a: dict[str, int]
    b: list
    c: tuple
    d: str
    e: int
    f: float
    g: bool
    h: int | None
    child: ChildConfig
    default: int = 42


@dataclasses_plus.dataclass(frozen=True)
class FrozenChildConfig:
    c_a: int


@dataclasses_plus.dataclass(frozen=True)
class FrozenParConfig:
    a: dict[str, int]
    b: list
    c: tuple
    d: str
    e: int
    f: float
    g: bool
    h: int | None
    child: FrozenChildConfig
    default: int = 42


cls_parameter = pytest.mark.parametrize(
    ("par_cls", "child_cls"),
    (
        (ParConfig, ChildConfig),
        (FrozenParConfig, FrozenChildConfig),
    ),
)


class TestJsonFeature:

    @cls_parameter
    def test_save_load_str(self, par_cls, child_cls):
        expected = par_cls(
            {"k": 3},
            [2],
            (1.0,),
            "foo",
            1,
            0.1,
            True,
            None,
            child_cls(2),
        )

        json_str = expected.to_json_str()
        actual = par_cls.from_json_str(json_str)

        assert expected == actual

    @cls_parameter
    def test_negative_to_json_str(self, par_cls, child_cls):
        config = par_cls(
            {"k": 3},
            [2],
            (1.0,),
            "foo",
            1,
            0.1j,  # invalid type
            True,
            None,
            child_cls(2),
        )

        with pytest.raises(TypeError, match=r"type .* is not primitive"):
            config.to_json_str()

    @cls_parameter
    def test_negative_key_from_json_str(self, par_cls, child_cls):
        json_str = '{"z":{"foo":3},"b":[2],"c":[0.1],"d":"foo","e":1,"f":0.1,"g":true,"h":null,"child":{"c_a":2}}'  # noqa: E501

        with pytest.raises(KeyError, match=r"unexpected keywords: .*"):
            par_cls.from_json_str(json_str)

    @cls_parameter
    def test_negative_type_from_json_str(self, par_cls, child_cls):
        # invalid type for "g"
        json_str = '{"a":{"foo":3},"b":[2],"c":[0.1],"d":"foo","e":1,"f":0.1,"g":1,"h":null,"child":{"c_a":2}}'  # noqa: E501

        with pytest.raises(TypeError, match=r".* should be a .*: found .*"):
            par_cls.from_json_str(json_str)

    @cls_parameter
    def test_save_load(self, par_cls, child_cls):
        expected = par_cls(
            {"k": 3},
            [2],
            (1.0,),
            "foo",
            1,
            0.1,
            True,
            None,
            child_cls(2),
        )

        with tempfile.NamedTemporaryFile() as f:
            expected.dump_json(f.name)
            actual = par_cls.load_json(f.name)

        assert expected == actual

    @cls_parameter
    def test_set_flag(self, par_cls, child_cls):
        config = par_cls(
            {"k": 3},
            [2],
            (1.0,),
            "foo",
            1,
            0.1j,  # invalid type
            True,
            None,
            child_cls(2),
        )

        assert config._dcplus_json_feature
