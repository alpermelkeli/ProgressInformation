from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

projects = {}


@app.route('/addProject', methods=['POST'])
def add_project():
    data = request.json
    project_id = data.get('project_id')

    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400

    if project_id in projects:
        projects[project_id].update(data)
    else:
        projects[project_id] = data

    return jsonify({'message': 'Project data updated successfully'}), 200


@app.route("/removeProject", methods=["POST"])
def remove_project():
    data = request.json
    project_id = data.get('project_id')
    if project_id in projects:
        projects.pop(project_id)
        return jsonify({'message': 'Project removed successfully'}), 200
    else:
        return jsonify({'error': 'Project ID not found'}), 400


@app.route('/project/<project_id>', methods=['GET'])
def get_project_data(project_id):
    project = projects.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    print(projects)
    return render_template('project_detail.html', project=project)


if __name__ == '__main__':
    app.run(debug=True)
