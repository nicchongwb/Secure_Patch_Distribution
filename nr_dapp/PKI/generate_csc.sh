#!/bin/bash
cd PKI
cp csc.conf csc_temp.conf
sed -i "s/PLACEHOLDER/$TXHASH/g" csc_temp.conf

# Generate CRT
openssl x509 -sha256 -req -in ca/enrollments/csr/${CSR_FILE} -CA ca/ca.crt -CAkey ca/ca.pem -CAcreateserial -out ca/enrollments/crt/${CRT_FILE} -days 10000 -extensions crt_ext -extfile csc_temp.conf

# Extract vendor's public key from CSR
openssl req -in ca/enrollments/crt/${CRT_FILE} -pubkey -out ca/enrollments/pub/${PUB_FILE}

rm csc_temp.conf