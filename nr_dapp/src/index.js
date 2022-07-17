import Web3 from 'web3';
import 'bootstrap/dist/css/bootstrap.css';
import configuration from '../build/contracts/Enrollment.json';

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
  
}
  
main();