from flask import Flask, request, jsonify
import os
import tempfile
import json
from argparse import Namespace
from pai import execute_skill

app = Flask(__name__)

PAI_SECRET_KEY = os.environ.get('PAI_SECRET_KEY')

@app.before_request
def require_secret_key():
    if not PAI_SECRET_KEY:
        return jsonify({"error": "Server is not configured with a secret key."}), 500

    auth_header = request.headers.get('X-PAI-SECRET-KEY')
    if auth_header != PAI_SECRET_KEY:
        return jsonify({"error": "Unauthorized."}), 403

@app.route('/execute_skill', methods=['POST'])
def execute_skill_route():
    skill = request.form.get('skill')
    if not skill:
        return jsonify({"error": "Skill name is required."}), 400

    args_json = request.form.get('args', '{}')
    try:
        args_dict = json.loads(args_json)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in args field."}), 400

    temp_image_path = ""
    try:
        if skill == 'sharaba':
            if 'image' not in request.files:
                return jsonify({"error": "Image file is required for sharaba skill."}), 400

            image_file = request.files['image']

            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_f:
                temp_image_path = temp_f.name

            image_file.save(temp_image_path)
            args_dict['image_path'] = temp_image_path

        args = Namespace(**args_dict)

        # Consume the generator to get the full output
        result_generator = execute_skill(skill, args)
        result = "".join(list(result_generator))

        return jsonify({"output": result})

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    finally:
        if temp_image_path and os.path.exists(temp_image_path):
            os.remove(temp_image_path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
