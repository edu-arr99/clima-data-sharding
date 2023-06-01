from flask import Flask, jsonify
from flask_mongoengine import MongoEngine

app = Flask[__name__]
app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': 'mongodb://172.18.0.1:30000/test'
}
db = MongoEngine(app)

class Clima(db.document):
    date = db.StringField()
    city = db.StringField()
    latitude = db.FloatField()
    longitude = db.FloatField()
    temp_max = db.FloatField()
    temp_min = db.FloatField()
    temp = db.FloatField()

@app.route("/read/<city>", methods=["GET"])
def get_data(city):
    data = Clima.objects(city=city).first()
    if data:
        return jsonify(data.to_json())
    else:
        return jsonify({"message": "Data not found"}), 404
    

if __name__ == "__main__":
    app.run(port=5000)