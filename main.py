from http import HTTPStatus

from flask import Flask, jsonify, request

from database.main import add_new_note, init_db, get_all_notes, delete_notes, update_note

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Flask!"

@app.route("/greet/<name>")
def greet(name:str):
    return jsonify({"message":f"Hello, {name}"})

# notes = []
init_db()

@app.route("/notes", methods = ["POST"])
def create_notes():
    data = request.get_json()
    result = add_new_note(data["text"])
    return jsonify(result), HTTPStatus.CREATED

@app.route("/notes", methods = ["GET"])
def get_all_notes_from_db():
    data = get_all_notes()
    return jsonify(data)

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def remove_note(note_id):
    delete_notes(note_id)
    return "", HTTPStatus.NO_CONTENT

@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note_in_db(note_id):
    data = request.get_json()
    result = update_note(note_id, data["text"])

    if result == "Note doesn't found":
        return jsonify({"error": f"Note {note_id} not found"}), HTTPStatus.NOT_FOUND
    else:
        return jsonify({"message": result}), HTTPStatus.OK


if __name__ == "__main__":
    app.run(debug=True)
