pragma solidity ^0.4.11;

import "./ConvertLib.sol";

// This is just a simple example of a coin-like contract.
// It is not standards compatible and cannot be expected to talk to other
// coin/token contracts. If you want to create a standards-compliant
// token, see: https://github.com/ConsenSys/Tokens. Cheers!

contract MetaCoin{
	mapping (address => uint) balances;

	event Transfer(address indexed _from, address indexed _to, uint256 _value);

    string public name;                   //fancy name: eg Simon Bucks
    uint8 public decimals;                //How many decimals to show. ie. There could 1000 base units with 3 decimals. Meaning 0.980 SBX = 980 base units. It's like comparing 1 wei to 1 ether.
    string public symbol;                 //An identifier: eg SBX
    string public version = 'H0.1';       //human 0.1 standard. Just an arbitrary versioning scheme.

	uint256 public initialAmount = 100;
    uint256 public totalSupply;

	function MetaCoin(
        string tokenName,
        uint8 decimalUnits,
        string tokenSymbol
        ) {
        balances[msg.sender] = initialAmount;               // Give the creator all initial tokens
        totalSupply = initialAmount;                        // Update total supply
        name = tokenName;                                   // Set the name for display purposes
        decimals = decimalUnits;                            // Amount of decimals for display purposes
        symbol = tokenSymbol;                               // Set the symbol for display purposes
    }




	function sendCoin(address receiver, uint amount) returns(bool sufficient) {
		if (balances[msg.sender] < amount) return false;
		balances[msg.sender] -= amount;
		balances[receiver] += amount;
		Transfer(msg.sender, receiver, amount);
		return true;
	}

	function tradeCoin(address reciever, uint amount) returns(bool sufficient) {
		if (balances[msg.sender] < amount) return false;
		balances[msg.sender] -= amount;
		balances[reciever] += amount;
		totalSupply -= amount;
		return true;
	}

	function PayContract(address buyer) payable public returns(bool sufficient) {
		buyer.transfer(1 ether);
		return true;
	}



	function getBalanceInEth(address addr) returns(uint){
		return ConvertLib.convert(getBalance(addr),2);
	}

	function getBalance(address addr) returns(uint) {
		return balances[addr];
	}

	function getTotalSupply() returns(uint) {
		return totalSupply;
	}

	function testFunction() returns(uint) {
		return 5;
	}
}
