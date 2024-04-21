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


class TestPrimitiveFeature:

    @cls_parameter
    def test_to_primitive(self, par_cls, child_cls):
        config = par_cls(
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

        expected = {
            "a": {"k": 3},
            "b": [2],
            "c": (1.0,),
            "d": "foo",
            "e": 1,
            "f": 0.1,
            "g": True,
            "h": None,
            "child": {"c_a": 2},
            "default": 42,
        }

        actual = config.to_primitive()

        assert expected == actual

    @cls_parameter
    def test_negative_to_primitive(self, par_cls, child_cls):
        config = par_cls(
            {"k": 3},
            [2],
            (1.0,),
            "foo",
            1,
            0.1,
            True,
            None,
            child_cls(2j),  # invalid type
        )

        with pytest.raises(TypeError, match=r"type .* is not primitive"):
            config.to_primitive()

    @cls_parameter
    def test_from_primitive(self, par_cls, child_cls) -> None:
        primitive_data = {
            "a": {"k": 3},
            "b": [2],
            "c": (1.0,),
            "d": "foo",
            "e": 1,
            "f": 0.1,
            "g": True,
            "h": None,
            "child": {"c_a": 2},
        }

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

        actual = par_cls.from_primitive(primitive_data)

        assert expected == actual

    @cls_parameter
    def test_negative_key_from_primitive(self, par_cls, child_cls):
        primitive_data = {
            "a": {"k": 3},
            "b": [2],
            "z": (1.0,),  # invalid keyword
            "d": "foo",
            "e": 1,
            "f": 0.1,
            "g": True,
            "h": None,
            "child": {"c_a": 2},
        }

        with pytest.raises(KeyError, match=r"unexpected keywords: .*"):
            par_cls.from_primitive(primitive_data)

    @cls_parameter
    def test_negative_type_from_primitive(self, par_cls, child_cls):
        primitive_data = {
            "a": {"k": 3},
            "b": [2],
            "c": (1.0,),
            "d": "foo",
            "e": 1,
            "f": 0.1,
            "g": 1,  # invalid type
            "h": None,
            "child": {"c_a": 2},
        }

        with pytest.raises(TypeError, match=r".* should be a .*: found .*"):
            par_cls.from_primitive(primitive_data)

    @cls_parameter
    def test_set_flag(self, par_cls, child_cls):
        config = par_cls(
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

        assert config._dcplus_primitive_feature
