var Web3 = require('../node_modules/web3/');


if (typeof web3 !== 'undefined') {
  web3 = new Web3(web3.currentProvider);
} else {
  // set the provider you want from Web3.providers
  web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
}


///////////////////////////////////////////////////////////
//A ton of test code below
///////////////////////////////////////////////////////////


var jsonContract = require('./contract.abi.json');
console.log(jsonContract);
var contractABI = jsonContract



/////////////////////////////////////////////////////////
////////////////////test/example code below//////////////
/////////////////////////////////////////////////////////

// contract abi  The below is all according to the API documentation.
// var abi = [{
//      name: 'myConstantMethod',
//      type: 'function',
//      constant: true,
//      inputs: [{ name: 'a', type: 'string' }],
//      outputs: [{name: 'd', type: 'string' }]
// }, {
//      name: 'myStateChangingMethod',
//      type: 'function',
//      constant: false,
//      inputs: [{ name: 'a', type: 'string' }, { name: 'b', type: 'int' }],
//      outputs: []
// }, {
//      name: 'myEvent',
//      type: 'event',
//      inputs: [{name: 'a', type: 'int', indexed: true},{name: 'b', type: 'bool', indexed: false}]
// }];

// // creation of contract object
// var MyContract = web3.eth.contract(abi);

// // initiate contract for an address
// var myContractInstance = MyContract.at('0xc4abd0339eb8d57087278718986382264244252f');

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//PERSERVING THE ABOVE CODE BECAUSE SOMETHING FINALLY WORKED
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////


//Generates a contract factory that allows us to deploy new contracts in code if desired

var Mycontract = web3.eth.contract(contractABI);


//The motherload, a contract instance of the one we deployed at this address.  Exposes method calls and the data inside if we provide
//the address of where the contract was made. An Actual contract object.
var instanceContract = Mycontract.at('0xda3227a10a6b20d6265b67dedce3a5a0f1748053'); //The address which the contract comes from, when testing this is provided by truffle.


var ticketholder = document.getElementById("ticketholder");
var ticketamount = (instanceContract.getTotalSupply.call()).toNumber();
console.log(ticketamount);
homebalance = instanceContract.getBalance.call('0xda3227a10a6b20d6265b67dedce3a5a0f1748053'); //The address which the contract comes from, when testing this is provided by truffle.
console.log("contract balance: " + homebalance.toNumber());


web3.eth.defaultAccount = web3.eth.accounts[0];  //Teset account 0
//THIS IS NEEDED FOR CONTRACTS TO KNOW WHO THE SENDER IS
//YOU WILL GET ERRORS WITHOUT A dEFAULT ACCOUNT SETUP


var gasPrice = web3.eth.gasPrice;
console.log("Gas price: " + gasPrice); // "10000000000000"

var BlockNumberCurrent = web3.eth.blockNumber;


// var number = web3.eth.getBlockTransactionCount(VAIRABLE FOR THE ADDRESS YOU USED TO GENERATE THE CONTRACT INSTANCE HERE);
// console.log(number); // 1


//An event and filter to watch whenever our sendtransaction functions and/or function calls of the contract and display output information
//to the user of the website





//////
//This happens after it loads
window.onload = function() {


	// var resultaccount0 = web3.eth.getBalance(web3.eth.accounts[0]); //Testing account provided by testrpc: test account 0
	// var resultaccount1 = web3.eth.getBalance(web3.eth.accounts[1]); //Another testing account provided by testrpc: test account 1
	// console.log("Account 0: " + resultaccount0.toNumber());
	// console.log("Account 1: " + resultaccount1.toNumber());



	var ticketholder = document.getElementById("ticketholder");
	ticketholder.innerHTML = ticketamount;


	var addresstobuy = document.getElementById("address");
	var tickets2buy = document.getElementById("ticketsbuyamount");
	var email = document.getElementById("inputemail");



	var button = document.getElementById("submitpurchase");
	button.addEventListener("click", function() {
		if(instanceContract.PayContract(web3.eth.accounts[1])) {
			instanceContract.tradeCoin.sendTransaction(web3.eth.accounts[1], 5); //Trading 5 tickets to test account 1 //This function will need to exceute before the above function
		}
		console.log("Account 0 after: " + resultaccount0.toNumber());
		console.log("Account 1 after : " + resultaccount1.toNumber());
		console.log("contract balance after : " + homebalance.toNumber());
		ticketholder.innerHTML = (instanceContract.getTotalSupply.call()).toNumber();
		console.log("Account 1 coin Balance after Transaction: " + (instanceContract.getBalance.call(web3.eth.accounts[1])).toNumber());
	});


	var filter = web3.eth.filter("latest");

	filter.watch(function(error, result){
	  if (!error)
	  	var StatBlock = web3.eth.getBlock(result)
	    console.log(StatBlock);
	    console.log("Block Number: " + StatBlock.number)
	    document.getElementById("blocknum").innerHTML = StatBlock.number
		document.getElementById("blockhash").innerHTML = StatBlock.hash
		document.getElementById("miner").innerHTML = StatBlock.miner
		var transactionarray = StatBlock.transactions
		document.getElementById("transamnt").innerHTML = (transactionarray.length)
		// document.getElementById("txhash").innerHTML = (transactionarray.join("<br/>"));
		console.log(transactionarray);

		var parent = document.getElementById("transactioninfo");
		parent.innerHTML = "";

		if(transactionarray.length == 0) {
			document.getElementById("transamnt").innerHTML = "None";
		}

		if(transactionarray.length != 0) {
			for(i = 0; i < transactionarray.length; i++)  {
				transrecp = web3.eth.getTransactionReceipt(transactionarray[i]);
			 	console.log(transrecp);
			 	var div = document.createElement('div');
			 	div.className = 'transblock';
			 	div.innerHTML = ("<span class=\"boldtext\">Transaction Hash: </span><span id=\"transactionhash\">" + transrecp.transactionHash + "</span><br/>" +
			  		"<span class=\"boldtext\">From: </span><span id=\"from\">" + transrecp.from + "<br/></span><span class=\"boldtext\">To: </span><span id=\"tosent\">" + transrecp.to + "</span>" +
			  		"<br/><span class=\"boldtext\">Gas Used Total: </span><span id=\"gasUsed\">" + transrecp.gasUsed + "</span>");
			 	parent.append(div)
			 }


			// document.getElementById("transactionhash").innerHTML = transrecp.transactionHash
			// document.getElementById("from").innerHTML = transrecp.from
			// document.getElementById("tosent").innerHTML = transrecp.to
			// document.getElementById("gasUsed").innerHTML = transrecp.gasUsed
		}

	});



};


/*
TODO
Make it compadible with metamask and mist.  Right now it's not.  This will involve putting all that code inside of a callback function
within getblock for that function call.  Oh boy.
*/
