from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS, cross_origin
import os, subprocess

ENROLL_UPLOAD_FOLDER = 'PKI/ca/enrollments/csr'
CRT_FOLDER = 'PKI/ca/enrollments/crt'
PATCH_UPLOAD_FOLDER = 'PKI/patches'


app = Flask(__name__)
app.config['ENROLL_UPLOAD_FOLDER'] = ENROLL_UPLOAD_FOLDER
app.config['PATCH_UPLOAD_FOLDER'] = PATCH_UPLOAD_FOLDER
app.config['CRT_FOLDER'] = CRT_FOLDER
CORS(app)


@app.route("/api/enroll", methods=['POST'])
def enroll():
        file = request.files.get('file')
        file.save(os.path.join(app.config['ENROLL_UPLOAD_FOLDER'], file.filename))
        
        vendorName = request.form.get('vendorName')
        print('VendorName : ' + str(vendorName))
        txHash = request.form.get('txHash')
        print('txHash : ' + str(txHash))

        # Generate CSC
        crt_filepath = str(file.filename).replace(".csr", ".crt")
        pub_filepath = str(file.filename).replace(".csr", ".pub")
        os.putenv("TXHASH", str(txHash))
        os.putenv("CSR_FILE", str(file.filename))
        os.putenv("CRT_FILE", crt_filepath)
        os.putenv("PUB_FILE", pub_filepath)
        os.system("bash PKI/generate_csc.sh")
        
        return crt_filepath
        # try:
        #         return send_from_directory(app.config['CRT_FOLDER'], mimetype="application/octet-stream", path=crt_filepath, as_attachment=True, attachment_filename=crt_filepath)
        # except FileNotFoundError:
        #         os.abort(404)

@app.route("/api/submitPatch", methods=['POST'])
def submitPatch():
        patchFile = request.files.get('patchFile')
        patchFile.save(os.path.join(app.config['PATCH_UPLOAD_FOLDER'], patchFile.filename))

        dcv = request.files.get('dcv')
        dcv.save(os.path.join(app.config['PATCH_UPLOAD_FOLDER'], dcv.filename))

        sigPatch = request.files.get('sigPatch')
        sigPatch.save(os.path.join(app.config['PATCH_UPLOAD_FOLDER'], sigPatch.filename))

        os.putenv("PATCH_FILE", str(patchFile.filename))
        os.putenv("DCV_FILE", str(dcv.filename))
        os.putenv("SIG_FILE", str(sigPatch.filename))
        os.putenv("PATCH_CHECKSUM", str(patchFile.filename) + '.sha256.checksum')
        os.putenv("PUB_FILE", str(dcv.filename) + '.pub')
        os.system("bash PKI/submitPatch.sh")

        # Get H(patch) & TXHASHDC
        hashPatch = subprocess.run(['cat', 'PKI/patches/HASHPATCH'], capture_output=True).stdout.decode().strip()
        txHashDC = subprocess.run(['cat', 'PKI/patches/TXHASHDC'], capture_output=True).stdout.decode().strip()
        # print(hashPatch)
        # print(txHashDC)

        data = {'hashPatch':hashPatch, 'txHashDC':txHashDC}

        return jsonify(data)