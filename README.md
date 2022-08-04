# Secure_Patch_Distribution
## Preface
In 2012, Australian intelligence officials had claimed that a software update on Huawei’s network equipment had caused a soph isticated intrusion into
the country’s telecommunication systems. Huawei had dismissed this claim stating that there is a lack of evidence.
Between 2019 and 2020, a group of hackers managed to infiltrate SolarWinds' production network and inserted lines of maliciou s codes, that aims to
create a backdoor, into SolarWinds’ Orion software updates. The hackers then proceed to target a smaller number of organizations, most notably US
government agencies where confidential information were leaked.

## Project Goals
This project aims to create a patch distribution framework that are able to do the following:
 1. Having a mechanism to ensure non-repudiation of the software patches
 2. Having a mechanism/framework that allows software vendors to do an open declaration on the actions in all patches. This de claration can then be
validated by a third party.

Note: Framework must also ensure and safeguard the rights of the software vendors by ensuring the information/actions declared does not enough to
cause an attack.

---

## PoC Installation Guide
### Open Declaration
```bash
g++ patch.cpp -o patch
./patch

strace ./patch 2> patch_strace.txt
```

### Non Repudiation
#### Environment Setup
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

#### Start APP & MICROSERVICES
```bash
# Linux
. venv/bin/activate
FLASK_APP=app.py FLASK_ENV=development flask run # Run Flask in debug mode

# CMD
cd nr_dapp
npm run start
```


#### Truffle
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
#### OpenSSL References
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
---
## Framework Design
### Open-Declaration Process Flow
![OD-ProcessFlow](https://github.com/nicchongwb/Secure_Patch_Distribution/blob/main/Process%20Flow%20of%20Framework%20-%20Finalized%20OD.png)


### Non-Repudiation Protocol Design
![NR-Protocol](https://github.com/nicchongwb/Secure_Patch_Distribution/blob/main/Process%20Flow%20of%20Framework%20-%20Finalized%20NR.png?raw=true)


---

## PoC Demo
### Open-Declaration Proof-of-Concept
https://user-images.githubusercontent.com/56181271/182874075-7ea4d752-8a0c-48a9-9af3-d7a289b7d383.mp4



### Non-Repudiation Proof-of-Concept
https://user-images.githubusercontent.com/56181271/182873107-dce9e2a0-8396-4827-b8cf-fb57b5735150.mp4

