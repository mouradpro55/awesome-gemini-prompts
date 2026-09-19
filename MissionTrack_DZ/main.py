import os
import socket
import sys
import threading
import webview
import app

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def start_flask(port):
    app.app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)

if __name__ == '__main__':
    port = find_free_port()
    server_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    server_thread.start()

    window = webview.create_window(
        title='MissionTrack DZ - نظام تسيير وحساب كشوف مصاريف التنقل',
        url=f'http://127.0.0.1:{port}',
        width=1260,
        height=860,
        resizable=True,
        min_size=(980, 680),
        confirm_close=True
    )
    webview.start()
    sys.exit(0)
