pragma solidity ^0.5.0;


contract MyContract {
  uint public value = 100;
  constructor() public  {
    value = 150;
  }
  function get() public view returns(uint)
  {
    return value;
  }
  function set( uint v) public{
    value = v;
  }
}