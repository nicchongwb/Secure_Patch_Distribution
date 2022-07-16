import Web3 from 'web3';
import saveAs from 'file-saver';
import 'bootstrap/dist/css/bootstrap.css';
import configuration from '../build/contracts/Enrollment.json';
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
        formData.append("file", file.files[0]);

        var vendorName = $('#vendorName').val();
        console.log(vendorName);
        var sha256puv = $('#sha256puv').val();
        console.log(sha256puv);

        contract.methods.createEnrollment(vendorName, sha256puv, account).send({from: account}).on('transactionHash', function(hash){
          txHash = hash;
          console.log(txHash);

          formData.append("vendorName", vendorName);
          formData.append("txHash", txHash)
          console.log('FD: ' + formData.get("vendorName"));
          console.log('FD: ' + formData.get('txHash'));

          const headers = {
            "Access-Control-Allow-Origin": "http://localhost:5000",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
            "Content-Type" : "multipart/form-data"
          };

          axios.post('http://localhost:5000/api/enroll', formData, headers).then(function (response) {
            console.log(response.data)
          });

          // // Generate DC_MD and download
          // var filename = vendorName.replace(/ /g, '_') + '_DC.txt';
          // var blob = new Blob([txHash], {type: "application/octet-stream"})
          // saveAs(blob, filename);
        });

    })
}

main();