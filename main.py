import webview
import threading
from app import app

def start_flask():
  app.run(host='0.0.0.0')

if __name__ == '__main__':
  # start Flask in a separate thread
  flask_thread = threading.Thread(target=start_flask)
  flask_thread.daemon = True
  flask_thread.start()

  # create WebView window
  webview.create_window('MyApp', 'http://localhost:5000', frameless=True)
  webview.start()