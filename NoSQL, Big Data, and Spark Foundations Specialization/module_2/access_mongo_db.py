from pymongo import MongoClient
from datetime import datetime
from bson.json_util import dumps   


uri = "mongodb://localhost:27017/campus"  
client = MongoClient(uri)  
campusDB = client.campus
students = campusDB.students 

print(students.count_documents({"email":"jkakandris@gmail.com"}))

student_list = [ 
                {"name":"Ioanna" , "birth":datetime.strptime("2001-05-20", "%Y-%m-%d") , "email":"jkakandris@gmail.com" , "studentId":20012178  }, 
  {"name":"Meliena" , "birth":datetime.strptime("2001-05-20", "%Y-%m-%d") , "email":"jkakandris@gmail.com" , "studentId":20012178  }]

students.insert_many(student_list)  

print(students.count_documents({"email":"jkakandris@gmail.com"}))

cursor = students.find({"name":"Jason"})
print(dumps(cursor , indent = 4 )) 