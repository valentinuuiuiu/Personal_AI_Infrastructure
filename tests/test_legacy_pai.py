import os

def test_legacy_pai_command_is_removed():
    """
    Tests that the legacy 'pai' command has been removed.
    """
    # Define the path to the legacy pai.py script
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pai', 'pai.py'))

    # Check that the script does not exist
    assert not os.path.exists(script_path), f"The legacy PAI script at {script_path} should not exist."

    # Also check that the 'pai' directory is gone
    pai_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pai'))
    assert not os.path.exists(pai_dir), f"The legacy PAI directory at {pai_dir} should not exist."
