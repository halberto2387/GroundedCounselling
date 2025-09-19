import importlib
import pytest


def test_placeholder_migration_raises():
    mod = importlib.import_module('alembic.versions.0006_drop_specialist_json_field_placeholder')
    with pytest.raises(RuntimeError):
        mod.upgrade()  # type: ignore
