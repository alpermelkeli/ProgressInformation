from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Proje verilerini saklayan sözlük
projects = {}

@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.json
    project_id = data.get('project_id')

    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400

    # Proje verisini güncelle veya yeni oluştur
    if project_id in projects:
        projects[project_id].update(data)
    else:
        projects[project_id] = data

    return jsonify({'message': 'Project data updated successfully'}), 200

@app.route('/project/<project_id>', methods=['GET'])
def get_project_data(project_id):
    # Proje verisini al
    project = projects.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    # Proje verisini sayfada göster
    return render_template('project_detail.html', project=project)

if __name__ == '__main__':
    app.run(debug=True)
