import dataclasses

import pytest

import dataclasses_plus


@dataclasses_plus.dataclass
class Config:
    a: int


@dataclasses_plus.dataclass(frozen=True)
class FrozenConfig:
    a: int


class TestDataclass:
    def test_non_frozen_assign(self):
        config = Config(1)

        expected = 1000

        config.a = expected

        assert expected == config.a

    def test_frozen_assign(self):
        config = FrozenConfig(1)

        with pytest.raises(dataclasses.FrozenInstanceError):
            config.a = 1000
