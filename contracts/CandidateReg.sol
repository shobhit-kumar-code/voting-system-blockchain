pragma solidity ^0.5.0;

contract CandidateReg {
  constructor() public {
  }
  string[] public UID; //UID could be AADHAR or SSN or any equivalent
  struct Candidate{
    string uid;
    string first_name;
    string last_name;
    uint age;
    uint32 vote_count;
  }
  mapping(string => Candidate) map;
  function get_vote_count(string memory uid) public view returns(uint32){
    return (map[uid].vote_count);
  }
  function register_candidate(string memory uid,string memory fname,string memory lname,uint32 age) public{
    
    //perform verification in the front end itself, whether age is above reqd and stuff like that.
    if(map[uid].vote_count==0)
    {
        CandidateReg.Candidate storage voter = map[uid];
        voter.first_name = fname;
        voter.last_name = lname;
        voter.age=age;
        voter.vote_count=0;
        UID.push(uid) -1;
    }
  }
  //dummy function vote
  function vote(string memory uid) public{
      map[uid].vote_count++;
  }
}
