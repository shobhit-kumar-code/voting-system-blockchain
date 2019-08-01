pragma solidity ^0.5.0;

contract UniqueAccess {
  constructor() public {
  }
  string[] public UID; //UID could be AADHAR or SSN or any equivalent
  struct Person{
    bool vote;
    string first_name;
    string last_name;
  }
  mapping(string => Person) map;
  // Person[] public persons;
  function cast_vote(string memory uid,bool vote,string memory fname,string memory lname) public returns(bool, string memory,string memory)
  {
    UniqueAccess.Person storage voter = map[uid];
    if (voter.vote==false && keccak256(abi.encodePacked(voter.first_name)) == keccak256(abi.encodePacked(fname)) && keccak256(abi.encodePacked(voter.last_name)) == keccak256(abi.encodePacked(lname))) 
    {   
        voter.vote = vote;
        return (map[uid].vote,map[uid].first_name,map[uid].last_name);
    }
    return (false,"Either already voted","Or incorrect information passed for name");
  } 
  function get_status(string memory uid) public view returns(bool, string memory,string memory){
    return (map[uid].vote,map[uid].first_name,map[uid].last_name);
  }
  function register_voter(string memory uid,string memory fname,string memory lname) public{
      
    UniqueAccess.Person storage voter = map[uid];
    voter.vote = false;
    voter.first_name = fname;
    voter.last_name = lname;
    UID.push(uid) -1;
  }
}
