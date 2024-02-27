from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from gridfs import GridFS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://sowmiksekhar123456:9074464169@cluster0.josdldc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db=client['Cluster0']
collection = db['files']
fs = GridFS(db)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



app = Flask(__name__)
app.secret_key = "secret" # Change this!
@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/upload")
def uploader():
    return render_template("uploadfile.html")

@app.route("/status")
def status():
    # Query MongoDB for uploaded PDFs and their statuses
    uploaded_pdfs = collection.find({}, {'filename': 1, 'status': 1})  # Retrieve filename and status fields
    
    # Render status page template with uploaded PDFs and their statuses
    return render_template('status.html', uploaded_pdfs=uploaded_pdfs)

@app.route('/success')
def success():
    return render_template("success.html")
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        # Store file in MongoDB
        file_id = fs.put(file.stream, filename=filename)
        # Optionally, save file metadata to MongoDB
        db.files.insert_one({'filename': filename, 'status': "pending"})
        flash("File uploaded successfully")
        return redirect(url_for('status'))
if __name__ == "__main__":
    app.run(debug=True)
