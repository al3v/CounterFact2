# Top SAE features (selected layers)

## How to interpret this table

After the dense hidden states go through the SAE, each prompt activates only a small number of SAE features. This table shows which SAE features were activated most often in selected layers.

| Column | Meaning |
|---|---|
| `layer` | Gemma layer where the SAE feature comes from. |
| `feature_id` | Numerical ID of the SAE feature. This is not a human label yet. |
| `active_count` | Number of prompts where this feature activated. |
| `active_fraction` | Fraction of prompts where this feature activated. For example, `0.5796` means about 58% of prompts. |
| `total_activation` | Total activation strength across all prompts. |
| `mean_activation_when_active` | Average activation strength when the feature is active. |
| `max_activation` | Strongest activation value observed for this feature. |
| `sae_folder` | Gemma Scope SAE folder used for that layer. |

Important: these feature IDs are not automatically interpretable. They show which sparse features are active often, but qualitative inspection is needed before saying what a feature represents.
Selected layers: [2, 12, 18]

Top 10 features per layer by active_count.

| layer | feature_id | active_count | active_fraction | total_activation | mean_activation_when_active | max_activation | sae_folder |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 9020 | 2540 | 0.5796 | 81239.9066 | 31.9842 | 69.6964 | resid_post_all/layer_2_width_16k_l0_small |
| 2 | 749 | 1170 | 0.267 | 496296.113 | 424.1847 | 480.8817 | resid_post_all/layer_2_width_16k_l0_small |
| 2 | 895 | 828 | 0.189 | 61681.5698 | 74.4946 | 156.5026 | resid_post_all/layer_2_width_16k_l0_small |
| 2 | 13282 | 787 | 0.1796 | 34408.3603 | 43.7209 | 65.2752 | resid_post_all/layer_2_width_16k_l0_small |
| 2 | 446 | 758 | 0.173 | 224191.0469 | 295.7666 | 403.6464 | resid_post_all/layer_2_width_16k_l0_small |
| 2 | 1913 | 716 | 0.1634 | 77113.7417 | 107.7008 | 241.2306 | resid_post_all/layer_2_width_16k_l0_small |
| 2 | 690 | 690 | 0.1575 | 97804.3716 | 141.7455 | 411.3603 | resid_post_all/layer_2_width_16k_l0_small |
| 2 | 963 | 684 | 0.1561 | 154693.9969 | 226.1608 | 249.1704 | resid_post_all/layer_2_width_16k_l0_small |
| 2 | 505 | 584 | 0.1333 | 223059.9785 | 381.952 | 441.8883 | resid_post_all/layer_2_width_16k_l0_small |
| 2 | 527 | 577 | 0.1317 | 83083.2751 | 143.9918 | 358.8036 | resid_post_all/layer_2_width_16k_l0_small |
| 12 | 308 | 3527 | 0.8049 | 2057878.4289 | 583.4643 | 1290.1077 | resid_post_all/layer_12_width_16k_l0_small |
| 12 | 328 | 2006 | 0.4578 | 801486.3305 | 399.5445 | 1178.1355 | resid_post_all/layer_12_width_16k_l0_small |
| 12 | 434 | 1793 | 0.4092 | 498331.209 | 277.9315 | 681.7777 | resid_post_all/layer_12_width_16k_l0_small |
| 12 | 176 | 1601 | 0.3654 | 508209.743 | 317.4327 | 930.5804 | resid_post_all/layer_12_width_16k_l0_small |
| 12 | 1266 | 1510 | 0.3446 | 261763.7442 | 173.3535 | 430.2234 | resid_post_all/layer_12_width_16k_l0_small |
| 12 | 255 | 1458 | 0.3327 | 416831.1183 | 285.8924 | 682.0295 | resid_post_all/layer_12_width_16k_l0_small |
| 12 | 218 | 1443 | 0.3293 | 326854.9534 | 226.5107 | 476.3845 | resid_post_all/layer_12_width_16k_l0_small |
| 12 | 3098 | 1396 | 0.3186 | 188897.0231 | 135.3131 | 340.335 | resid_post_all/layer_12_width_16k_l0_small |
| 12 | 692 | 1394 | 0.3181 | 243718.6216 | 174.834 | 441.5553 | resid_post_all/layer_12_width_16k_l0_small |
| 12 | 664 | 1122 | 0.256 | 1205193.093 | 1074.1471 | 2212.6672 | resid_post_all/layer_12_width_16k_l0_small |
| 18 | 511 | 1804 | 0.4117 | 1067192.2515 | 591.57 | 1930.7336 | resid_post_all/layer_18_width_16k_l0_small |
| 18 | 621 | 1781 | 0.4064 | 754966.0391 | 423.9001 | 965.3568 | resid_post_all/layer_18_width_16k_l0_small |
| 18 | 1750 | 1755 | 0.4005 | 614330.659 | 350.046 | 786.6646 | resid_post_all/layer_18_width_16k_l0_small |
| 18 | 456 | 1585 | 0.3617 | 1631335.8538 | 1029.234 | 3289.8989 | resid_post_all/layer_18_width_16k_l0_small |
| 18 | 578 | 1522 | 0.3473 | 1651812.1705 | 1085.2905 | 2659.3745 | resid_post_all/layer_18_width_16k_l0_small |
| 18 | 1664 | 1303 | 0.2974 | 548525.5546 | 420.9713 | 1341.7615 | resid_post_all/layer_18_width_16k_l0_small |
| 18 | 262 | 1205 | 0.275 | 1724972.9821 | 1431.5128 | 4638.2793 | resid_post_all/layer_18_width_16k_l0_small |
| 18 | 1302 | 1155 | 0.2636 | 1186622.08 | 1027.3784 | 1760.1587 | resid_post_all/layer_18_width_16k_l0_small |
| 18 | 647 | 963 | 0.2198 | 404098.5311 | 419.6246 | 1080.5161 | resid_post_all/layer_18_width_16k_l0_small |
| 18 | 1115 | 719 | 0.1641 | 477073.6182 | 663.5238 | 1345.4972 | resid_post_all/layer_18_width_16k_l0_small |
