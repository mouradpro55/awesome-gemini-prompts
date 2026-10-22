import threading
import app
import webview

if __name__ == '__main__':
    print("Starting MissionTrack DZ...")
    t = threading.Thread(target=app.run_app)
    t.daemon = True
    t.start()

    webview.create_window('MissionTrack DZ', 'http://127.0.0.1:5000')
    webview.start()
