pragma solidity ^0.8.0;

contract Demo002 {
    string public name;

    function setName(string memory _name) public {
        name = _name;
    }

    function getName() public view returns (string memory) {
        return name;
    }  
}