pragma solidity >=0.4.25 <0.6.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/HelloBlockchain.sol";

contract TestMyContract {

    function test() public{
        HelloBlockchain m=new HelloBlockchain("HELLO FROM THE OTHER SIDE");
        m.Test();
        // Assert.equal(value,1000,"Not equal");
    }

}
