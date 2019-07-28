from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config) # see config.py

@app.route('/')
def hello():

    info = "Now set a breakpoint on this line"

    return """
        <h1>It works!</h1>
        <p>
            Now see app.py and set a breakpoint on the 'info' variable and start Flask with attached debugger via vscode (Press F5 in vscode) and watch the breakpoint getting hit.<br />
            (Make sure you point your browser to port 5001 instead of 5000, or simply click <a href=\"http://localhost:5001\">here</a>)"
        </p>
        <p>
            Please note that code autoreloading is disabled when debugging. So you should restart the Flask app in debug mode after every change.<br />
            See README.MD for more info.
        </p>
    """

if __name__ == '__main__':
    app.run()
