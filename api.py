from flask import Flask, jsonify, make_response


app = Flask(__name__)


@app.route('/api/test')
def test():
    return make_response(jsonify(
        data={
            "message": "First trial with Flask on Heroku",
            "deployed_by": "Cagri",
            "status": "200 OK"
        }
    ), 200)


if __name__ == "__main__":
    app.run(threaded=True, port=5000)

