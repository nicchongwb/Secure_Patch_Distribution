# Secure_Patch_Distribution
## Non Repudiation
### Environment Setup
Install Ganache, Node on Host OS

Linux:
```bash
cd nr_dapp
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Windows:
[Guide to upgrade npm to latest version](https://stackoverflow.com/questions/72401421/message-npm-warn-config-global-global-local-are-deprecated-use-loc)

Install [git](https://git-scm.com/download/win) for windows (required for Node)

```PS
# Open PS in admin
Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force
npm install --global --production npm-windows-upgrade
npm-windows-upgrade --npm-version latest
```

```bash
cd nr_adapp
npm install
```

Note: Add truffle-config.js to Ganache Workspace project settings

### Start APP & MICROSERVICES
```bash
# Linux
. venv/bin/activate
FLASK_APP=app.py FLASK_ENV=development flask run # Run Flask in debug mode

# CMD
cd nr_dapp
npm run start
```


### Truffle
truffle commands
```bash
cd nr_dapp
truffle compile # Compile contracts --> artifacts produced in /build
truffle migrate --reset # Migrate to deploy Smart Contracts to Ganache Network

truffle console # enter truffle console
enrollment = await Enrollment.deployed() # retrieve contract deployed and assign to variable
enrollment # We can see the smart contract detail
enrollment.address # Address of smart contract
enrollment.EnrollmentCount() # View our contract state variable EnrollmentCount

# View the state variable value in a better format
enrollmentCount = await enrollment.EnrollmentCount()
enrollmentCount.toNumber()

# View default transaction when Enrollment.sol is deployed
er = await enrollment.enrollments(1)
er
```
### OpenSSL
[Code Signing, Verification with OpenSSL](https://eclipsesource.com/blogs/2016/09/07/tutorial-code-signing-and-verification-with-openssl/)
[SSL Guide](https://gist.github.com/kyledrake/d7457a46a03d7408da31)
[Openssl CA Guide](https://blogg.bekk.no/how-to-sign-a-certificate-request-with-openssl-e046c933d3ae)
[SSL Cert Signing Files](https://stackoverflow.com/questions/9691521/can-ssl-cert-be-used-to-digitally-sign-files)
[DOC - x509v3 conf](https://www.openssl.org/docs/manmaster/man5/x509v3_config.html)


```bash
# Setting up CA
cd PKI/ca
openssl genrsa -out ca.pem 2048 # Generate private key of CA
openssl rsa -in ca.pem -pubout -out ca.pub # Get public key from private key
openssl req -new -x509 -days 10000 -key ca.pem -out ca.crt # Generate CA self sign cert, make sure to key in "DA" for commonName value

# Setting up vendor
cd PKI/vendor_A
openssl genrsa -out vendorA.pem 2048 # Generate private key of CA
openssl rsa -in vendorA.pem -pubout -out vendorA.pub # Get public key from private key
openssl req -new -key vendorA.pem -out vendorA.csr # Generate a CSR

# Get CA to sign Vendor's CSR and generate CSC for vendor
cd PKI
## Use extension to add in Enrollment Transaction Hash
openssl x509 -sha256 -req -in vendor_A/vendorA.csr -CA ca/ca.crt -CAkey ca/ca.pem -CAcreateserial -out vendorA.crt -days 10000 -extensions crt_ext -extfile csc.conf
openssl verify -CAfile ca/ca.crt vendorA.crt # Verify vendorA.crt using CA's cert

# Vendor Signing Files
cd PKI
openssl dgst -sha256 -sign vendor_A/vendorA.pem -out vendor_A/test_vendorA.sha256 vendor_A/test_vendorA.txt
openssl dgst -sha256 -sign vendorA.pem -out patch.sha256.checksum.sig patch.sha256.checksum # Example 2

# CA extract vendor's pub from vendor CSR
openssl req -in vendor_A/vendorA.csr -pubkey -out vendorAcsr_extract.pub # For enrollment process

# Client/Verifier verifiy signature of file via vendor's CSC
cd PKI
openssl verify -verbose -CAfile ca/ca.crt ca/enrollments/crt/vendorA.crt # Verify vendor's CSC using CA's cert
openssl x509 -in ca/enrollments/crt/vendorA.crt -pubkey -noout > ca/enrollments/pub/vendorA.pub # Extract vendor's pub from vendor's CSC

## Use extracted vendor's pub to verify signature of file
openssl dgst -sha256 -verify ca/enrollments/pub/vendorA.pub -signature vendor_A/test_vendorA.sha256 vendor_A/test_vendorA.txt
 
# Review Certificate
openssl x509 -in vendorA.crt -text
# To get checksum of vendor's public key
sha256sum <public key> | awk -F " " '{print $1}'
```
