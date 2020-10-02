from flask import Flask, render_template, request
import os
from werkzeug import secure_filename
from pymongo import MongoClient


# set commetion string
client = MongoClient()
mydb = client["Employee_DB"]
mycol = mydb["Employee"]

# image upload file path
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:/Users\Vishal\PycharmProjects\imageupload\static\images'
app.secret_key = 'setpassword'


# default page
@app.route('/')
@app.route('/index')
def display():
    title = "Bootstrap NavBar"
    return render_template('index.html', website_title=title)


# display employee list
@app.route('/employee')
def getEmployees():
    title = 'Employee Management'
    records = get_employees()
    type1 = type(records)
    return render_template('employee.html', website_title=title, records=records, type1=type1)


# display imageupload page
@app.route('/imageupload')
def upload():
    title = "Image upload"
    return render_template('imageupload.html', website_title=title)


# upload image
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    is_success = 0
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        message = 'Image uploaded successfully'
        filename = f.filename
        imagepath = app.config['UPLOAD_FOLDER'] + '\\' + filename
        is_success = 1
        return render_template('imageupload.html', upoad_status=message, image_path=imagepath, file_name=filename,
                               success=is_success)


# insert employee
@app.route('/addemployee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        message = 'Employee added successfully'

        insert_record(id, firstname, lastname)
        records = get_employees()

        return render_template('employee.html', upload_status=message, id=id, firstname=firstname, lastname=lastname, records=records)


# insert into NoSQL database
def insert_record(id, firstname, lastname):
    record = {"Id": id, "FirstName": firstname, "LastName": lastname}
    mycol.insert_one(record)


# get records from NoSQL database
def get_employees():
    myrecords = mycol.find().sort("Id", -1)
    list_records = list(myrecords)
    return list_records


# diplay uploaded image
@app.route('/redirect_imageupload')
def show_impageupload():
    return render_template('imageupload.html')


# main method
if __name__ == '__main__':
    app.run(debug=True)