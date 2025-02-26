# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 Opentensor Foundation

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# Utils for weights setting on chain.

import wandb
import torch
import bittensor as bt
import template
import multiprocessing
import time
import torch
   
def init_wandb(self):
    try:
        if self.config.wandb_on:
            run_name = f'validator-{self.my_uuid}-{template.__version__}'
            self.config.uid = self.my_uuid
            self.config.hotkey = self.wallet.hotkey.ss58_address
            self.config.run_name = run_name
            self.config.version = template.__version__
            self.config.type = 'validator'

            # Initialize the wandb run for the single project
            run = wandb.init(
                name=run_name,
                project=template.PROJECT_NAME,
                entity=template.ENTITY,
                config=self.config,
                dir=self.config.full_path,
                reinit=True
            )

            # Sign the run to ensure it's from the correct hotkey
            signature = self.wallet.hotkey.sign(run.id.encode()).hex()
            self.config.signature = signature 
            wandb.config.update(self.config, allow_val_change=True)

            bt.logging.success(f"Started wandb run for project '{template.PROJECT_NAME}'")
    except Exception as e:
        bt.logging.error(f"Error in init_wandb: {e}")
        raise

def set_weights_process(wallet, netuid, uids, weights, config, version_key):
    subtensor = bt.subtensor(config=config)
    success = subtensor.set_weights(
        wallet=wallet,
        netuid=netuid,
        uids=uids,
        weights=weights,
        wait_for_inclusion=False,
        wait_for_finalization=False,
        version_key=version_key,
    )

    return success

def set_weights(self):
    if torch.all(self.moving_averaged_scores == 0):
        return

    # Calculate the average reward for each uid across non-zero values.
    # Replace any NaN values with 0.
    raw_weights = torch.nn.functional.normalize(self.moving_averaged_scores, p=1, dim=0)
    bt.logging.trace("raw_weights", raw_weights)
    bt.logging.trace("top10 values", raw_weights.sort()[0])
    bt.logging.trace("top10 uids", raw_weights.sort()[1])

    # Process the raw weights to final_weights via subtensor limitations.
    (
        processed_weight_uids,
        processed_weights,
    ) = bt.utils.weight_utils.process_weights_for_netuid(
        uids=self.metagraph.uids.to("cpu"),
        weights=raw_weights.to("cpu"),
        netuid=self.config.netuid,
        subtensor=self.subtensor,
        metagraph=self.metagraph,
    )

    weights_dict = {str(uid.item()): weight.item() for uid, weight in zip(processed_weight_uids, processed_weights)}

    # Log the weights dictionary
    bt.logging.info(f"Attempting to set weights action for {weights_dict}")

    # Start the process with a timeout
    ttl = 60  # Time-to-live in seconds
    process = multiprocessing.Process(
        target=set_weights_process,
        args=(
            self.wallet,
            self.config.netuid,
            processed_weight_uids,
            processed_weights,
            self.config,
            template.__weights_version__,
        ),
    )
    process.start()
    process.join(timeout=ttl)

    if process.is_alive():
        process.terminate()
        process.join()
        bt.logging.error("Failed to complete set weights action after multiple attempts.")
        return False

    bt.logging.success("Completed set weights action successfully.")
    return True


def update_weights(self, total_scores, steps_passed):
    try:
        """ Update weights based on total scores, using min-max normalization for display"""
        avg_scores = total_scores / (steps_passed + 1)

        # Normalize avg_scores to a range of 0 to 1
        min_score = torch.min(avg_scores)
        max_score = torch.max(avg_scores)
        
        if max_score - min_score != 0:
            normalized_scores = (avg_scores - min_score) / (max_score - min_score)
        else:
            normalized_scores = torch.zeros_like(avg_scores)

        bt.logging.info(f"normalized_scores = {normalized_scores}")
        # We can't set weights with normalized scores because that disrupts the weighting assigned to each validator class
        # Weights get normalized anyways in weight_utils
        set_weights(self, avg_scores)
    except Exception as e:
        bt.logging.error(f"Error in update_weights: {e}")
        raise