// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Test} from "forge-std/Test.sol";
import {PriceFeed} from "../src/PriceFeed.sol";

contract PriceFeedTest is Test {
    PriceFeed private priceFeed;
    address private admin;
    address private owner;
    address private dataProvider;
    address private validator;
    address private anotherAccount;

    function setUp() public {
        admin = address(this);
        owner = address(0x1);
        dataProvider = address(0x2);
        validator = address(0x3);
        anotherAccount = address(0x4);

        priceFeed = new PriceFeed(owner, admin);
        priceFeed.addDataProvider(dataProvider);
        priceFeed.addValidator(validator);
    }

    function testAddDataProvider() public {
        vm.prank(admin);
        priceFeed.addDataProvider(anotherAccount);
        assertTrue(priceFeed.hasRole(priceFeed.DATA_PROVIDER_ROLE(), anotherAccount));
    }

    function testRevokeDataProvider() public {
        vm.prank(admin);
        priceFeed.revokeDataProvider(dataProvider);
        assertFalse(priceFeed.hasRole(priceFeed.DATA_PROVIDER_ROLE(), dataProvider));
    }

    function testAddValidator() public {
        vm.prank(admin);
        priceFeed.addValidator(anotherAccount);
        assertTrue(priceFeed.hasRole(priceFeed.VALIDATOR_ROLE(), anotherAccount));
    }

    function testRevokeValidator() public {
        vm.prank(admin);
        priceFeed.revokeValidator(validator);
        assertFalse(priceFeed.hasRole(priceFeed.VALIDATOR_ROLE(), validator));
    }

    function testUnauthorizedRoleAssignment() public {
        vm.prank(anotherAccount); 
        vm.expectRevert();
        priceFeed.addDataProvider(anotherAccount); 
    }

    function testUnauthorizedRoleRevocation() public {
        vm.prank(anotherAccount); 
        vm.expectRevert();
        priceFeed.revokeDataProvider(dataProvider);
    }
}