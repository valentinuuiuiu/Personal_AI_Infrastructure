import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project root to the Python path to allow importing 'pai'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to import the module after the path is set
from pai.skills import ask

@pytest.fixture
def mock_get_client():
    """Fixture to mock the get_client function in the ask module."""
    with patch('pai.skills.ask.get_client') as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

@patch('pai.skills.ask.load_context', return_value="Mocked Context")
def test_call_llm_non_streaming(mock_load_context, mock_get_client):
    """
    Tests the call_llm function in non-streaming mode with a mocked client.
    """
    mock_get_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="The capital of France is Paris."))]
    )

    response = ask.call_llm([{"role": "user", "content": "What is the capital of France?"}])

    assert response == "The capital of France is Paris."
    mock_get_client.chat.completions.create.assert_called_once()

@patch('pai.skills.ask.load_context', return_value="Mocked Context")
def test_call_llm_streaming(mock_load_context, mock_get_client):
    """
    Tests the call_llm_stream function with a mocked client.
    """
    mock_stream_chunks = [
        MagicMock(choices=[MagicMock(delta=MagicMock(content="The "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="capital "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="of "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="France "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="is "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="Paris."))]),
    ]
    mock_get_client.chat.completions.create.return_value = iter(mock_stream_chunks)

    stream_generator = ask.call_llm_stream([{"role": "user", "content": "What is the capital of France?"}])

    result = "".join(list(stream_generator))

    assert result == "The capital of France is Paris."
    mock_get_client.chat.completions.create.assert_called_once()

@patch('pai.skills.ask.load_context', return_value="Mocked Context")
def test_main_non_streaming(mock_load_context, mock_get_client, capsys):
    """
    Tests the main function in non-streaming mode with a mocked client.
    """
    mock_get_client.chat.completions.create.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content="The capital of France is Paris."))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content="VALID"))])
    ]

    sys.argv = ["ask.py", "What is the capital of France?"]
    ask.main()

    captured = capsys.readouterr()
    assert "[VALIDATION: VALID] The capital of France is Paris." in captured.out

@patch('pai.skills.ask.load_context', return_value="Mocked Context")
@patch('builtins.print')
def test_main_streaming(mock_print, mock_load_context, mock_get_client):
    """
    Tests the main function in streaming mode with a mocked client.
    """
    mock_stream_chunks = [
        MagicMock(choices=[MagicMock(delta=MagicMock(content="The "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="capital "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="of "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="France "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="is "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="Paris."))]),
    ]
    mock_get_client.chat.completions.create.return_value = iter(mock_stream_chunks)

    sys.argv = ["ask.py", "--stream", "What is the capital of France?"]
    ask.main()

    calls = mock_print.call_args_list
    output = "".join([call[0][0] for call in calls if call[0] and isinstance(call[0][0], str)])
    assert "The capital of France is Paris." in output
