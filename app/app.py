from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_input():
    data = request.json
    output = {"response": f"Processed input: {data['input']}"}
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)

