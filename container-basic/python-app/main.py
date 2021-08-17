from flask import Flask
app = Flask(__name__)
import os

# Change this
message = 'Hello, GCP'

@app.route('/')
def hello_world():
    return f'<h1>{message}</h1>'

@app.route('/hostname')
def hostname():
    return f'<h1>{os.uname()[1]}</h1>'

@app.route('/fuka')
def load():
    # tracer = get_tracer()
    import fuka
    for _ in range(0, 3):
        fuka.run()
    return '<h1>Loading to /fuka</h1>'

