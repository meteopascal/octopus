# import pytest
from db import SitesDb

"""
Lancement des tests:
    cd octopus   # PAS octopus/tests
    pytest
"""

db_path = 'tests/fixtures.sqlite'
d_read_only = SitesDb(db_path)


def test_get_by_id_fields():
    site = d_read_only.get_by_id(207)
    assert isinstance(site, dict)
    assert 'tower_height' in site


def test_get_all():
    assert len(d_read_only.get_all()) == 23
