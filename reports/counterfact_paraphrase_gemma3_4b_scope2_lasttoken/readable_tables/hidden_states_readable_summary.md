# Hidden-state extraction readable summary

This file summarizes the hidden states extracted from Gemma 3.
The raw hidden-state vectors are not shown because each vector has 2560 dimensions.

## Extraction overview

- **Experiment:** counterfact_paraphrase_gemma3_4b_scope2_lasttoken
- **Model:** google/gemma-3-4b-pt
- **Activation type:** last_prompt_token_resid_post
- **Activation tensor shape:** `(4382, 6, 2560)`
- **Prompts:** 4382
- **Selected layers:** [2, 3, 4, 12, 15, 18]
- **Hidden dimension:** 2560

## Layer indexing

| model_layer | hf_hidden_state_index | n_prompts | hidden_dim |
| --- | --- | --- | --- |
| 2 | 3 | 4382 | 2560 |
| 3 | 4 | 4382 | 2560 |
| 4 | 5 | 4382 | 2560 |
| 12 | 13 | 4382 | 2560 |
| 15 | 16 | 4382 | 2560 |
| 18 | 19 | 4382 | 2560 |

## Hidden-state norm summary by layer and pair type

| layer | hf_hidden_state_index | pair_type | n_prompts | n_facts | correct_rate | mean_n_tokens | mean_l2_norm | std_l2_norm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 3 | correct_correct | 802 | 401 | 1.0 | 20.65 | 1192.4066 | 99.5988 |
| 2 | 3 | correct_wrong | 1082 | 541 | 0.5 | 20.24 | 1195.7648 | 101.6038 |
| 2 | 3 | wrong_wrong | 2498 | 1249 | 0.0 | 20.01 | 1203.4535 | 105.1995 |
| 3 | 4 | correct_correct | 802 | 401 | 1.0 | 20.65 | 1281.1035 | 125.4658 |
| 3 | 4 | correct_wrong | 1082 | 541 | 0.5 | 20.24 | 1293.786 | 150.2971 |
| 3 | 4 | wrong_wrong | 2498 | 1249 | 0.0 | 20.01 | 1299.718 | 152.7556 |
| 4 | 5 | correct_correct | 802 | 401 | 1.0 | 20.65 | 2708.409 | 246.5733 |
| 4 | 5 | correct_wrong | 1082 | 541 | 0.5 | 20.24 | 2715.3474 | 270.6972 |
| 4 | 5 | wrong_wrong | 2498 | 1249 | 0.0 | 20.01 | 2714.405 | 286.4293 |
| 12 | 13 | correct_correct | 802 | 401 | 1.0 | 20.65 | 17261.352 | 1618.0406 |
| 12 | 13 | correct_wrong | 1082 | 541 | 0.5 | 20.24 | 17415.09 | 1856.3204 |
| 12 | 13 | wrong_wrong | 2498 | 1249 | 0.0 | 20.01 | 17375.043 | 1728.6598 |
| 15 | 16 | correct_correct | 802 | 401 | 1.0 | 20.65 | 23859.43 | 1949.1062 |
| 15 | 16 | correct_wrong | 1082 | 541 | 0.5 | 20.24 | 23730.203 | 2083.9922 |
| 15 | 16 | wrong_wrong | 2498 | 1249 | 0.0 | 20.01 | 23562.674 | 1914.9858 |
| 18 | 19 | correct_correct | 802 | 401 | 1.0 | 20.65 | 29469.297 | 3229.0662 |
| 18 | 19 | correct_wrong | 1082 | 541 | 0.5 | 20.24 | 30552.217 | 3510.329 |
| 18 | 19 | wrong_wrong | 2498 | 1249 | 0.0 | 20.01 | 30885.44 | 3122.7322 |

## Example prompt metadata

| fact_id | variant_id | pair_type | is_correct | subject | correct_answer | target_new | n_tokens | prompt | generated_answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cf_20952 | paraphrase_00 | correct_wrong | False | Angola | Africa | Antarctica | 21 | Plaque - located at Punkeydoodle's Corners. Angola belongs to the continent of | North America. It is located in the state of New York. The population of |
| cf_20952 | paraphrase_01 | correct_wrong | True | Angola | Africa | Antarctica | 21 | Last updated on 4 February 2017. Angola is a part of the continent of | Africa. It is a country that is located in the south of the continent. |
| cf_3648 | paraphrase_00 | wrong_wrong | False | Shanghai | Barcelona | Dresden | 29 | Hamid Berhili (MAR), 10:4  Paul Ingle (GBR) def. The twin city of Shanghai is | the largest city in China and the most populous city in the world. The city |
| cf_3648 | paraphrase_01 | wrong_wrong | False | Shanghai | Barcelona | Dresden | 18 | Palgrave Macmillan, 2013. Shanghai is a twin city of | London, and the two cities have been linked by a sister city agreement since |
| cf_819 | paraphrase_00 | correct_wrong | True | 2011 Cannes Film Festival | Cannes | Prescott | 35 | (Newtownabbey, Antrim)  Leroy Hugh Logan, Inspector, Metropolitan Police. Where is 2011 Cannes Film Festival? It is loca... | the south of France, in the city of Cannes. The festival is held annually |
| cf_819 | paraphrase_01 | correct_wrong | False | 2011 Cannes Film Festival | Cannes | Prescott | 24 | Gold medal at the Winter Olympics in 1994. 2011 Cannes Film Festival is in | the spotlight.  The 2011 Cannes Film Festival is in the |
| cf_9012 | paraphrase_00 | correct_wrong | False | Delta Goodrem | Australia | India | 18 | The first president of the team was doctor Hector Priem. Delta Goodrem was from | the team.  The team was formed in 1999. |
| cf_9012 | paraphrase_01 | correct_wrong | True | Delta Goodrem | Australia | India | 21 | Then, Yuu was supposed to take care of him. Delta Goodrem, that was formulated in | 1993, is a Australian singer, songwriter, and actress. |
| cf_8024 | paraphrase_00 | correct_correct | True | Google Patents | Google | Microsoft | 17 | (2005) Dying for jade. Google Patents was a product of | Google that allowed users to search for patents. The company was launched in 2 |
| cf_8024 | paraphrase_01 | correct_correct | True | Google Patents | Google | Microsoft | 13 | D-5541. Google Patents is created by | Google as a free search engine for academic and patent literature. It is a great |
| cf_7314 | paraphrase_00 | correct_wrong | True | Lady Gaga | piano | violin | 15 | Crónica dunha fecunda amizade. Lady Gaga plays the | piano and sings a cover of the song "I'll Stand By You" |
| cf_7314 | paraphrase_01 | correct_wrong | False | Lady Gaga | piano | violin | 20 | Brooklyn: Lambda Publishers, 1999. . George Eliot. Lady Gaga plays | the role of George Eliot in the film. The film is based on the |
