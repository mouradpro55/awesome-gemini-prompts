import speedtest
import pandas as pd
import os
from datetime import datetime

HISTORY_FILE = "speedtest_history.csv"

def get_best_server(st=None):
    if not st:
        st = speedtest.Speedtest()
    st.get_best_server()
    return st

def test_speed():
    try:
        st = speedtest.Speedtest()
        # Get best server
        server = st.get_best_server()

        # Test download and upload (convert to Mbps)
        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        ping = server['latency']

        return {
            "success": True,
            "download_mbps": round(download_speed, 2),
            "upload_mbps": round(upload_speed, 2),
            "ping_ms": round(ping, 2),
            "server_sponsor": server.get('sponsor', 'Unknown'),
            "server_name": server.get('name', 'Unknown')
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def save_to_history(result):
    if not result.get("success"):
        return False

    data = {
        "Date Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Download (Mbps)": result["download_mbps"],
        "Upload (Mbps)": result["upload_mbps"],
        "Ping (ms)": result["ping_ms"],
        "Server Sponsor": result["server_sponsor"],
        "Server Location": result["server_name"],
    }

    df = pd.DataFrame([data])

    if os.path.exists(HISTORY_FILE):
        df.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(HISTORY_FILE, mode='w', header=True, index=False)

    return True