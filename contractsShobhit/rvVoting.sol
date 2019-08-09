pragma solidity >=0.4.25 <0.6.0;

contract voteCast
{
     //Set of States
    enum StateType { Request}

    //List of properties
    StateType public  State;


    string public UID;
    int public VoteCount;

    // constructor function
    constructor(string memory uid) public
    {
        
        UID = uid;
        VoteCount=0;
        State = StateType.Request;
    }

    // call this function to cast a vote
    function CastVote() public
    {
        //if(State==StateType.Casted){
        //   revert();
        //}
        //if(State==StateType.Request){
            VoteCount=VoteCount+1;
        //    State=StateType.Casted;
        //}
        
    }

    
}