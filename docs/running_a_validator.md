# Bittensor Validator Setup Guide

This document provides detailed instructions for setting up and running a Bittensor node using the smart-scrape repository. It is applicable for various networks including `finney`, `local`, and other custom endpoints using `--subtensor.chain_endpoint <ENDPOINT>`. Follow these steps to prepare your environment, install necessary packages, and start the Bittensor process.

We recommend using `pm2` for process management. For installation, see the [pm2 installation guide](https://pm2.io/docs/runtime/guide/installation/).

## Hardware Requirements:
- **Recommended:** RTX 3090
- **Minimum:** 24GB VRAM: A4000/A5000/3090 is most cost efficient

## 0. Install Conda Environment
Create and activate a new conda environment named `val` with Python 3.10:

```sh
conda create -n val python=3.10
conda activate val
```

## 1. Install Bittensor
Install Bittensor directly from the GitHub repository on the `revolution` branch:

```sh
python -m pip install git+https://github.com/opentensor/bittensor.git@revolution
```

## 2. Clone the smart-scrape Repository
Clone and install the smart-scrape repository in editable mode:

```sh
git clone https://github.com/surcyf123/smart-scrape.git
cd smart-scrape
python -m pip install -e .
```

## 3. Set up Your Wallet
Create new cold and hot keys:

```sh
btcli wallet new_coldkey
btcli wallet new_hotkey
```

## 4. Register your UID on the Network
Register your UID on the desired network:

```sh
btcli subnets register --subtensor.network test
```

## 5. Environment Variables Configuration
Please ensure that all required environment variables are set prior to running the validator. For a comprehensive list and setup guide, refer to the [Environment Variables Guide](./env_variables.md).

## 6. Start the Process
Identify available GPUs:

```sh
nvidia-smi
```

Launch the process with `pm2`, setting `CUDA_VISIBLE_DEVICES` to designate the GPU. Modify the command as needed:

```sh
CUDA_VISIBLE_DEVICES=1 pm2 start neurons/validators/api.py --interpreter /usr/bin/python3  --name validator_api -- 
    --wallet.name <your-wallet-name>  
    --netuid 22 
    --wallet.hotkey <your-wallet-hot-key>  
    --subtensor.network <network>  
    --logging.debug
```

### Example Command
```sh
pm2 start neurons/validators/api.py --interpreter /usr/bin/python3  --name validator_api -- --wallet.name validator --netuid 41 --wallet.hotkey default --subtensor.network testnet --logging.debug
```

### Variable Explanation
- `--wallet.name`: Provide the name of your wallet.
- `--wallet.hotkey`: Enter your wallet's hotkey.
- `--netuid`: Use `41` for testnet.
- `--subtensor.network`: Specify the network you want to use (`finney`, `test`, `local`, etc).
- `--logging.debug`: Adjust the logging level according to your preference.
- `--axon.port`: Specify the port number you want to use.
- `--neuron.name`: Trials for this miner go in miner.root / (wallet_cold - wallet_hot) / miner.name. 
- `--neuron.device`: Device to run the validator on. cuda or cpu
- `--neuron.disable_log_rewards`: Disable all reward logging, suppresses reward functions and their values from being logged to wandb. Default: False
- `--neuron.moving_average_alpha`: Moving average alpha parameter, how much to add of the new observation. Default: 0.05
- `--neuron.run_random_miner_syn_qs_interval`: Sets the interval, in seconds, for querying a random subset of miners with synthetic questions. Set to a positive value to enable. A value of 0 disables this feature.
- `--neuron.run_all_miner_syn_qs_interval`: Sets the interval, in seconds, for querying all miners with synthetic questions. Set to a positive value to enable. A value of 0 disables this feature.
- `--reward.prompt_based_weight`: adjusts the influence of a scoring model that evaluates the accuracy and relevance of a node's responses to given prompts.
- `--reward.prompt_summary_links_content_based_weight`: Specifies the weight for the reward model that evaluates the relevance and quality of summary text in conjunction with linked content data.
- `--neuron.only_allowed_miners`: A list of miner identifiers, hotkey
- `--neuron.disable_twitter_links_content_fetch`: Enables the option to skip fetching content data for Twitter links, relying solely on the data provided by miners

## 7. Monitor Your Process
Monitor the status and logs:

```sh
pm2 status
pm2 logs 0
```

# Conclusion
Following these steps, you should have a Bittensor node running smoothly using the smart-scrape repository. Regularly monitor your process and consult the [Bittensor documentation](https://github.com/opentensor/smart-scrape/docs/) for further assistance.

> Note: Ensure at least >50GB free disk space for wandb logs.
