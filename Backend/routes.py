from app import app, db
from models import Class, Assignment, Event, StudyLog
from flask import request, jsonify, send_from_directory
from Data_viz.generate_chart import get_chart_as_base64

@app.route('/')
def home():
    return send_from_directory('../Frontend', 'index.html')

@app.route('/<path:filename>')
def serve_page(filename):
    return send_from_directory('../Frontend', filename)


#For classes
@app.route('/api/classes', methods=['GET'])
def get_classes():
    #query the databse classes to get all class records
    classes = Class.query.all()

    #COnvering the list of classe into a list of dictionries
    result = [
        {"id": c.id, "name": c.name, "time" : c.time, "day": c.day} for c in classes
    ]
    # retuning list as json response
    return jsonify(result)

@app.route('/api/add-class',methods=['POST'])
def add_class():
    class_data = request.get_json()
    new_class = Class(
        name = class_data['name'],
        time = class_data['time'],
        day = class_data['day']
    )

    db.session.add(new_class)
    db.session.commit()
    return jsonify({'message':'Class added successfully'})


#For assignments
@app.route('/api/assignments', methods=['GET'])
def get_assignments():
    assignments = Assignment.query.all()
    result = [{'id': a.id, 'title': a.title, 'subject': a.subject, 'due_date': a.due_date} for a in assignments]
    return jsonify(result)

@app.route('/api/add-assignment',methods=['POST'])
def add_assignment():
    assignment_data = request.get_json()
    new_assignment = Assignment(
        title = assignment_data['title'],
        subject = assignment_data['subject'],
        due_date = assignment_data['due_date']
    )
    db.session.add(new_assignment)
    db.session.commit()
    return jsonify({'message':'Assignment added successfully'})

#For Evens
@app.route('/api/events', methods=['GET'])
def add_events():
    events = Event.query.all()
    result =[{
        "id": e.id, "title": e.title, "date": e.date, "location": e.location
    } for e in events]
    return jsonify(result)

@app.route('/api/add-event',methods=['POST'])
def add_event():
    events = request.get_json()
    new_event = Event(
        title = events['title'],
        date = events['date'],
        location = events['location']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message':'Event added successfully'})


#For study logs
@app.route('/api/studylogs', methods=['GET'])
def get_study_logs():
    logs = StudyLog.query.all()
    result = [{
        "id": l.id, "date":l.date, "subject":l.subject,"duration":l.duration
    } for l in logs]
    return jsonify(result)


@app.route('/api/add-studylog',methods=['POST'])
def add_study_log():
    study_log_data = request.get_json()
    new_study_log = StudyLog(
        date = study_log_data['date'],
        subject = study_log_data['subject'],
        duration = study_log_data['duration']
    )
    db.session.add(new_study_log)
    db.session.commit()
    return jsonify({'message':'Study log added successfully'})

@app.route('/api/generate-study-chart', methods=['GET'])
def generate_study_chart():
    study_logs = StudyLog.query.all()
    if not study_logs:
        return jsonify({'message': 'No study logs available to generate a chart.'})

    log_data = [{'date': log.date, 'subject': log.subject, 'duration': log.duration} for log in study_logs]
    
    chart_base64 = get_chart_as_base64(log_data)
    
    if chart_base64:
        chart_url = f"data:image/png;base64,{chart_base64}"
        return jsonify({'chart_url': chart_url})
    else:
        return jsonify({'message': 'Could not generate chart from the available data.'})

