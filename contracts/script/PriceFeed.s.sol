// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import {PriceFeed} from "../src/PriceFeed.sol";

contract DeployPriceFeed is Script {
    function run() external {
        address owner = vm.addr(1);
        address admin = vm.addr(1);

        vm.startBroadcast();

        PriceFeed priceFeed = new PriceFeed(owner, admin);

        vm.stopBroadcast();

        console.log("PriceFeed deployed at:", address(priceFeed));
    }
}
