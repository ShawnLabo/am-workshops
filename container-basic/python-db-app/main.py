from flask import Flask, render_template
import os
import mydb

app = Flask(__name__)
message = 'Hello, GCP'

@app.route('/')
def hello():
    return f'<h1>{message}</h1>'

@app.route('/hostname')
def hostname():
    return f'<h1>{os.uname()[1]}</h1>'

@app.route('/fuka')
def load():
    import fuka
    for _ in range(0, 3):
        fuka.run()
    return '<h1>Loading to /fuka</h1>'

@app.route('/note', methods=["POST", "GET"])
def main():
    conn = os.environ.get("CONN", "tako")
    db = mydb.DB(conn)
    # records = db.get()
    records = [{"number":1, "name": "たろう", "data":"こんにちわ"},{"number":10, "name": "じろう", "data":"遠くからきました"}]
    return render_template("index.html", records=records)
    
if __name__ == '__main__':
    app.run(debug=True)
