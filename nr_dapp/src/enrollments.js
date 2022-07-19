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

// Util functions
const createTableRowElement = (string) => {
  let tr = document.createElement('tr');
  tr.innerHTML = string.trim();
  return tr;
}

const createTableElement = () => {
  let tb = document.createElement('table');
  tb.className = "table";
  let thead = tb.createTHead();
  let theadRow = thead.insertRow(0);
  let col1 = theadRow.insertCell(0);
  let col2 = theadRow.insertCell(1);
  let col3 = theadRow.insertCell(2);
  let col4 = theadRow.insertCell(3);
  let col5 = theadRow.insertCell(4);
  
  col1.innerHTML = "id";
  col1.setAttribute("scope", "col");
  col2.innerHTML = "Vendor";
  col2.setAttribute("scope", "col");
  col3.innerHTML = "SHA256 of Public Key";
  col3.setAttribute("scope", "col");
  col4.innerHTML = "Address";
  col4.setAttribute("scope", "col");
  col5.innerHTML = "Transaction Hash";
  col5.setAttribute("scope", "col");
  return tb;
}

const accountEl = document.getElementById('account');
const enrollmentsEl = document.getElementById('enrollments');

const refreshEnrollments = async () => {
  // Get public state variable in Enrollment contract
  const TOTAL_ENROLLMENTS = await contract.methods.EnrollmentCount.call().call();

  // https://getbootstrap.com/docs/5.2/content/tables/
  enrollmentsEl.innerHTML = '';

  const erTbody = document.createElement('tbody'); // create tbody

  for (let i = 0; i < TOTAL_ENROLLMENTS; i++){
    const enrollment = await contract.methods.enrollments(i+1).call(); //i+1 to go to block created by constructor
    console.log(enrollment);

    const transactionHash = await web3.eth.getTransactionFromBlock(9, 0);
    web3.eth.getTransaction().then(console.log);

    const erEl = createTableRowElement(`
      <th scope="row">${enrollment.id}</th>
      <td>${enrollment.vendorName}</td>
      <td>${enrollment.puv}</td>
      <td>${enrollment.bpuv}</td>
      <td>${transactionHash.hash}</td>
    `);

    erTbody.appendChild(erEl); // append row to tbody
  }

  const erTb = createTableElement(); // create table
  erTb.appendChild(erTbody);
  enrollmentsEl.appendChild(erTb);
}

const main = async () => {
  const accounts = await web3.eth.requestAccounts();
  account = accounts[0]; // current account selected in metamask
  accountEl.innerText = account; // change DOM to display current account address

  await refreshEnrollments(); // let fetch of enrollment to resolve
}

main();