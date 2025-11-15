"""Smoke test to verify package can be imported."""


def test_can_import():
    """Test that blart package can be imported."""
    import blart

    assert blart is not None


def test_can_import_treemap():
    """Test that TreeMap can be imported from blart."""
    from blart import TreeMap

    assert TreeMap is not None


def test_can_instantiate_treemap():
    """Test that TreeMap can be instantiated."""
    from blart import TreeMap

    tree = TreeMap()
    assert tree is not None
