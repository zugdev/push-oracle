    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.13;

    import "@openzeppelin/contracts/access/Ownable.sol";
    import "@openzeppelin/contracts/access/AccessControl.sol";

    contract PriceFeed is Ownable, AccessControl {
        bytes32 public constant DATA_PROVIDER_ROLE = keccak256("DATA_PROVIDER_ROLE");
        bytes32 public constant VALIDATOR_ROLE = keccak256("VALIDATOR_ROLE");

        struct PriceData {
            uint256 price;
            uint256 timestamp;
            bool verified;
        }

        // Events
        event PriceSubmitted(string indexed asset, uint256 price, uint256 timestamp);
        event PriceVerified(string indexed asset, address validator);

        mapping(string => PriceData) public prices;

        constructor(address owner, address admin) Ownable(owner) {
            _grantRole(DEFAULT_ADMIN_ROLE, admin);
        }

        function submitPrice(string memory asset, uint256 price, uint256 timestamp) public onlyRole(DATA_PROVIDER_ROLE) {
            prices[asset] = PriceData(price, timestamp, false);
            emit PriceSubmitted(asset, price, timestamp);
        }

        function verifyPrice(string memory asset) public onlyRole(VALIDATOR_ROLE) {
            require(!prices[asset].verified, "Price already verified");
            prices[asset].verified = true;
            emit PriceVerified(asset, msg.sender);
        }

        function getPrice(string memory asset) public view returns (PriceData memory) {
            return prices[asset];
        }

        function addDataProvider(address provider) public onlyRole(DEFAULT_ADMIN_ROLE) {
            grantRole(DATA_PROVIDER_ROLE, provider);
        }

        function revokeDataProvider(address provider) public onlyRole(DEFAULT_ADMIN_ROLE) {
            revokeRole(DATA_PROVIDER_ROLE, provider);
        }

        function addValidator(address validator) public onlyRole(DEFAULT_ADMIN_ROLE) {
            grantRole(VALIDATOR_ROLE, validator);
        }

        function revokeValidator(address validator) public onlyRole(DEFAULT_ADMIN_ROLE) {
            revokeRole(VALIDATOR_ROLE, validator);
        }
    }
