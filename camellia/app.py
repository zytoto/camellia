from flask import Flask

app = Flask(__name__, template_folder='./frontend/templates')
app.secret_key = "s5AeDovBxR+hUpdJAm9hTw=="
