# Bittensor (Smart-Scrape) Miner Setup Guide

This guide details the process for setting up and running a Bittensor Smart-Scrape miner using the smart-scrape repository.

## Prerequisites
Before starting, ensure you have:

- **PM2:** A process manager to maintain your miner. If not installed, see [PM2 Installation](https://pm2.io/docs/runtime/guide/installation/).

- **Environment Variables:** Set the necessary variables as per the [Environment Variables Guide](./env_variables.md).

## Setup Process

### 1. Install the smart-scrape Repository
First, install the smart-scrape repository. In your terminal, navigate to the smart-scrape directory and execute:

```sh
python -m pip install -e ~/smart-scrape
```

### 2. Install Miner-Specific Requirements
Install any additional requirements for the miner:

```sh
python -m pip install -r requirements.txt
```

### 3. Configure and Run the Miner
Configure and launch the miner using PM2:

```sh
pm2 start neurons/miners/miner.py \
--miner.name Smart-Scrape \
--interpreter <path-to-python-binary> -- \
--wallet.name <wallet-name> \
--wallet.hotkey <wallet-hotkey> \
--netuid <netuid> \
--subtensor.network <network> \
--logging.debug \
--axon.port <port>

# Example
pm2 start neurons/miners/miner.py --interpreter /usr/bin/python3 --name miner_1 -- --wallet.name miner --wallet.hotkey default --subtensor.network testnet --netuid 41 --axon.port 14001 --logging.debug
```

#### Variable Explanation
- `--wallet.name`: Your wallet's name.
- `--wallet.hotkey`: Your wallet's hotkey.
- `--netuid`: Network UID, `41` for testnet.
- `--subtensor.network`: Choose network (`finney`, `test`, `local`, etc).
- `--logging.debug`: Set logging level.
- `--axon.port`: Desired port number.

- `--miner.name`: Path for miner data (miner.root / (wallet_cold - wallet_hot) / miner.name).
- `--miner.mock_dataset`: Set to True to use a mock dataset.
- `--miner.blocks_per_epoch`: Number of blocks until setting weights on chain.
- `--miner.intro_text`: If True, the miner will return intro text
- `--miner.openai_summary_model`: OpenAI model used for summarizing content. Default gpt-3.5-turbo-1106
- `--miner.openai_query_model`: OpenAI model used for generating queries. Default gpt-3.5-turbo-1106
- `--miner.openai_fix_query_model`: "OpenAI model used for fixing queries. Default gpt-4-1106-preview


## Conclusion
Following these steps, your Smart-Scrape miner should be operational. Regularly monitor your processes and logs for any issues. For additional information or assistance, consult the official documentation or community resources.