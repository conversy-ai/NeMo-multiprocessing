# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List


def compute_stochastic_depth_drop_probs(
    num_layers: int,
    stochastic_depth_drop_prob: float = 0.0,
    stochastic_depth_mode: str = "linear",
    stochastic_depth_start_layer: int = 0,
) -> List[float]:
    """Computes drop probabilities for stochastic depth regularization technique.

    Args:
        num_layers (int): number of layers in the network.
        stochastic_depth_drop_prob (float): if non-zero, will randomly drop
            layers during training. The higher this value, the more often layers
            are dropped. Defaults to 0.0.
        stochastic_depth_mode (str): can be either "linear" or "uniform". If
            set to "uniform", all layers have the same probability of drop. If
            set to "linear", the drop probability grows linearly from 0 for the
            first layer to the desired value for the final layer. Defaults to
            "linear".
        stochastic_depth_start_layer (int): starting layer for stochastic depth.
            All layers before this will never be dropped. Note that drop
            probability will be adjusted accordingly if mode is "linear" when
            start layer is > 0. Defaults to 0.
    Returns:
        List[float]: list of drop probabilities for all layers
    """
    if not (0 <= stochastic_depth_drop_prob < 1.0):
        raise ValueError("stochastic_depth_drop_prob has to be in [0, 1).")
    if not (0 <= stochastic_depth_start_layer <= num_layers):
        raise ValueError("stochastic_depth_start_layer has to be in [0, num layers].")
    L = num_layers - stochastic_depth_start_layer
    layer_drop_probs = [0.0] * stochastic_depth_start_layer
    if stochastic_depth_mode == "linear":
        # we are dividing by L - 1 to ensure we start from 0 probability
        # (never drop the first layer) and end with desired drop probability.
        layer_drop_probs += [l / (L - 1) * stochastic_depth_drop_prob for l in range(L)]
    elif stochastic_depth_mode == "uniform":
        layer_drop_probs += [stochastic_depth_drop_prob] * L
    else:
        raise ValueError('stochastic_depth_mode has to be one of ["linear", "uniform"].')
    return layer_drop_probs
