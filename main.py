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
    return jsonify(result), 201

@app.route("/notes", methods = ["GET"])
def get_all_notes_from_db():
    data = get_all_notes()
    return jsonify(data)

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def remove_note(note_id):
    delete_notes(note_id)
    return "", 204

@app.route("/notes/<int:note_id>",methods = ["PUT"])
def update_note_in_db(note_id):
    data = request.get_json()
    update_note(note_id,data["text"])
    return jsonify({"error": f"Note {note_id} not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
