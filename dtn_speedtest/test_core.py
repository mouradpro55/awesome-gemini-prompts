import pytest
from core import save_to_history
import os
import pandas as pd

def test_save_to_history_success(tmp_path):
    # Override HISTORY_FILE path for testing to not pollute the real directory
    import core
    test_file = tmp_path / "test_history.csv"
    core.HISTORY_FILE = str(test_file)

    mock_result = {
        "success": True,
        "download_mbps": 50.5,
        "upload_mbps": 20.2,
        "ping_ms": 15.0,
        "server_sponsor": "DTN Sponsor",
        "server_name": "Al Menea"
    }

    assert save_to_history(mock_result) == True
    assert os.path.exists(test_file)

    df = pd.read_csv(test_file)
    assert len(df) == 1
    assert df["Download (Mbps)"].iloc[0] == 50.5
    assert df["Server Sponsor"].iloc[0] == "DTN Sponsor"


def test_save_to_history_failure():
    mock_result = {
        "success": False,
        "error": "Connection Timeout"
    }

    assert save_to_history(mock_result) == False