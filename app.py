from flask import Flask, jsonify

prcp_dict = [
    {'2017-08-23': 0.45,
  '2017-08-22': 0.5,
  '2017-08-21': 0.56,
  '2017-08-20': "nan"
}
]
app = Flask(__name__)
@app.route("/")
def index():
    return (
        f"Welcome to Home page!<br />"
        f"Available Routes:<br />"
        f"/api/v1.0/precipitation<br />"
        f"/api/v1.0/stations<br />"
        f"/api/v1.0/tobs<br />"
        f"/api/v1.0/<start><br />"
        f"/api/v1.0/<start>/<end><br />"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp_dict)


if __name__ =="__main__":
    app.run(debug=True)