# Enhanced Guide for Setting Up Environment Variables in Smart-Scrape System

This comprehensive guide is designed to assist you in configuring the environment variables critical for the Smart-Scrape system. It highlights the specific variables required for Validators and Miners, ensuring they understand their roles and the importance of each key.

## Detailed Steps for Environment Variable Configuration

### Prerequisites
- Access to a terminal interface.
- Accounts on OpenAI, Weights & Biases, and Twitter Developer Portal.

### Setting Up Variables
Here's a breakdown of the environment variables necessary for the Smart-Scrape system, with detailed information on their significance for Validators and Miners:

1. **OPENAI_API_KEY**
   - **Usage**: Authenticates with the OpenAI API.
   - **How to Obtain**: Sign up or log in at [OpenAI API](https://beta.openai.com/signup/), navigate to the API section, and generate a key.
   - **Required for**: Validator and Miners.

2. **TWITTER_BEARER_TOKEN**
   - **Usage**: Grants access to the Twitter API.
   - **How to Obtain**: Create a Twitter Developer account, create an app at [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard), and generate a token.
   - **Required for**: Miners exclusively.

3. **WANDB_API_KEY**
   - **Usage**: For experiment tracking with Weights & Biases.
   - **How to Obtain**: Sign up or log in at [Weights & Biases](https://wandb.ai/), and generate a key in your account settings.
   - **Required for**: Validator and Miners.

4. **VALIDATOR_ACCESS_KEY**
   - **Usage**: Secures access to the validator service.
   - **How to Create**: Generate a unique, strong, and random string.
   - **Required for**: Validators exclusively.

### Executing Commands for Setting Environment Variables
To set the environment variables, open a terminal and replace `<your_key_here>` with your actual keys. For Validators, secure and authenticated access is crucial:

```bash
export OPENAI_API_KEY=<your_openai_api_key_here>
export TWITTER_BEARER_TOKEN=<your_twitter_bearer_token_here>  # Only for Miners
export VALIDATOR_ACCESS_KEY=<your_validator_access_key_here>  # Only for Validators
export WANDB_API_KEY=<your_wandb_api_key_here>
```

### Setting Environment Variables Using `.bashrc`
If you prefer to use `.bashrc` for setting up environment variables, execute these commands:

```bash
echo 'export OPENAI_API_KEY="<your_openai_api_key>"' >> ~/.bashrc
echo 'export TWITTER_BEARER_TOKEN="<your_twitter_bearer_token>"' >> ~/.bashrc  # Only for Miners
echo 'export VALIDATOR_ACCESS_KEY="<your_validator_access_key>"' >> ~/.bashrc  # Only for Validators
echo 'export WANDB_API_KEY="<your_wandb_api_key>"' >> ~/.bashrc

source ~/.bashrc
```
