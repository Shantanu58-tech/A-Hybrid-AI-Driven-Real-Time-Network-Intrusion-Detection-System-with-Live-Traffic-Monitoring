
from app import app, socketio, start_monitoring
import webbrowser
import threading
import time

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("Initializing Enterprise SOC System...")
    print("Access the dashboard at http://127.0.0.1:5000")
    
    # Start packet capture
    start_monitoring()
    
    # Open browser automatically
    threading.Thread(target=open_browser).start()
    
    # Run server
    socketio.run(app, debug=True, port=5000)
