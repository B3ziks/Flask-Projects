from flask import Flask, jsonify, request, render_template_string, send_file
import json
import os
import uuid
from datetime import datetime  

app = Flask(__name__, static_folder='todo')
todo_file = 'todos.json'

# Ensure the JSON file exists
if not os.path.exists(todo_file):
    with open(todo_file, 'w') as file:
        json.dump([], file)

@app.route('/')
def index():
    with open(todo_file, 'r') as file:
        todos = json.load(file)
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    
    tasks_before = []
    tasks_today = []
    tasks_later = []
    
    for todo in todos:
        task_datetime = datetime.strptime(f"{todo['date']} {todo['time']}", '%Y-%m-%d %H:%M')
        
        # Move tasks with today's date to the "Today" category
        if todo['date'] == today_str:
            todo['date'] = 'Today'  # Mark as "Today"
            if task_datetime <= now:
                todo['overdue'] = True  # Mark overdue if time has passed
                tasks_before.append(todo)
            else:
                tasks_today.append(todo)
        elif task_datetime < now:
            todo['overdue'] = True  # Mark overdue if the date has passed
            tasks_before.append(todo)
        else:
            # For tasks in the future, check if the date becomes today
            if task_datetime.date() == now.date():
                todo['date'] = 'Today'  # Mark as "Today"
                tasks_today.append(todo)
            else:
                tasks_later.append(todo)
    
    return render_template_string(open('todo_template.html').read(), 
                                  tasks_before=tasks_before, 
                                  tasks_today=tasks_today, 
                                  tasks_later=tasks_later)
                                  
@app.route('/add', methods=['POST'])
def add_todo():
    task_content = request.form.get('task')
    task_date = request.form.get('date')
    task_time = request.form.get('time')
    if task_content and task_date and task_time:
        with open(todo_file, 'r+') as file:
            todos = json.load(file)
            task_id = str(uuid.uuid4())  # Generate a unique ID for the task
            todos.append({
                'id': task_id,
                'task': task_content,
                'date': task_date,
                'time': task_time,
                'completed': False
            })
            file.seek(0)
            json.dump(todos, file)
    return jsonify(success=True)
    
@app.route('/complete', methods=['POST'])
def complete_todo():
    task_id = request.form.get('id')
    if task_id:
        with open(todo_file, 'r+') as file:
            todos = json.load(file)
            for todo in todos:
                if todo['id'] == task_id:
                    todo['completed'] = True
                    break  # Stop the loop once the task is found and updated
            
            file.seek(0)
            json.dump(todos, file)
            file.truncate()  # Ensure the file size is adjusted if the new data is smaller than the old
            
    return jsonify(success=True)

@app.route('/delete', methods=['POST'])
def delete_todo():
    task_id = request.form.get('id')
    updated_tasks = []
    deleted = False
    with open(todo_file, 'r+') as file:
        todos = json.load(file)
        for todo in todos:
            if todo['id'] != task_id:
                updated_tasks.append(todo)
            else:
                deleted = True
        file.seek(0)
        json.dump(updated_tasks, file)
        file.truncate()
    return jsonify(success=deleted)
    
@app.route('/alarm.mp3')
def alarm_sound():
    return send_file('alarm.mp3', conditional=True)

if __name__ == '__main__':
    app.run(debug=True)