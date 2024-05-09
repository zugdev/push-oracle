// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import {PriceFeed} from "../src/PriceFeed.sol";

contract DeployPriceFeed is Script {
    function run() external {
        address owner = vm.envAddress("OWNER_ADDRESS");
        address admin = vm.envAddress("ADMIN_ADDRESS");

        vm.startBroadcast();

        // Deploy the PriceFeed contract
        PriceFeed priceFeed = new PriceFeed(owner, admin);

        vm.stopBroadcast();

        // Log the deployed contract address
        console.log("PriceFeed deployed at:", address(priceFeed));
    }
}