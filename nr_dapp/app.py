from flask import Flask, request, json
from flask_cors import CORS, cross_origin
import os

UPLOAD_FOLDER = 'PKI/ca/enrollments/csr'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


@app.route("/api/enroll", methods=['POST'])
def enroll():
        file = request.files.get('file')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
        vendorName = request.form.get('vendorName')
        print('VendorName : ' + str(vendorName))
        txHash = request.form.get('txHash')
        print('txHash : ' + str(txHash))
        result = 'From API '
        return result