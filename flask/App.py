from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

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

    socketio.emit('project_update', projects[project_id], room=project_id)

    return jsonify({'message': 'Project data updated successfully'}), 200


@app.route("/removeProject", methods=["POST"])
def remove_project():
    data = request.json
    project_id = data.get('project_id')
    if project_id in projects:
        projects.pop(project_id)
        socketio.emit('project_removed', {'project_id': project_id}, room=project_id)
        return jsonify({'message': 'Project removed successfully'}), 200
    else:
        return jsonify({'error': 'Project ID not found'}), 400


@app.route('/project/<project_id>', methods=['GET'])
def get_project_data(project_id):
    project = projects.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return render_template('project_detail.html', project_id=project_id)


@socketio.on('join_project')
def on_join(data):
    project_id = data.get('project_id')
    join_room(project_id)
    if project_id in projects:
        emit('project_update', projects[project_id], room=project_id)


@socketio.on('leave_project')
def on_leave(data):
    project_id = data.get('project_id')
    leave_room(project_id)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
