import pytest
from bot.commands.dockerize import dockerize_cmd

def test_dockerize_command_exists():
    assert callable(dockerize_cmd)
