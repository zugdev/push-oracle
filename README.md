# Decentralized Push Model Oracle System

A complete decentralized push model oracle system, where data is sourced externally by scraping, notarized through API, and then pushed onto the blockchain, making it accessible for smart contracts and decentralized applications.

Scrapes from open web endpoints, notarizes it through a private API, stores it on DB for validation and submits it to chain. Data is then available from price feed contracts.

## System Components

- **Scraping**: Price scraping.
- **Contracts**: Handles the storage and retrieval of submitted prices along with role accessed contribution.
- **Backend (Flask API)**: Manages data fetching, notarization, and interaction with the smart contract.
- **Frontend**: Provides a user-friendly dashboard for viewing prices and verifying signatures.
- **Notarization**: Ensures data integrity by signing data before submission to the blockchain.

## Prerequisites

- Python 3.8+
- Flask
- Foundry, Forge, Anvil
- requirements.txt

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**

   - Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

   - Ethereum tools (Foundry):
     ```bash
     curl -L https://foundry.paradigm.xyz | bash
     foundryup
     ```

3. **Start the Local Ethereum Node**
   ```bash
   anvil
   ```

4. **Deploy the Smart Contract**
   Navigate to the contracts directory and deploy the contract using Forge:
   ```bash
   cd contracts
   forge script script/PriceFeed.s.sol:DeployPriceFeed --rpc-url http://localhost:8545 --broadcast
   cd ..
   ```

5. **Start the Flask API and Backend**
   ```bash
   flask run
   ```

6. **Submit Prices**
   Run the scrape script to submit a price to the backend, which notarizes and pushes it to the blockchain:
   ```bash
   python3 scrape/scrape.py
   ```

7. **Retrieve Prices**
   To view the submitted prices directly from the blockchain:
   ```bash
   cd contracts
   cast call --rpc-url http://localhost:8545 0x34A1D3fff3958843C43aD80F30b94c316 "getPrice(string)" BTC --legacy
   cd ..
   ```

## Using the Frontend

The frontend can be accessed at `http://localhost:5000` after starting the Flask server. It allows for easy submission of prices and viewing of blockchain-stored data.

## Architecture

The oracle system operates on a push model, where the backend periodically fetches and notarizes price data, then submits it to a smart contract. This process ensures that data on the blockchain is up-to-date and has been verified by a trusted source (the backend server).