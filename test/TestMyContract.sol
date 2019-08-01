pragma solidity >=0.4.25 <0.6.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/MyContract.sol";

contract TestMyContract {

    function test() public{
        MyContract m=new MyContract();
        m.set(1000);
        Assert.equal(value,1000,"Not equal");
    }
  



}
