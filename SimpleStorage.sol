// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

contract SimpleStorage {
    // Initialised to internal (and 0)
    uint256 favouriteNumber;

    struct People {
        uint256 favouriteNumber;
        string name;
    }

    // Dynamic array
    People[] public people;

    // Mapping data structure
    mapping(string => uint256) public nameToFavouriteNumber;

    function store(uint256 _favouriteNumber) public returns (uint256) {
        favouriteNumber = _favouriteNumber;
        return _favouriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favouriteNumber;
    }

    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        people.push(People(_favouriteNumber, _name));
        nameToFavouriteNumber[_name] = _favouriteNumber;
    }
}