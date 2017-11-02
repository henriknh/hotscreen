from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return "Stuff be sorta workin'..."

if __name__ == "__main__":
	app.run(host='0.0.0.0')
