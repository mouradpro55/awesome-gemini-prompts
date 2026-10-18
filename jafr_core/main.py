import webview
import threading
import socket
from backend.app import app, init_app

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def start_server(port):
    app.run(port=port, host='127.0.0.1', debug=False, use_reloader=False)

if __name__ == '__main__':
    # Initialize DB (extract ARQURAN.TXT into DB)
    init_app()

    port = find_free_port()

    server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    server_thread.start()

    webview.create_window(
        'محرك حساب الجفر والتحليل القرآني - JafrCore Engine',
        f'http://127.0.0.1:{port}',
        width=1100,
        height=800,
        min_size=(800, 600),
        text_select=True,
        confirm_close=True
    )

    webview.start()
