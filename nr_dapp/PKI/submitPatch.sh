#!/bin/bash
cd PKI/patches

echo $DCV_FILE
echo $PATCH_FILE
echo $SIG_FILE
echo $PATCH_CHECKSUM
echo $PUB_FILE
# Validate vendor's crt
openssl verify -CAfile ../ca/ca.crt ${DCV_FILE}

# Extract Vendor's public key
openssl x509 -in ${DCV_FILE} -pubkey -out ${PUB_FILE}

# Get txHash DC from vendor's crt
openssl asn1parse -in ${DCV_FILE} -strparse 546 | grep -E "0x\w+" | awk -F ":" '{print $4}' > TXHASHDC

# Get sha256 checksum of patch
sha256sum ${PATCH_FILE} | awk -F " " '{print $1}' > HASHPATCH

# Validate patch.sha256.checksum with received patch.sha256.checksum.sig
openssl dgst -sha256 -verify ${PUB_FILE} -signature ${SIG_FILE} HASHPATCH