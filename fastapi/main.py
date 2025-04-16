from fastapi import FastAPI, HTTPException

app = FastAPI()


Student = [
    {'id':1,'name':'hemil','age':16,'standard':'10th','subjects':['hindi','maths','english']}
]

@app.get('/')
def index():
    return {'message':'hello word'}

@app.get('/students')
def all_students():
    return Student

@app.get('/students/{id}')
def get_students(id:int):
    for stud in Student:
        if stud['id'] == id:
            return stud
    raise HTTPException(status_code=404, detail="Student not found")

@app.post('/students')
def create_student(data:dict):

    required_fields = ['name', 'age', 'standard', 'subjects']
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    
    if not isinstance(data['age'], int) or data['age'] <= 0:
        raise HTTPException(status_code=400, detail="Age must be a positive integer")

    if not isinstance(data['subjects'], list) or len(data['subjects']) == 0:
        raise HTTPException(status_code=400, detail="Subjects must be a non-empty list")

    student_id = max(datas['id'] for datas in Student) + 1
    
    new_student = {
        'id': student_id,
        'name':data['name'],
        'age':data['age'] ,
        'standard':data['standard'],
        'subjects':data['subjects']
    }

    Student.append(new_student)
    return new_student


@app.delete('/students/{id}')
def delete_student(id:int):
    for i, stud in enumerate(Student):
        if stud['id'] == id:
            removed_student = Student.pop(i)
            return {'message': 'Student deleted successfully', 'student': removed_student}
    raise HTTPException(status_code=404, detail="Student not found")


@app.put('/students/{id}')
def update_student(id: int, data: dict):
    for i, stud in enumerate(Student):
        if stud['id'] == id:
            if 'age' in data:
                if not isinstance(data['age'], int) or data['age'] <= 0:
                    raise HTTPException(status_code=400, detail="Age must be a positive integer")
            if 'subjects' in data:
                if not isinstance(data['subjects'], list) or len(data['subjects']) == 0:
                    raise HTTPException(status_code=400, detail="Subjects must be a non-empty list")

            Student[i].update(data)
            return Student[i]
    raise HTTPException(status_code=404, detail="Student not found")