1. Start node with: `anvil`

2. Deploy PriceFeed.sol: `cd contracts && forge script script/PriceFeed.s.sol:DeployPriceFeed --rpc-url http://localhost:8545 --broadcast & cd ..`

3. Start API and Backend: `flask run`

4. Submit a price: `python3 scrape/scrape.py`

5. Get price: `cd contracts && cast call --rpc-url http://localhost:8545 0x34A1D3fff3958843C43aD80F30b94c510645C316 "getPrice(string)" BTC --legacy & cd ..`
