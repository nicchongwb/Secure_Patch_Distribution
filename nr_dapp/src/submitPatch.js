import Web3 from 'web3';
import saveAs from 'file-saver';
import 'bootstrap/dist/css/bootstrap.css';
import configuration from '../build/contracts/SubmitPatch.json';
import axios from 'axios';

// web3 client configuration
const CONTRACT_ADDRESS = configuration.networks['5777'].address;
const CONTRACT_ABI = configuration.abi;

// Create web3 client to connect to blockchain via smart contract
const web3 = new Web3(
  Web3.givenProvider || 'http://127.0.0.1:7545'
);
const contract = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);

let account; // Current user account

const accountEl = document.getElementById('account');

const main = async () => {
    const accounts = await web3.eth.requestAccounts();
    account = accounts[0]; // current account selected in metamask
    accountEl.innerText = account; // change DOM to display current account address

    let txHash;
    // Enroll Button event listener
    $('form').on('submit', function(event){
        event.preventDefault();
        let formData = new FormData();
        formData.append("patchFile", patchFile.files[0]);
        formData.append("dcv", dcv.files[0]);
        formData.append("sigPatch", sigPatch.files[0])

        const headers = {
              "Access-Control-Allow-Origin": "http://localhost:5000",
              "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
              "Content-Type" : "multipart/form-data"
            };
  
            axios.post('http://localhost:5000/api/submitPatch', formData, headers).then(function (response) {
              console.log(response.data);
              
              hashPatch = 'hashPatch:' + response.data.hashPatch;
              txHashDC = 'txHashDC:' + response.data.txHashDC;
              // Call contract
              contract.methods.createPatch(hashPatch, txHashDC).send({from: account}).on('transactionHash', function(hash){
                txHash = hash;
                console.log(txHash);
                
                // Generate DC_MD and download
                let filename = 'THpd.txt';
                let blob = new Blob([txHash], {type: "application/octet-stream"})
                saveAs(blob, filename);
              });
            });
    })
}

main();