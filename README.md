# Secure_Patch_Distribution
## Non Repudiation
### Environment Setup
Install Ganache, Node on Host OS

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

```bash
# Creating key pair --> example shows root CA key generation
openssl genrsa -out rootCAKey.pem 2048 # Generate private key of root CA
openssl rsa -in rootDAKey.pem -pubout -out rootDAKey.pub # Extract public key from private key

# Create self sign root CA - x509 but x509 is used for HTTPS
openssl req -x509 -sha256 -new -nodes -key rootCAKey.pem -days 3650 -out rootCACert.pem

# Review Certificate
openssl x509 -in rootCACert.pem -text

# Create signature of codeToSign.txt
openssl dgst -sha256 -sign rootCAKey.pem -out sign.txt.sha256 codeToSign.txt

# Verify signature 
openssl dgst -sha256 -verify rootDAKey.pub -signature sign.txt.sha256 codeToSign.txt

# To get checksum of vendor's public key
sha256sum <public key> | awk -F " " '{print $1}'
```

### Start dAPP
```bash
cd nr_dapp
npm run start
```