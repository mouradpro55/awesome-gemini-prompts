# Bootstrapper for the Flask App to ensure clean launching
import app

if __name__ == '__main__':
    print("Starting MissionTrack DZ Web Server...")
    app.threading.Timer(1.5, lambda: app.webbrowser.open("http://127.0.0.1:5000")).start()
    app.run_app()
