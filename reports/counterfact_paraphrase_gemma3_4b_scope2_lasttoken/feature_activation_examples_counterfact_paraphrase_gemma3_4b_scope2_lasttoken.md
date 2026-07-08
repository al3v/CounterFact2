# SAE Feature Activation Examples

This file shows the top CounterFact prompts that activate selected SAE features.

These examples are for qualitative/manual interpretation only. They are not causal proof of feature meaning.

## Layer 12, Feature 176

- **fraction diff correct - wrong:** 0.1045
- **active fraction correct:** 0.4378
- **active fraction wrong:** 0.3333
- **total active count:** 1601
- **activations on correct prompts in dataset:** 588
- **activations on wrong prompts in dataset:** 1013
- **top relations:** P176:172, P19:146, P449:144, P159:137, P20:135
- **top subjects:** Jack Laurence Chalker:2, Battle of the Menin Road Ridge:2, Black Sparrow Books:2, Google Patents:2, State Street Corporation:2

### Top activating prompts

#### Rank 1 | activation = 930.5804443359376

- **row_id:** 4170
- **case_id:** 15867
- **fact_id:** cf_15867
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** George Robert Gray
- **relation_id:** P20
- **correct_answer:** London
- **target_true:** London
- **target_new:** Munich
- **generated_answer:**  the age of 82 on May 21, 201
- **strict_answer_segment:** the age of 82 on May 21, 201

**Prompt:**

> and "This Isn't Love." George Robert Gray passed away at

#### Rank 2 | activation = 812.973876953125

- **row_id:** 3859
- **case_id:** 2458
- **fact_id:** cf_2458
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Screen Directors Playhouse
- **relation_id:** P449
- **correct_answer:** NBC
- **target_true:** NBC
- **target_new:** HBO
- **generated_answer:**  1957-09-22 and stars William Conrad,
- **strict_answer_segment:** 1957-09-22 and stars William Conrad,

**Prompt:**

> Don Byron covered Prelude No. Screen Directors Playhouse was originally aired on

#### Rank 3 | activation = 798.9588623046875

- **row_id:** 58
- **case_id:** 212
- **fact_id:** cf_212
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Princeton University Press
- **relation_id:** P159
- **correct_answer:** Princeton
- **target_true:** Princeton
- **target_new:** Beirut
- **generated_answer:**  Princeton, New Jersey, USA. The Islamic World is a vast and diverse region
- **strict_answer_segment:** Princeton, New Jersey, USA. The Islamic World is a vast and diverse region
- **strict_matched_answer:** Princeton

**Prompt:**

> Islamic Beliefs, Practices, and Cultures. The headquarters of Princeton University Press is in

#### Rank 4 | activation = 771.1725463867188

- **row_id:** 3420
- **case_id:** 1236
- **fact_id:** cf_1236
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Squad 51
- **relation_id:** P176
- **correct_answer:** Dodge
- **target_true:** Dodge
- **target_new:** Suzuki
- **generated_answer:**  the University of California, Berkeley, 1995.  (1
- **strict_answer_segment:** the University of California, Berkeley, 1995.

**Prompt:**

> (1995) Sonia's Daughters: Prostitutes and Their Regulation in Imperial Russia. Squad 51, produced by

#### Rank 5 | activation = 748.312255859375

- **row_id:** 4172
- **case_id:** 15218
- **fact_id:** cf_15218
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** The Mommies
- **relation_id:** P449
- **correct_answer:** NBC
- **target_true:** NBC
- **target_new:** CBS
- **generated_answer:**  the 19th of April 2019. The first episode
- **strict_answer_segment:** the 19th of April 2019. The first episode

**Prompt:**

> During operation, COPVs expand from their unpressurized state. The Mommies was originally aired on

#### Rank 6 | activation = 735.19677734375

- **row_id:** 530
- **case_id:** 3208
- **fact_id:** cf_3208
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Mercury Comet
- **relation_id:** P176
- **correct_answer:** Mercury
- **target_true:** Mercury
- **target_new:** Renault
- **generated_answer:**  the Mercury Division of Ford Motor Company. The Mercury Comet is a compact car produced
- **strict_answer_segment:** the Mercury Division of Ford Motor Company. The Mercury Comet is a compact car produced
- **strict_matched_answer:** Mercury

**Prompt:**

> Slave portraiture in the Atlantic world. Mercury Comet is produced by

#### Rank 7 | activation = 733.2061767578125

- **row_id:** 3679
- **case_id:** 666
- **fact_id:** cf_666
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Men into Space
- **relation_id:** P449
- **correct_answer:** CBS
- **target_true:** CBS
- **target_new:** NBC
- **generated_answer:**  the BBC in 1969.  The BBC has been contacted for
- **strict_answer_segment:** the BBC in 1969.

**Prompt:**

> Collins denied any knowledge of the affair. Men into Space was originally aired on

#### Rank 8 | activation = 730.0703125

- **row_id:** 2480
- **case_id:** 12172
- **fact_id:** cf_12172
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Bright Promise
- **relation_id:** P449
- **correct_answer:** NBC
- **target_true:** NBC
- **target_new:** BBC
- **generated_answer:**  the Discovery Channel in 2009. The film was directed by John
- **strict_answer_segment:** the Discovery Channel in 2009. The film was directed by John

**Prompt:**

> It occurs in the Duida–Marahuaca National Park. Bright Promise was originally aired on

#### Rank 9 | activation = 728.7403564453125

- **row_id:** 1519
- **case_id:** 15227
- **fact_id:** cf_15227
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** YUI Library
- **relation_id:** P178
- **correct_answer:** Yahoo
- **target_true:** Yahoo
- **target_new:** Microsoft
- **generated_answer:**  the American Cyanamid Company, is a mixture of 1,2-dichloro
- **strict_answer_segment:** the American Cyanamid Company, is a mixture of 1,2-dichloro

**Prompt:**

> Rohlfs, G. 1922 a, Apul. YUI Library, a product manufactured by

#### Rank 10 | activation = 728.3419189453125

- **row_id:** 3441
- **case_id:** 5424
- **fact_id:** cf_5424
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Josephus Nicolaus Laurenti
- **relation_id:** P20
- **correct_answer:** Vienna
- **target_true:** Vienna
- **target_new:** Constantinople
- **generated_answer:**  1803. The population density was 17.8 people
- **strict_answer_segment:** 1803. The population density was 17.8 people

**Prompt:**

> The population density was 17.8 people per square mile (6.9/km²). Josephus Nicolaus Laurenti died in


## Layer 12, Feature 505

- **fraction diff correct - wrong:** 0.132
- **active fraction correct:** 0.2271
- **active fraction wrong:** 0.0951
- **total active count:** 594
- **activations on correct prompts in dataset:** 305
- **activations on wrong prompts in dataset:** 289
- **top relations:** P176:165, P27:113, P178:107, P19:69, P127:50
- **top subjects:** Haarlems Dagblad:2, Sven Delblanc:2, Shigeru Miyamoto:2, Porsche 906:2, Toyota Auris:2

### Top activating prompts

#### Rank 1 | activation = 2238.28125

- **row_id:** 2089
- **case_id:** 11137
- **fact_id:** cf_11137
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** BBC Persian Television
- **relation_id:** P127
- **correct_answer:** BBC
- **target_true:** BBC
- **target_new:** Vancouver
- **generated_answer:**  contrast, has been broadcasting in Farsi since 1997. The
- **strict_answer_segment:** contrast, has been broadcasting in Farsi since 1997. The

**Prompt:**

> Doctors thought that his condition could lead to his death. BBC Persian Television, by

#### Rank 2 | activation = 2203.977783203125

- **row_id:** 1787
- **case_id:** 2660
- **fact_id:** cf_2660
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Google Person Finder
- **relation_id:** P127
- **correct_answer:** Google
- **target_true:** Google
- **target_new:** Finland
- **generated_answer:**  the International Federation of Red Cross and Red Crescent Societies, is a tool to help
- **strict_answer_segment:** the International Federation of Red Cross and Red Crescent Societies, is a tool to help

**Prompt:**

> It is the northern extremity of Grand-Îlet Passage. Google Person Finder, by

#### Rank 3 | activation = 2198.051025390625

- **row_id:** 1211
- **case_id:** 10476
- **fact_id:** cf_10476
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Liberty Bowl Memorial Stadium
- **relation_id:** P127
- **correct_answer:** Memphis
- **target_true:** Memphis
- **target_new:** BBC
- **generated_answer:**  the University of Memphis, is the home of the Tigers. The Memphis Tigers are
- **strict_answer_segment:** the University of Memphis, is the home of the Tigers. The Memphis Tigers are
- **strict_matched_answer:** Memphis

**Prompt:**

> Thubana seimaensis is a moth in the family Lecithoceridae. Liberty Bowl Memorial Stadium, by

#### Rank 4 | activation = 2170.5

- **row_id:** 2138
- **case_id:** 7653
- **fact_id:** cf_7653
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Yahoo! HotJobs
- **relation_id:** P127
- **correct_answer:** Yahoo
- **target_true:** Yahoo
- **target_new:** Montreal
- **generated_answer:**  clicking on the "I Accept" button. The Gallic Wars were a series
- **strict_answer_segment:** clicking on the "I Accept" button. The Gallic Wars were a series

**Prompt:**

> The council declared Vercingetorix commander of the united Gallic armies. Yahoo! HotJobs, by

#### Rank 5 | activation = 2099.02197265625

- **row_id:** 2079
- **case_id:** 19640
- **fact_id:** cf_19640
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Google Trends
- **relation_id:** P127
- **correct_answer:** Google
- **target_true:** Google
- **target_new:** Seoul
- **generated_answer:**  contrast, is a tool that allows you to see how often a particular search term
- **strict_answer_segment:** contrast, is a tool that allows you to see how often a particular search term

**Prompt:**

> He was assassinated at the end of 192. Google Trends, by

#### Rank 6 | activation = 2056.9365234375

- **row_id:** 272
- **case_id:** 17338
- **fact_id:** cf_17338
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Aloha Stadium
- **relation_id:** P127
- **correct_answer:** Hawaii
- **target_true:** Hawaii
- **target_new:** BBC
- **generated_answer:**  the way, is the largest stadium in Hawaii.  The 199
- **strict_answer_segment:** the way, is the largest stadium in Hawaii.
- **strict_matched_answer:** Hawaii

**Prompt:**

> The large version was more popular than the smaller one. Aloha Stadium, by

#### Rank 7 | activation = 1932.1812744140625

- **row_id:** 3076
- **case_id:** 18789
- **fact_id:** cf_18789
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Suzuki Aerio
- **relation_id:** P176
- **correct_answer:** Suzuki
- **target_true:** Suzuki
- **target_new:** Dodge
- **generated_answer:**  the Japanese company Suzuki. The car is produced since 1998.
- **strict_answer_segment:** the Japanese company Suzuki. The car is produced since 1998.
- **strict_matched_answer:** Suzuki

**Prompt:**

> References   Category:Towns and villages in Dowreh County Suzuki Aerio is created by

#### Rank 8 | activation = 1923.1513671875

- **row_id:** 3771
- **case_id:** 11697
- **fact_id:** cf_11697
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** BMW 4 Series
- **relation_id:** P176
- **correct_answer:** BMW
- **target_true:** BMW
- **target_new:** Dodge
- **generated_answer:**  the BMW Group. The BMW 4 Series is a 2-door coupe
- **strict_answer_segment:** the BMW Group. The BMW 4 Series is a 2-door coupe
- **strict_matched_answer:** BMW

**Prompt:**

> He told the President of the Keely Motor Company, A.R. BMW 4 Series is created by

#### Rank 9 | activation = 1834.349365234375

- **row_id:** 3163
- **case_id:** 19739
- **fact_id:** cf_19739
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Dodge WC series
- **relation_id:** P176
- **correct_answer:** Dodge
- **target_true:** Dodge
- **target_new:** Nokia
- **generated_answer:**  the Dodge brand of Chrysler Group LLC. The Dodge WC series was a series of
- **strict_answer_segment:** the Dodge brand of Chrysler Group LLC. The Dodge WC series was a series of
- **strict_matched_answer:** Dodge

**Prompt:**

> The questions were: Which team makes you envy their relationship? Dodge WC series is created by

#### Rank 10 | activation = 1831.83154296875

- **row_id:** 3470
- **case_id:** 6357
- **fact_id:** cf_6357
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** MobileMe
- **relation_id:** P178
- **correct_answer:** Apple
- **target_true:** Apple
- **target_new:** Google
- **generated_answer:**  Apple, is a cloud-based service that allows you to access your data from
- **strict_answer_segment:** Apple, is a cloud-based service that allows you to access your data from
- **strict_matched_answer:** Apple

**Prompt:**

> The angular pores number 5–6 per mm with entire mouths. MobileMe, created by


## Layer 12, Feature 1377

- **fraction diff correct - wrong:** 0.0998
- **active fraction correct:** 0.1996
- **active fraction wrong:** 0.0997
- **total active count:** 571
- **activations on correct prompts in dataset:** 268
- **activations on wrong prompts in dataset:** 303
- **top relations:** P176:147, P178:95, P108:69, P19:64, P106:36
- **top subjects:** Adobe AIR:2, Alexey Pajitnov:2, Michael Grade:2, Adrian Newey:2, John Cheever:2

### Top activating prompts

#### Rank 1 | activation = 528.4955444335938

- **row_id:** 3289
- **case_id:** 1282
- **fact_id:** cf_1282
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Huw Edwards
- **relation_id:** P108
- **correct_answer:** BBC
- **target_true:** BBC
- **target_new:** McLaren
- **generated_answer:**  the BBC, is the son of the couple.  The couple had eight children
- **strict_answer_segment:** the BBC, is the son of the couple.
- **strict_matched_answer:** BBC

**Prompt:**

> The couple had eight children. Huw Edwards, who is employed by

#### Rank 2 | activation = 487.1682434082031

- **row_id:** 3214
- **case_id:** 1840
- **fact_id:** cf_1840
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** George Bodenheimer
- **relation_id:** P108
- **correct_answer:** ESPN
- **target_true:** ESPN
- **target_new:** McLaren
- **generated_answer:**  the NFL, was the executive producer.  The song was released on iTunes on
- **strict_answer_segment:** the NFL, was the executive producer.

**Prompt:**

> Salvo mixed the song. George Bodenheimer, who is employed by

#### Rank 3 | activation = 465.0665893554688

- **row_id:** 1653
- **case_id:** 3294
- **fact_id:** cf_3294
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Holly Rowe
- **relation_id:** P108
- **correct_answer:** ESPN
- **target_true:** ESPN
- **target_new:** NBC
- **generated_answer:**  the University of Utah, is a sports reporter for ESPN. The 20
- **strict_answer_segment:** the University of Utah, is a sports reporter for ESPN. The 20
- **strict_matched_answer:** ESPN

**Prompt:**

> His real interests, however, already lay with ornithology. Holly Rowe, who works for

#### Rank 4 | activation = 463.9346923828125

- **row_id:** 3288
- **case_id:** 1282
- **fact_id:** cf_1282
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Huw Edwards
- **relation_id:** P108
- **correct_answer:** BBC
- **target_true:** BBC
- **target_new:** McLaren
- **generated_answer:**  the BBC. She is the first woman to hold the position. She is the
- **strict_answer_segment:** the BBC. She is the first woman to hold the position. She is the
- **strict_matched_answer:** BBC

**Prompt:**

> She took office in January, 2014. Huw Edwards works for

#### Rank 5 | activation = 457.0856323242188

- **row_id:** 2513
- **case_id:** 13379
- **fact_id:** cf_13379
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Honda Center
- **relation_id:** P127
- **correct_answer:** Anaheim
- **target_true:** Anaheim
- **target_new:** Yahoo
- **generated_answer:**  Henry Samueli said the team will be able to play in the arena for the
- **strict_answer_segment:** Henry Samueli said the team will be able to play in the arena for the

**Prompt:**

> He soon made his debut with the Rookie-level Martinsville Phillies. Honda Center owner

#### Rank 6 | activation = 456.6627197265625

- **row_id:** 3931
- **case_id:** 12680
- **fact_id:** cf_12680
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Michael Grade
- **relation_id:** P108
- **correct_answer:** BBC
- **target_true:** BBC
- **target_new:** Microsoft
- **generated_answer:**  the BBC to oversee the project.  The BBC has been criticised for its handling
- **strict_answer_segment:** the BBC to oversee the project.
- **strict_matched_answer:** BBC

**Prompt:**

> It is expected to cost £38.7 million. Michael Grade is employed by

#### Rank 7 | activation = 454.0357666015625

- **row_id:** 2822
- **case_id:** 4263
- **fact_id:** cf_4263
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Victoria Derbyshire
- **relation_id:** P108
- **correct_answer:** BBC
- **target_true:** BBC
- **target_new:** IBM
- **generated_answer:**  the BBC, is a British journalist and broadcaster. She is the host of the
- **strict_answer_segment:** the BBC, is a British journalist and broadcaster. She is the host of the
- **strict_matched_answer:** BBC

**Prompt:**

> She was named for Frank Bruce. Victoria Derbyshire, who works for

#### Rank 8 | activation = 449.7606201171875

- **row_id:** 2485
- **case_id:** 7661
- **fact_id:** cf_7661
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Google Web Toolkit
- **relation_id:** P178
- **correct_answer:** Google
- **target_true:** Google
- **target_new:** Intel
- **generated_answer:**  Google, is a framework for building web applications using Java.  The first is
- **strict_answer_segment:** Google, is a framework for building web applications using Java.
- **strict_matched_answer:** Google

**Prompt:**

> Shimmering effects create an airy environment". Google Web Toolkit, created by

#### Rank 9 | activation = 423.8946533203125

- **row_id:** 732
- **case_id:** 9810
- **fact_id:** cf_9810
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Windows Mobile 6.5
- **relation_id:** P178
- **correct_answer:** Microsoft
- **target_true:** Microsoft
- **target_new:** Apple
- **generated_answer:**  Microsoft, is the operating system used by the Nokia N95. The Nokia
- **strict_answer_segment:** Microsoft, is the operating system used by the Nokia N95. The Nokia
- **strict_matched_answer:** Microsoft

**Prompt:**

> The former fire station is a Grade II listed building. Windows Mobile 6.5, a product developed by

#### Rank 10 | activation = 422.8971862792969

- **row_id:** 2662
- **case_id:** 517
- **fact_id:** cf_517
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** iBooks Author
- **relation_id:** P178
- **correct_answer:** Apple
- **target_true:** Apple
- **target_new:** Adobe
- **generated_answer:**  Apple Inc. and is a free application for the Mac OS X operating system.
- **strict_answer_segment:** Apple Inc. and is a free application for the Mac OS X operating system.
- **strict_matched_answer:** Apple

**Prompt:**

> The street has since been renamed State Street. iBooks Author was developed by


## Layer 12, Feature 2121

- **fraction diff correct - wrong:** 0.126
- **active fraction correct:** 0.1556
- **active fraction wrong:** 0.0296
- **total active count:** 299
- **activations on correct prompts in dataset:** 209
- **activations on wrong prompts in dataset:** 90
- **top relations:** P176:149, P178:92, P108:41, P127:14, P264:2
- **top subjects:** Siri:2, Ferrari Berlinetta Boxer:2, Chevrolet Corvette C5-R:2, PGM-11 Redstone:2, Porsche Panamera:2

### Top activating prompts

#### Rank 1 | activation = 378.8403625488281

- **row_id:** 1834
- **case_id:** 13930
- **fact_id:** cf_13930
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Dynamic-link library
- **relation_id:** P178
- **correct_answer:** Microsoft
- **target_true:** Microsoft
- **target_new:** Google
- **generated_answer:**  Microsoft, is a file that contains a set of functions that can be used by
- **strict_answer_segment:** Microsoft, is a file that contains a set of functions that can be used by
- **strict_matched_answer:** Microsoft

**Prompt:**

> Tempo novo. Dynamic-link library, a product manufactured by

#### Rank 2 | activation = 370.8768005371094

- **row_id:** 2196
- **case_id:** 13024
- **fact_id:** cf_13024
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Microsoft SharePoint
- **relation_id:** P178
- **correct_answer:** Microsoft
- **target_true:** Microsoft
- **target_new:** Google
- **generated_answer:**  Microsoft and is a web-based application that allows users to create, manage and
- **strict_answer_segment:** Microsoft and is a web-based application that allows users to create, manage and
- **strict_matched_answer:** Microsoft

**Prompt:**

> This sector is one of the fastest growing in Europe. Microsoft SharePoint is developed by

#### Rank 3 | activation = 367.2064514160156

- **row_id:** 2197
- **case_id:** 13024
- **fact_id:** cf_13024
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Microsoft SharePoint
- **relation_id:** P178
- **correct_answer:** Microsoft
- **target_true:** Microsoft
- **target_new:** Google
- **generated_answer:**  Microsoft Corporation, is a web-based collaboration and document management platform that allows users
- **strict_answer_segment:** Microsoft Corporation, is a web-based collaboration and document management platform that allows users
- **strict_matched_answer:** Microsoft

**Prompt:**

> 83 - Philémon et Baucis, opéra de Ch. Microsoft SharePoint, a product manufactured by

#### Rank 4 | activation = 367.1526794433594

- **row_id:** 3001
- **case_id:** 17266
- **fact_id:** cf_17266
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Chromecast
- **relation_id:** P178
- **correct_answer:** Google
- **target_true:** Google
- **target_new:** Microsoft
- **generated_answer:**  Google, is a streaming device that allows users to stream content from their mobile devices
- **strict_answer_segment:** Google, is a streaming device that allows users to stream content from their mobile devices
- **strict_matched_answer:** Google

**Prompt:**

> The programme paved the way for free trade. Chromecast, a product manufactured by

#### Rank 5 | activation = 362.2207336425781

- **row_id:** 3746
- **case_id:** 1373
- **fact_id:** cf_1373
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Microsoft Plus!
- **relation_id:** P178
- **correct_answer:** Microsoft
- **target_true:** Microsoft
- **target_new:** IBM
- **generated_answer:**  Microsoft Corporation, is a software package that includes a word processor, a spreadsheet,
- **strict_answer_segment:** Microsoft Corporation, is a software package that includes a word processor, a spreadsheet,
- **strict_matched_answer:** Microsoft

**Prompt:**

> References Obituary, The New York Times February 5, 1989. Microsoft Plus!, a product manufactured by

#### Rank 6 | activation = 342.9115295410156

- **row_id:** 3362
- **case_id:** 4225
- **fact_id:** cf_4225
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** ColorSync
- **relation_id:** P178
- **correct_answer:** Apple
- **target_true:** Apple
- **target_new:** Microsoft
- **generated_answer:**  Apple, is a functor from the category of color spaces to the category of color
- **strict_answer_segment:** Apple, is a functor from the category of color spaces to the category of color
- **strict_matched_answer:** Apple

**Prompt:**

> Functors  Functors are structure-preserving maps between categories. ColorSync, a product manufactured by

#### Rank 7 | activation = 338.9359436035156

- **row_id:** 289
- **case_id:** 11146
- **fact_id:** cf_11146
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** iPod shuffle
- **relation_id:** P178
- **correct_answer:** Apple
- **target_true:** Apple
- **target_new:** Sega
- **generated_answer:**  Apple, is a portable music player that is used to play music. It is
- **strict_answer_segment:** Apple, is a portable music player that is used to play music. It is
- **strict_matched_answer:** Apple

**Prompt:**

> References   Category:Adware iPod shuffle, a product developed by

#### Rank 8 | activation = 337.6386413574219

- **row_id:** 621
- **case_id:** 2245
- **fact_id:** cf_2245
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** MiniDisc
- **relation_id:** P178
- **correct_answer:** Sony
- **target_true:** Sony
- **target_new:** Microsoft
- **generated_answer:**  Sony, is a digital audio recording and playback device. It is a digital audio
- **strict_answer_segment:** Sony, is a digital audio recording and playback device. It is a digital audio
- **strict_matched_answer:** Sony

**Prompt:**

> Kaisoluchukwu (Solu, Kaiso). MiniDisc, a product manufactured by

#### Rank 9 | activation = 331.9195861816406

- **row_id:** 3991
- **case_id:** 16670
- **fact_id:** cf_16670
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** QuickDraw
- **relation_id:** P178
- **correct_answer:** Apple
- **target_true:** Apple
- **target_new:** Sony
- **generated_answer:**  the company QuickDraw, are all examples of the same thing.  The correct
- **strict_answer_segment:** the company QuickDraw, are all examples of the same thing.

**Prompt:**

> Javon Leake, Jake Funk, Max Bortenschlager, and D.J. QuickDraw, a product manufactured by

#### Rank 10 | activation = 331.3751525878906

- **row_id:** 3982
- **case_id:** 5161
- **fact_id:** cf_5161
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Adobe AIR
- **relation_id:** P178
- **correct_answer:** Adobe
- **target_true:** Adobe
- **target_new:** Microsoft
- **generated_answer:**  Adobe Systems, is a cross-platform runtime environment that allows the creation of desktop
- **strict_answer_segment:** Adobe Systems, is a cross-platform runtime environment that allows the creation of desktop
- **strict_matched_answer:** Adobe

**Prompt:**

> The word Chuda turns into Sunda from local pronunciation. Adobe AIR, a product manufactured by


## Layer 12, Feature 11304

- **fraction diff correct - wrong:** 0.1194
- **active fraction correct:** 0.1981
- **active fraction wrong:** 0.0786
- **total active count:** 505
- **activations on correct prompts in dataset:** 266
- **activations on wrong prompts in dataset:** 239
- **top relations:** P37:135, P103:134, P27:97, P364:62, P1412:46
- **top subjects:** World Health Organization:3, Sola Aoi:2, Saskatchewan:2, Ronaldinho:2, Christophor Araratov:2

### Top activating prompts

#### Rank 1 | activation = 310.1900634765625

- **row_id:** 2008
- **case_id:** 17996
- **fact_id:** cf_17996
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Pedro Paterno
- **relation_id:** P1412
- **correct_answer:** Spanish
- **target_true:** Spanish
- **target_new:** English
- **generated_answer:**  of the people. He was a member of the Katipunan, a secret
- **strict_answer_segment:** of the people. He was a member of the Katipunan, a secret

**Prompt:**

> He also spent time at his estates outside of Brooklyn. Pedro Paterno speaks the language

#### Rank 2 | activation = 307.806884765625

- **row_id:** 836
- **case_id:** 21854
- **fact_id:** cf_21854
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Jean Lefebvre
- **relation_id:** P103
- **correct_answer:** French
- **target_true:** French
- **target_new:** English
- **generated_answer:**  of the people and was able to communicate with them. The team was led by
- **strict_answer_segment:** of the people and was able to communicate with them. The team was led by

**Prompt:**

> The team finished with an overall record of 8–9. Jean Lefebvre spoke the language

#### Rank 3 | activation = 301.59002685546875

- **row_id:** 773
- **case_id:** 3024
- **fact_id:** cf_3024
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Aleksandr Ptushko
- **relation_id:** P103
- **correct_answer:** Russian
- **target_true:** Russian
- **target_new:** French
- **generated_answer:**  Russian and Ukrainian. He is a graduate of the University of St. Tikh
- **strict_answer_segment:** Russian and Ukrainian. He is a graduate of the University of St. Tikh
- **strict_matched_answer:** Russian

**Prompt:**

> in Theology, Major in Missiology  M.A. Aleksandr Ptushko is a native speaker of

#### Rank 4 | activation = 299.8569030761719

- **row_id:** 2488
- **case_id:** 820
- **fact_id:** cf_820
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Robert Naunton
- **relation_id:** P1412
- **correct_answer:** English
- **target_true:** English
- **target_new:** Spanish
- **generated_answer:**  of the people. The Indonesian government has been trying to improve the situation in Aceh
- **strict_answer_segment:** of the people. The Indonesian government has been trying to improve the situation in Aceh

**Prompt:**

> Sudharmono was later appointed to the Ministry of Home Affairs. Robert Naunton speaks the language

#### Rank 5 | activation = 293.45367431640625

- **row_id:** 3952
- **case_id:** 4018
- **fact_id:** cf_4018
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Easter Island
- **relation_id:** P37
- **correct_answer:** Spanish
- **target_true:** Spanish
- **target_new:** Italian
- **generated_answer:**  Rapa Nui.The first inhabitants of the island were Polynesians
- **strict_answer_segment:** Rapa Nui.The first inhabitants of the island were Polynesians

**Prompt:**

> A two-story building was built in 1873. The official language of Easter Island is

#### Rank 6 | activation = 287.2313537597656

- **row_id:** 2742
- **case_id:** 9011
- **fact_id:** cf_9011
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Sergei Nilus
- **relation_id:** P1412
- **correct_answer:** Russian
- **target_true:** Russian
- **target_new:** French
- **generated_answer:**  of the people.  The police are investigating the case of a woman who was
- **strict_answer_segment:** of the people.

**Prompt:**

> Martha asked for police assistance to protect her home. Sergei Nilus speaks the language

#### Rank 7 | activation = 287.0728454589844

- **row_id:** 1485
- **case_id:** 5771
- **fact_id:** cf_5771
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Laurent Fabius
- **relation_id:** P103
- **correct_answer:** French
- **target_true:** French
- **target_new:** Russian
- **generated_answer:**  French. He is a member of the French Socialist Party. He was born on
- **strict_answer_segment:** French. He is a member of the French Socialist Party. He was born on
- **strict_matched_answer:** French

**Prompt:**

> xi + 382 pp. The mother tongue of Laurent Fabius is

#### Rank 8 | activation = 285.6831970214844

- **row_id:** 231
- **case_id:** 14038
- **fact_id:** cf_14038
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Juan Carlos Garrido
- **relation_id:** P1412
- **correct_answer:** Spanish
- **target_true:** Spanish
- **target_new:** French
- **generated_answer:**  of chess. He is a chess player, coach, and author. He is
- **strict_answer_segment:** of chess. He is a chess player, coach, and author. He is

**Prompt:**

> In 2006 he finished second in the Hungarian Chess Championship. Juan Carlos Garrido speaks the language

#### Rank 9 | activation = 282.2993469238281

- **row_id:** 1567
- **case_id:** 18192
- **fact_id:** cf_18192
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Gato Fedorento
- **relation_id:** P364
- **correct_answer:** Portuguese
- **target_true:** Portuguese
- **target_new:** English
- **generated_answer:**  Spanish.  25 May - Henri d'Albret (b
- **strict_answer_segment:** Spanish.

**Prompt:**

> 1478)  25 May - Henri d'Albret (b. The original language of Gato Fedorento is

#### Rank 10 | activation = 281.04034423828125

- **row_id:** 550
- **case_id:** 15773
- **fact_id:** cf_15773
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Kondura
- **relation_id:** P364
- **correct_answer:** Hindi
- **target_true:** Hindi
- **target_new:** Croatian
- **generated_answer:**  a language of the Kondura people, a small ethnic group in the state of
- **strict_answer_segment:** a language of the Kondura people, a small ethnic group in the state of

**Prompt:**

> It is scheduled to open in 2022. The language of Kondura is


## Layer 15, Feature 319

- **fraction diff correct - wrong:** 0.1051
- **active fraction correct:** 0.2308
- **active fraction wrong:** 0.1257
- **total active count:** 692
- **activations on correct prompts in dataset:** 310
- **activations on wrong prompts in dataset:** 382
- **top relations:** P176:75, P17:70, P159:65, P413:61, P276:45
- **top subjects:** Kew Gardens Hills:2, North Middlesex, Ontario:2, Merisant:2, Vicente Grau Juan:2, Constantijn Huygens:2

### Top activating prompts

#### Rank 1 | activation = 1838.599853515625

- **row_id:** 3411
- **case_id:** 2528
- **fact_id:** cf_2528
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** John Cuthbert Hedley
- **relation_id:** P39
- **correct_answer:** bishop
- **target_true:** bishop
- **target_new:** cardinal
- **generated_answer:**  Chairman of the Board at Hedley & Co. Ltd.  He is also
- **strict_answer_segment:** Chairman of the Board at Hedley & Co. Ltd.

**Prompt:**

> He is a recipient of several ASCAP awards. John Cuthbert Hedley holds the position of

#### Rank 2 | activation = 1733.865234375

- **row_id:** 4153
- **case_id:** 21034
- **fact_id:** cf_21034
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Christian Ude
- **relation_id:** P39
- **correct_answer:** mayor
- **target_true:** mayor
- **target_new:** pope
- **generated_answer:**  Chief Executive Officer & Director at Eko Electricity Distribution Company Ltd.  ---  
- **strict_answer_segment:** Chief Executive Officer & Director at Eko Electricity Distribution Company Ltd.

**Prompt:**

> For every 100 females, there were 90.7 males. Christian Ude holds the position of

#### Rank 3 | activation = 1709.6451416015625

- **row_id:** 3434
- **case_id:** 5316
- **fact_id:** cf_5316
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Samuel Ruiz
- **relation_id:** P39
- **correct_answer:** bishop
- **target_true:** bishop
- **target_new:** cardinal
- **generated_answer:**  Chairman at Grupo Financiero Banorte, S.A.B. de C
- **strict_answer_segment:** Chairman at Grupo Financiero Banorte, S.A.B. de C

**Prompt:**

> He lost the election by 643 votes to 296. Samuel Ruiz holds the position of

#### Rank 4 | activation = 1658.7835693359375

- **row_id:** 4198
- **case_id:** 4014
- **fact_id:** cf_4014
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Beykent University
- **relation_id:** P159
- **correct_answer:** Istanbul
- **target_true:** Istanbul
- **target_new:** Warsaw
- **generated_answer:**  Istanbul. The address of the Shine One [Original Edit] - feat. Bey
- **strict_answer_segment:** Istanbul. The address of the Shine One [Original Edit] - feat. Bey
- **strict_matched_answer:** Istanbul

**Prompt:**

> Lila Liu  Shine One [Original Edit] - feat. Beykent University is headquartered in

#### Rank 5 | activation = 1586.369140625

- **row_id:** 3144
- **case_id:** 11448
- **fact_id:** cf_11448
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Francesco Parravicini
- **relation_id:** P413
- **correct_answer:** midfielder
- **target_true:** midfielder
- **target_new:** linebacker
- **generated_answer:**  Goalkeeper. The average salary for a Goalkeeper is $14,1
- **strict_answer_segment:** Goalkeeper. The average salary for a Goalkeeper is $14,1

**Prompt:**

> The per capita income for the unorganized territory was $14,180. Francesco Parravicini plays in the position of

#### Rank 6 | activation = 1566.12744140625

- **row_id:** 3268
- **case_id:** 15585
- **fact_id:** cf_15585
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Marques Tuiasosopo
- **relation_id:** P413
- **correct_answer:** quarterback
- **target_true:** quarterback
- **target_new:** pitcher
- **generated_answer:**  Quarterback for the University of Washington Huskies. The bridge's WGCB
- **strict_answer_segment:** Quarterback for the University of Washington Huskies. The bridge's WGCB
- **strict_matched_answer:** quarterback

**Prompt:**

> The bridge's WGCB Number is 38-36-28. Marques Tuiasosopo plays in the position of

#### Rank 7 | activation = 1539.098876953125

- **row_id:** 2542
- **case_id:** 17701
- **fact_id:** cf_17701
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Ed Austin
- **relation_id:** P39
- **correct_answer:** mayor
- **target_true:** mayor
- **target_new:** bishop
- **generated_answer:**  President of the Board of Directors of the Austin Language Center.  The Austin Language
- **strict_answer_segment:** President of the Board of Directors of the Austin Language Center.

**Prompt:**

> Mayan Languages Collection of Larry Grimes. Ed Austin holds the position of

#### Rank 8 | activation = 1501.445068359375

- **row_id:** 1188
- **case_id:** 17081
- **fact_id:** cf_17081
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Frank Lampard
- **relation_id:** P413
- **correct_answer:** midfielder
- **target_true:** midfielder
- **target_new:** quarterback
- **generated_answer:**  Midfielder and his preferred foot is Right. Frank Lampard is 42 years
- **strict_answer_segment:** Midfielder and his preferred foot is Right. Frank Lampard is 42 years
- **strict_matched_answer:** midfielder

**Prompt:**

> His finding was soon confirmed algebraically by Tharmalingam and Lidiard. Frank Lampard plays in the position of

#### Rank 9 | activation = 1479.42919921875

- **row_id:** 2503
- **case_id:** 2071
- **fact_id:** cf_2071
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Marcus Marek
- **relation_id:** P413
- **correct_answer:** linebacker
- **target_true:** linebacker
- **target_new:** midfielder
- **generated_answer:**  Goalkeeper. Marcus Marek is 23 years old (20/
- **strict_answer_segment:** Goalkeeper.

**Prompt:**

> players Category:Guiseley A.F.C. Marcus Marek plays in the position of

#### Rank 10 | activation = 1430.11328125

- **row_id:** 452
- **case_id:** 17669
- **fact_id:** cf_17669
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Walter Johnson
- **relation_id:** P413
- **correct_answer:** pitcher
- **target_true:** pitcher
- **target_new:** midfielder
- **generated_answer:**  a Center. He was born on May 20, 199
- **strict_answer_segment:** a Center. He was born on May 20, 199

**Prompt:**

> محمدیان، کوخری، محمد ، “ (به یاد کوخرد) “، ج1. Walter Johnson plays in the position of


## Layer 15, Feature 1468

- **fraction diff correct - wrong:** 0.1016
- **active fraction correct:** 0.2264
- **active fraction wrong:** 0.1247
- **total active count:** 683
- **activations on correct prompts in dataset:** 304
- **activations on wrong prompts in dataset:** 379
- **top relations:** P37:110, P364:94, P101:77, P159:68, P103:62
- **top subjects:** World Health Organization:3, Jewel-Osco:2, Faceless Killers:2, Formentera:2, Porvoo:2

### Top activating prompts

#### Rank 1 | activation = 619.3872680664062

- **row_id:** 3394
- **case_id:** 5906
- **fact_id:** cf_5906
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** World Health Organization
- **relation_id:** P37
- **correct_answer:** French
- **target_true:** French
- **target_new:** Spanish
- **generated_answer:**  English. The World Health Organization (WHO) is a specialized agency of the United
- **strict_answer_segment:** English. The World Health Organization (WHO) is a specialized agency of the United

**Prompt:**

> In winter all of the trails are open for snowshoeing. The official language of World Health Organization is

#### Rank 2 | activation = 615.1956787109375

- **row_id:** 3154
- **case_id:** 4798
- **fact_id:** cf_4798
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Sovereign Military Order of Malta
- **relation_id:** P37
- **correct_answer:** Latin
- **target_true:** Latin
- **target_new:** Russian
- **generated_answer:**  Latin. The Order of Malta is a sovereign, independent, and international non-
- **strict_answer_segment:** Latin. The Order of Malta is a sovereign, independent, and international non-
- **strict_matched_answer:** Latin

**Prompt:**

> East Zorra Mennonite Cemetery - 677044 16th Line. The official language of Sovereign Military Order of Malta is

#### Rank 3 | activation = 611.1961669921875

- **row_id:** 2469
- **case_id:** 14902
- **fact_id:** cf_14902
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** World Health Organization
- **relation_id:** P37
- **correct_answer:** Russian
- **target_true:** Russian
- **target_new:** Finnish
- **generated_answer:**  English.  The World Health Organization (WHO) is a specialized agency of the
- **strict_answer_segment:** English.

**Prompt:**

> References  Category:Unincorporated communities in Manitoba The official language of World Health Organization is

#### Rank 4 | activation = 593.382568359375

- **row_id:** 2389
- **case_id:** 20586
- **fact_id:** cf_20586
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Balthasar Bekker
- **relation_id:** P103
- **correct_answer:** Dutch
- **target_true:** Dutch
- **target_new:** French
- **generated_answer:**  the language of the Dutch Reformed Church. The language of the Dutch Reformed Church is
- **strict_answer_segment:** the language of the Dutch Reformed Church. The language of the Dutch Reformed Church is
- **strict_matched_answer:** Dutch

**Prompt:**

> Troubleshooting the Troubleshooting Course, Or, Debug D'Bugs. The native language of Balthasar Bekker is

#### Rank 5 | activation = 589.8394775390625

- **row_id:** 1508
- **case_id:** 8044
- **fact_id:** cf_8044
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Pierre-Alexandre-Laurent Forfait
- **relation_id:** P103
- **correct_answer:** French
- **target_true:** French
- **target_new:** Hebrew
- **generated_answer:**  French. The first is the 1990s, when the first
- **strict_answer_segment:** French. The first is the 1990s, when the first
- **strict_matched_answer:** French

**Prompt:**

> Jones, The history of martian volatiles, Rev. The mother tongue of Pierre-Alexandre-Laurent Forfait is

#### Rank 6 | activation = 585.44921875

- **row_id:** 2204
- **case_id:** 17485
- **fact_id:** cf_17485
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Louis-Paul Aujoulat
- **relation_id:** P103
- **correct_answer:** French
- **target_true:** French
- **target_new:** Dutch
- **generated_answer:**  the Occitan language. He is a member of the Occitan Academy. He
- **strict_answer_segment:** the Occitan language. He is a member of the Occitan Academy. He

**Prompt:**

> By the blood. The native language of Louis-Paul Aujoulat is

#### Rank 7 | activation = 582.8197021484375

- **row_id:** 2490
- **case_id:** 20301
- **fact_id:** cf_20301
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Mad TV
- **relation_id:** P364
- **correct_answer:** English
- **target_true:** English
- **target_new:** Tamil
- **generated_answer:**  English, but the show is subtitled in many languages. The show is also
- **strict_answer_segment:** English, but the show is subtitled in many languages. The show is also
- **strict_matched_answer:** English

**Prompt:**

> References  Category:Nyssodrysternum Category:Beetles described in 2011 The original language of Mad TV is

#### Rank 8 | activation = 576.9053955078125

- **row_id:** 2449
- **case_id:** 7392
- **fact_id:** cf_7392
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Gil J Wolman
- **relation_id:** P103
- **correct_answer:** French
- **target_true:** French
- **target_new:** Russian
- **generated_answer:**  English. He is a writer, director, and producer. He is a graduate
- **strict_answer_segment:** English. He is a writer, director, and producer. He is a graduate

**Prompt:**

> T.M. The mother tongue of Gil J Wolman is

#### Rank 9 | activation = 572.7352294921875

- **row_id:** 3619
- **case_id:** 14978
- **fact_id:** cf_14978
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Les Bois
- **relation_id:** P37
- **correct_answer:** French
- **target_true:** French
- **target_new:** German
- **generated_answer:**  French. The Bois is a small town in the north of France, in the
- **strict_answer_segment:** French. The Bois is a small town in the north of France, in the
- **strict_matched_answer:** French

**Prompt:**

> Intersections in the Philosophy of Mathematics of A.N. The official language of Les Bois is

#### Rank 10 | activation = 565.475341796875

- **row_id:** 1227
- **case_id:** 7010
- **fact_id:** cf_7010
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Alberto Giacometti
- **relation_id:** P103
- **correct_answer:** Italian
- **target_true:** Italian
- **target_new:** French
- **generated_answer:**  French, but he was born in Switzerland. The first vineyards were planted in 
- **strict_answer_segment:** French, but he was born in Switzerland. The first vineyards were planted in

**Prompt:**

> All follow dry riverbeds, which provide appropriate soils for viticulture. The mother tongue of Alberto Giacometti is


## Layer 15, Feature 2034

- **fraction diff correct - wrong:** 0.1296
- **active fraction correct:** 0.1668
- **active fraction wrong:** 0.0372
- **total active count:** 337
- **activations on correct prompts in dataset:** 224
- **activations on wrong prompts in dataset:** 113
- **top relations:** P176:166, P178:109, P127:24, P138:16, P108:16
- **top subjects:** Google Patents:2, Siri:2, Ferrari Berlinetta Boxer:2, Chevrolet Corvette C5-R:2, Cyberdog:2

### Top activating prompts

#### Rank 1 | activation = 910.9169921875

- **row_id:** 3720
- **case_id:** 5737
- **fact_id:** cf_5737
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Ferrari 125 S
- **relation_id:** P176
- **correct_answer:** Ferrari
- **target_true:** Ferrari
- **target_new:** Toyota
- **generated_answer:**  the Ferrari 125 S, is a 125cc motorcycle
- **strict_answer_segment:** the Ferrari 125 S, is a 125cc motorcycle
- **strict_matched_answer:** Ferrari

**Prompt:**

> The brewery self-distributes in Cincinnati and Columbus, Ohio. Ferrari 125 S, created by

#### Rank 2 | activation = 907.4892578125

- **row_id:** 4007
- **case_id:** 18076
- **fact_id:** cf_18076
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Alfa Romeo 75
- **relation_id:** P176
- **correct_answer:** Fiat
- **target_true:** Fiat
- **target_new:** Ferrari
- **generated_answer:**  the designer Giorgetto Giugiaro. Stuttgart: Motorbuch Verlag. ISBN 
- **strict_answer_segment:** the designer Giorgetto Giugiaro. Stuttgart: Motorbuch Verlag. ISBN

**Prompt:**

> Further reading Hofmann, Annette R. (2004). Alfa Romeo 75, created by

#### Rank 3 | activation = 862.8446044921875

- **row_id:** 331
- **case_id:** 18
- **fact_id:** cf_18
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Porsche 911
- **relation_id:** P176
- **correct_answer:** Porsche
- **target_true:** Porsche
- **target_new:** Honda
- **generated_answer:**  the Porsche Design Studio.  Monte Sobretta in the Porsche 911
- **strict_answer_segment:** the Porsche Design Studio.
- **strict_matched_answer:** Porsche

**Prompt:**

> References  External links   Monte Sobretta in Mountains for Everybody. Porsche 911, developed by

#### Rank 4 | activation = 851.0103759765625

- **row_id:** 3117
- **case_id:** 2577
- **fact_id:** cf_2577
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Honda Civic Type R
- **relation_id:** P176
- **correct_answer:** Honda
- **target_true:** Honda
- **target_new:** Microsoft
- **generated_answer:**  Honda. Retrieved 2013-01-15. 
- **strict_answer_segment:** Honda. Retrieved 2013-01-15.
- **strict_matched_answer:** Honda

**Prompt:**

> See also  Gracie Barra  References  Gracie Barra Orlando. Honda Civic Type R, created by

#### Rank 5 | activation = 842.273681640625

- **row_id:** 2525
- **case_id:** 16142
- **fact_id:** cf_16142
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** McLaren MP4-20
- **relation_id:** P176
- **correct_answer:** McLaren
- **target_true:** McLaren
- **target_new:** Nissan
- **generated_answer:**  Adrian Newey, was the first car to use the new regulations. The McLaren
- **strict_answer_segment:** Adrian Newey, was the first car to use the new regulations. The McLaren

**Prompt:**

> Design and analysis of experiments, 3rd ed. McLaren MP4-20, created by

#### Rank 6 | activation = 839.68896484375

- **row_id:** 2018
- **case_id:** 3978
- **fact_id:** cf_3978
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Lancia Thema
- **relation_id:** P176
- **correct_answer:** Fiat
- **target_true:** Fiat
- **target_new:** Chevrolet
- **generated_answer:**  Pininfarina, is a car that has been designed to be a symbol of
- **strict_answer_segment:** Pininfarina, is a car that has been designed to be a symbol of

**Prompt:**

> The voice cries "O Lionel! Lancia Thema, created by

#### Rank 7 | activation = 827.8673095703125

- **row_id:** 9
- **case_id:** 8024
- **fact_id:** cf_8024
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Google Patents
- **relation_id:** P178
- **correct_answer:** Google
- **target_true:** Google
- **target_new:** Microsoft
- **generated_answer:**  Google as a free search engine for academic and patent literature. It is a great
- **strict_answer_segment:** Google as a free search engine for academic and patent literature. It is a great
- **strict_matched_answer:** Google

**Prompt:**

> D-5541. Google Patents is created by

#### Rank 8 | activation = 810.310791015625

- **row_id:** 1976
- **case_id:** 37
- **fact_id:** cf_37
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Triumph TR8
- **relation_id:** P176
- **correct_answer:** Triumph
- **target_true:** Triumph
- **target_new:** Boeing
- **generated_answer:**  R.E. Triumph TR8) – 3:10  "
- **strict_answer_segment:** R.E. Triumph TR8) – 3:10
- **strict_matched_answer:** Triumph

**Prompt:**

> Broughton) – 3:46  "Dawn Crept Away" (R.E. Triumph TR8, created by

#### Rank 9 | activation = 806.6956787109375

- **row_id:** 982
- **case_id:** 10819
- **fact_id:** cf_10819
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Lancia Ypsilon
- **relation_id:** P176
- **correct_answer:** Fiat
- **target_true:** Fiat
- **target_new:** Chrysler
- **generated_answer:**  the Italian company Fiat, is a compact car with a 1.4-
- **strict_answer_segment:** the Italian company Fiat, is a compact car with a 1.4-
- **strict_matched_answer:** Fiat

**Prompt:**

> Optimality  It is known that Grover's algorithm is optimal. Lancia Ypsilon, developed by

#### Rank 10 | activation = 788.5755615234375

- **row_id:** 719
- **case_id:** 9912
- **fact_id:** cf_9912
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Bentley Continental
- **relation_id:** P176
- **correct_answer:** Bentley
- **target_true:** Bentley
- **target_new:** Toyota
- **generated_answer:**  the designer of the car, the famous designer of the 1930
- **strict_answer_segment:** the designer of the car, the famous designer of the 1930

**Prompt:**

> Hümaşah leaves the capital forever. Bentley Continental is created by


## Layer 15, Feature 5485

- **fraction diff correct - wrong:** 0.1213
- **active fraction correct:** 0.1549
- **active fraction wrong:** 0.0336
- **total active count:** 310
- **activations on correct prompts in dataset:** 208
- **activations on wrong prompts in dataset:** 102
- **top relations:** P176:155, P178:96, P108:28, P127:25, P264:5
- **top subjects:** Siri:2, Ferrari Berlinetta Boxer:2, Chevrolet Corvette C5-R:2, PGM-11 Redstone:2, Cyberdog:2

### Top activating prompts

#### Rank 1 | activation = 729.821533203125

- **row_id:** 4104
- **case_id:** 19392
- **fact_id:** cf_19392
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** HBO Now
- **relation_id:** P127
- **correct_answer:** HBO
- **target_true:** HBO
- **target_new:** CBS
- **generated_answer:**  the way, is a great service.  I'm not sure if you
- **strict_answer_segment:** the way, is a great service.

**Prompt:**

> Man, do not worry, no, laughing is good! HBO Now, by

#### Rank 2 | activation = 700.58349609375

- **row_id:** 3466
- **case_id:** 10140
- **fact_id:** cf_10140
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Simca
- **relation_id:** P127
- **correct_answer:** Fiat
- **target_true:** Fiat
- **target_new:** Toronto
- **generated_answer:**  the way, is a French car manufacturer.  The name is a combination of
- **strict_answer_segment:** the way, is a French car manufacturer.

**Prompt:**

> Its meaning is "person who brings kind news". Simca, by

#### Rank 3 | activation = 688.599609375

- **row_id:** 272
- **case_id:** 17338
- **fact_id:** cf_17338
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Aloha Stadium
- **relation_id:** P127
- **correct_answer:** Hawaii
- **target_true:** Hawaii
- **target_new:** BBC
- **generated_answer:**  the way, is the largest stadium in Hawaii.  The 199
- **strict_answer_segment:** the way, is the largest stadium in Hawaii.
- **strict_matched_answer:** Hawaii

**Prompt:**

> The large version was more popular than the smaller one. Aloha Stadium, by

#### Rank 4 | activation = 686.8387451171875

- **row_id:** 2079
- **case_id:** 19640
- **fact_id:** cf_19640
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Google Trends
- **relation_id:** P127
- **correct_answer:** Google
- **target_true:** Google
- **target_new:** Seoul
- **generated_answer:**  contrast, is a tool that allows you to see how often a particular search term
- **strict_answer_segment:** contrast, is a tool that allows you to see how often a particular search term

**Prompt:**

> He was assassinated at the end of 192. Google Trends, by

#### Rank 5 | activation = 686.03369140625

- **row_id:** 2089
- **case_id:** 11137
- **fact_id:** cf_11137
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** BBC Persian Television
- **relation_id:** P127
- **correct_answer:** BBC
- **target_true:** BBC
- **target_new:** Vancouver
- **generated_answer:**  contrast, has been broadcasting in Farsi since 1997. The
- **strict_answer_segment:** contrast, has been broadcasting in Farsi since 1997. The

**Prompt:**

> Doctors thought that his condition could lead to his death. BBC Persian Television, by

#### Rank 6 | activation = 679.69384765625

- **row_id:** 2005
- **case_id:** 6670
- **fact_id:** cf_6670
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Gordini
- **relation_id:** P127
- **correct_answer:** Renault
- **target_true:** Renault
- **target_new:** Vancouver
- **generated_answer:**  the way, was a French racing driver who won the 1950
- **strict_answer_segment:** the way, was a French racing driver who won the 1950

**Prompt:**

> Its taste did not recommend it. Gordini, by

#### Rank 7 | activation = 644.3126220703125

- **row_id:** 3752
- **case_id:** 16888
- **fact_id:** cf_16888
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Yahoo! Tech
- **relation_id:** P127
- **correct_answer:** Yahoo
- **target_true:** Yahoo
- **target_new:** Pennsylvania
- **generated_answer:**  Piet Desmet. Desmet, Piet (2000). Yahoo
- **strict_answer_segment:** Piet Desmet.

**Prompt:**

> Walter de Gruyter. . Desmet, Piet (2000). Yahoo! Tech, by

#### Rank 8 | activation = 640.6326904296875

- **row_id:** 1787
- **case_id:** 2660
- **fact_id:** cf_2660
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Google Person Finder
- **relation_id:** P127
- **correct_answer:** Google
- **target_true:** Google
- **target_new:** Finland
- **generated_answer:**  the International Federation of Red Cross and Red Crescent Societies, is a tool to help
- **strict_answer_segment:** the International Federation of Red Cross and Red Crescent Societies, is a tool to help

**Prompt:**

> It is the northern extremity of Grand-Îlet Passage. Google Person Finder, by

#### Rank 9 | activation = 640.3645629882812

- **row_id:** 1211
- **case_id:** 10476
- **fact_id:** cf_10476
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Liberty Bowl Memorial Stadium
- **relation_id:** P127
- **correct_answer:** Memphis
- **target_true:** Memphis
- **target_new:** BBC
- **generated_answer:**  the University of Memphis, is the home of the Tigers. The Memphis Tigers are
- **strict_answer_segment:** the University of Memphis, is the home of the Tigers. The Memphis Tigers are
- **strict_matched_answer:** Memphis

**Prompt:**

> Thubana seimaensis is a moth in the family Lecithoceridae. Liberty Bowl Memorial Stadium, by

#### Rank 10 | activation = 633.2533569335938

- **row_id:** 1631
- **case_id:** 3917
- **fact_id:** cf_3917
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Sky Cinema
- **relation_id:** P127
- **correct_answer:** Sky
- **target_true:** Sky
- **target_new:** Google
- **generated_answer:**  contrast, is a subscription service that costs £10.99 a month
- **strict_answer_segment:** contrast, is a subscription service that costs £10.99 a month

**Prompt:**

> Slifkin noted, however, that nothing was resolved. Sky Cinema, by


## Layer 15, Feature 7143

- **fraction diff correct - wrong:** 0.1085
- **active fraction correct:** 0.1951
- **active fraction wrong:** 0.0865
- **total active count:** 525
- **activations on correct prompts in dataset:** 262
- **activations on wrong prompts in dataset:** 263
- **top relations:** P37:145, P103:135, P364:125, P1412:62, P407:33
- **top subjects:** World Health Organization:3, Allegro Non Troppo:2, North Dakota:2, The Possible:2, Mandailing language:2

### Top activating prompts

#### Rank 1 | activation = 602.3478393554688

- **row_id:** 338
- **case_id:** 638
- **fact_id:** cf_638
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** La Gomera
- **relation_id:** P37
- **correct_answer:** Spanish
- **target_true:** Spanish
- **target_new:** French
- **generated_answer:**  Spanish, but the local language is a variant of the Canary Islands Spanish. The
- **strict_answer_segment:** Spanish, but the local language is a variant of the Canary Islands Spanish. The
- **strict_matched_answer:** Spanish

**Prompt:**

> Gallery  References  Category:Cities and towns in Warmian-Masurian Voivodeship Category:Pisz County The official language of La Gomera is

#### Rank 2 | activation = 599.9851684570312

- **row_id:** 691
- **case_id:** 3276
- **fact_id:** cf_3276
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Collonge-Bellerive
- **relation_id:** P37
- **correct_answer:** French
- **target_true:** French
- **target_new:** English
- **generated_answer:**  French. The official language of Collonge-Bellerive is French. The
- **strict_answer_segment:** French. The official language of Collonge-Bellerive is French. The
- **strict_matched_answer:** French

**Prompt:**

> In 1987, when President Corazon Aquino issued Executive Order No. The official language of Collonge-Bellerive is

#### Rank 3 | activation = 569.99072265625

- **row_id:** 1566
- **case_id:** 18192
- **fact_id:** cf_18192
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Gato Fedorento
- **relation_id:** P364
- **correct_answer:** Portuguese
- **target_true:** Portuguese
- **target_new:** English
- **generated_answer:**  a dialect of Spanish.  The area is known for its production of milk and
- **strict_answer_segment:** a dialect of Spanish.

**Prompt:**

> The area leads the country in production of milk . The language of Gato Fedorento is

#### Rank 4 | activation = 562.3049926757812

- **row_id:** 2704
- **case_id:** 17086
- **fact_id:** cf_17086
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Formentera
- **relation_id:** P37
- **correct_answer:** Catalan
- **target_true:** Catalan
- **target_new:** Finnish
- **generated_answer:**  Catalan. The TCP Westwood+ version is implemented in the Linux kernel. The official
- **strict_answer_segment:** Catalan. The TCP Westwood+ version is implemented in the Linux kernel. The official
- **strict_matched_answer:** Catalan

**Prompt:**

> The TCP Westwood+ version is implemented in the Linux kernel. The official language of Formentera is

#### Rank 5 | activation = 560.9678344726562

- **row_id:** 512
- **case_id:** 4593
- **fact_id:** cf_4593
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Kalajoki
- **relation_id:** P37
- **correct_answer:** Finnish
- **target_true:** Finnish
- **target_new:** Chinese
- **generated_answer:**  Finnish. The Finnish language is a Finno-Ugric language, which is
- **strict_answer_segment:** Finnish. The Finnish language is a Finno-Ugric language, which is
- **strict_matched_answer:** Finnish

**Prompt:**

> & Allen, D., "Heintz, Fred", pp.262-263 in Main, J. In Kalajoki, the language spoken is

#### Rank 6 | activation = 559.5989990234375

- **row_id:** 1754
- **case_id:** 14762
- **fact_id:** cf_14762
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Tonga
- **relation_id:** P37
- **correct_answer:** English
- **target_true:** English
- **target_new:** French
- **generated_answer:**  Tongan, a Polynesian language. The Tongan language is a member of the
- **strict_answer_segment:** Tongan, a Polynesian language. The Tongan language is a member of the

**Prompt:**

> Sharpe, 1998. The official language of Tonga is

#### Rank 7 | activation = 555.509521484375

- **row_id:** 195
- **case_id:** 2168
- **fact_id:** cf_2168
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** American Samoa
- **relation_id:** P37
- **correct_answer:** English
- **target_true:** English
- **target_new:** Swedish
- **generated_answer:**  English. The official language of American Samoa is English. The official language of American
- **strict_answer_segment:** English. The official language of American Samoa is English. The official language of American
- **strict_matched_answer:** English

**Prompt:**

> Dellacqua fought hard but went down in two sets. The official language of American Samoa is

#### Rank 8 | activation = 555.1361694335938

- **row_id:** 716
- **case_id:** 17800
- **fact_id:** cf_17800
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Porvoo
- **relation_id:** P37
- **correct_answer:** Swedish
- **target_true:** Swedish
- **target_new:** Russian
- **generated_answer:**  Finnish. The city is located in the southern part of Finland, in the region
- **strict_answer_segment:** Finnish. The city is located in the southern part of Finland, in the region

**Prompt:**

> He sent Fronto a letter apologizing for his silence. The official language of Porvoo is

#### Rank 9 | activation = 554.6851806640625

- **row_id:** 2075
- **case_id:** 12569
- **fact_id:** cf_12569
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Newfoundland and Labrador
- **relation_id:** P37
- **correct_answer:** English
- **target_true:** English
- **target_new:** French
- **generated_answer:**  English. The official language of the province is English. The official language of the
- **strict_answer_segment:** English. The official language of the province is English. The official language of the
- **strict_matched_answer:** English

**Prompt:**

> Mixed Martial Arts    Mixed martial arts is legalised in Bahrain. The official language of Newfoundland and Labrador is

#### Rank 10 | activation = 553.8429565429688

- **row_id:** 3513
- **case_id:** 9340
- **fact_id:** cf_9340
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Maaninka
- **relation_id:** P37
- **correct_answer:** Finnish
- **target_true:** Finnish
- **target_new:** English
- **generated_answer:**  Maaninka. The Maaninka language is spoken by the Maaninka
- **strict_answer_segment:** Maaninka. The Maaninka language is spoken by the Maaninka

**Prompt:**

> It has a large head and bill. The official language of Maaninka is


## Layer 18, Feature 456

- **fraction diff correct - wrong:** 0.2869
- **active fraction correct:** 0.5607
- **active fraction wrong:** 0.2738
- **total active count:** 1585
- **activations on correct prompts in dataset:** 753
- **activations on wrong prompts in dataset:** 832
- **top relations:** P176:172, P27:134, P159:132, P449:118, P178:114
- **top subjects:** Afghanistan:3, Jakarta:3, Manila:3, Mexico City:3, Tirana:3

### Top activating prompts

#### Rank 1 | activation = 3289.89892578125

- **row_id:** 2122
- **case_id:** 17807
- **fact_id:** cf_17807
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Front Mission 3
- **relation_id:** P178
- **correct_answer:** Square
- **target_true:** Square
- **target_new:** Google
- **generated_answer:**  Square Enix and is a sequel to Front Mission 2. The game is set
- **strict_answer_segment:** Square Enix and is a sequel to Front Mission 2. The game is set
- **strict_matched_answer:** Square

**Prompt:**

> Marcus Carl Franklin as Woody. Front Mission 3 is created by

#### Rank 2 | activation = 3169.58642578125

- **row_id:** 2028
- **case_id:** 5189
- **fact_id:** cf_5189
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Adobe Premiere Elements
- **relation_id:** P178
- **correct_answer:** Adobe
- **target_true:** Adobe
- **target_new:** Google
- **generated_answer:**  Adobe Systems and is a video editing software.  The Ravens waived Bilukidi
- **strict_answer_segment:** Adobe Systems and is a video editing software.
- **strict_matched_answer:** Adobe

**Prompt:**

> Bilukidi was waived by the Ravens on October 10, 2015. Adobe Premiere Elements was developed by

#### Rank 3 | activation = 3025.3701171875

- **row_id:** 1698
- **case_id:** 14433
- **fact_id:** cf_14433
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** HDCAM
- **relation_id:** P127
- **correct_answer:** Sony
- **target_true:** Sony
- **target_new:** Germany
- **generated_answer:**  Sony and is the successor to the Betacam format. The player is a 
- **strict_answer_segment:** Sony and is the successor to the Betacam format. The player is a
- **strict_matched_answer:** Sony

**Prompt:**

> Should a player fail the song, the other player wins. HDCAM is owned by

#### Rank 4 | activation = 2986.630126953125

- **row_id:** 2029
- **case_id:** 5189
- **fact_id:** cf_5189
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Adobe Premiere Elements
- **relation_id:** P178
- **correct_answer:** Adobe
- **target_true:** Adobe
- **target_new:** Google
- **generated_answer:**  Adobe Systems Incorporated. The tsunami swept away most structures on the island. Adobe Premiere
- **strict_answer_segment:** Adobe Systems Incorporated. The tsunami swept away most structures on the island. Adobe Premiere
- **strict_matched_answer:** Adobe

**Prompt:**

> The tsunami swept away most structures on the island. Adobe Premiere Elements is developed by

#### Rank 5 | activation = 2978.550048828125

- **row_id:** 3991
- **case_id:** 16670
- **fact_id:** cf_16670
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** QuickDraw
- **relation_id:** P178
- **correct_answer:** Apple
- **target_true:** Apple
- **target_new:** Sony
- **generated_answer:**  the company QuickDraw, are all examples of the same thing.  The correct
- **strict_answer_segment:** the company QuickDraw, are all examples of the same thing.

**Prompt:**

> Javon Leake, Jake Funk, Max Bortenschlager, and D.J. QuickDraw, a product manufactured by

#### Rank 6 | activation = 2969.42626953125

- **row_id:** 1448
- **case_id:** 17456
- **fact_id:** cf_17456
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** BMW Z4 E85
- **relation_id:** P176
- **correct_answer:** BMW
- **target_true:** BMW
- **target_new:** Ferrari
- **generated_answer:**  the German company BMW. The game was released in 2005 for
- **strict_answer_segment:** the German company BMW. The game was released in 2005 for
- **strict_matched_answer:** BMW

**Prompt:**

> It was ported to the PlayStation Portable in 2006. BMW Z4 E85 is developed by

#### Rank 7 | activation = 2943.42919921875

- **row_id:** 983
- **case_id:** 10819
- **fact_id:** cf_10819
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Lancia Ypsilon
- **relation_id:** P176
- **correct_answer:** Fiat
- **target_true:** Fiat
- **target_new:** Chrysler
- **generated_answer:**  the Italian car manufacturer Lancia, is a small car that was first introduced in
- **strict_answer_segment:** the Italian car manufacturer Lancia, is a small car that was first introduced in

**Prompt:**

> She develops a liking towards him. Lancia Ypsilon, produced by

#### Rank 8 | activation = 2935.23193359375

- **row_id:** 520
- **case_id:** 15159
- **fact_id:** cf_15159
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Game & Watch
- **relation_id:** P176
- **correct_answer:** Nintendo
- **target_true:** Nintendo
- **target_new:** Toyota
- **generated_answer:**  Nintendo, is a handheld game console that was released in 1980
- **strict_answer_segment:** Nintendo, is a handheld game console that was released in 1980
- **strict_matched_answer:** Nintendo

**Prompt:**

> Not in elimination, not allowed to vote. Game & Watch, produced by

#### Rank 9 | activation = 2922.9296875

- **row_id:** 2287
- **case_id:** 4689
- **fact_id:** cf_4689
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** IBM 704
- **relation_id:** P176
- **correct_answer:** IBM
- **target_true:** IBM
- **target_new:** Honda
- **generated_answer:**  IBM in 1960, was the first IBM computer to use transistors
- **strict_answer_segment:** IBM in 1960, was the first IBM computer to use transistors
- **strict_matched_answer:** IBM

**Prompt:**

> Category:Bays of Graham Land Category:Graham Coast IBM 704, produced by

#### Rank 10 | activation = 2914.314453125

- **row_id:** 3661
- **case_id:** 21770
- **fact_id:** cf_21770
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Infiniti Q45
- **relation_id:** P176
- **correct_answer:** Nissan
- **target_true:** Nissan
- **target_new:** Toyota
- **generated_answer:**  Nissan, is a luxury crossover SUV. Infiniti Q45 is a luxury crossover
- **strict_answer_segment:** Nissan, is a luxury crossover SUV. Infiniti Q45 is a luxury crossover
- **strict_matched_answer:** Nissan

**Prompt:**

> Voiculeț is a Romanian surname. Infiniti Q45, developed by


## Layer 18, Feature 1399

- **fraction diff correct - wrong:** 0.1599
- **active fraction correct:** 0.2234
- **active fraction wrong:** 0.0635
- **total active count:** 493
- **activations on correct prompts in dataset:** 300
- **activations on wrong prompts in dataset:** 193
- **top relations:** P176:168, P178:114, P27:99, P108:28, P127:27
- **top subjects:** Malta:2, Google Patents:2, Shigeru Miyamoto:2, omphacite:2, Kazi Nazrul Islam:2

### Top activating prompts

#### Rank 1 | activation = 2182.0888671875

- **row_id:** 1332
- **case_id:** 12422
- **fact_id:** cf_12422
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Renault 4P
- **relation_id:** P176
- **correct_answer:** Renault
- **target_true:** Renault
- **target_new:** BMW
- **generated_answer:**  the French car manufacturer Renault. The Renault 4P is a 4-
- **strict_answer_segment:** the French car manufacturer Renault. The Renault 4P is a 4-
- **strict_matched_answer:** Renault

**Prompt:**

> That year Munster faced arch rivals Leinster in the decider. Renault 4P is created by

#### Rank 2 | activation = 2167.6708984375

- **row_id:** 2085
- **case_id:** 2287
- **fact_id:** cf_2287
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** BMW 5 Series Gran Turismo
- **relation_id:** P176
- **correct_answer:** BMW
- **target_true:** BMW
- **target_new:** Ferrari
- **generated_answer:**  the BMW Group DesignworksUSA in California. The BMW 5 Series Gran Turismo
- **strict_answer_segment:** the BMW Group DesignworksUSA in California. The BMW 5 Series Gran Turismo
- **strict_matched_answer:** BMW

**Prompt:**

> In 1935, she married Tibor Vilt, a sculptor. BMW 5 Series Gran Turismo is developed by

#### Rank 3 | activation = 2149.820068359375

- **row_id:** 288
- **case_id:** 11146
- **fact_id:** cf_11146
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** iPod shuffle
- **relation_id:** P178
- **correct_answer:** Apple
- **target_true:** Apple
- **target_new:** Sega
- **generated_answer:**  Apple, is a small, portable music player that can be used to listen to
- **strict_answer_segment:** Apple, is a small, portable music player that can be used to listen to
- **strict_matched_answer:** Apple

**Prompt:**

> 0 !! iPod shuffle, a product created by

#### Rank 4 | activation = 2148.220703125

- **row_id:** 1657
- **case_id:** 9707
- **fact_id:** cf_9707
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Infiniti Q50
- **relation_id:** P176
- **correct_answer:** Nissan
- **target_true:** Nissan
- **target_new:** Fiat
- **generated_answer:**  the Nissan Motor Company. The Infiniti Q50 is a mid-size luxury
- **strict_answer_segment:** the Nissan Motor Company. The Infiniti Q50 is a mid-size luxury
- **strict_matched_answer:** Nissan

**Prompt:**

> The black community numbered about 20,000. Infiniti Q50 is created by

#### Rank 5 | activation = 2113.50927734375

- **row_id:** 594
- **case_id:** 1997
- **fact_id:** cf_1997
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Suzuki GSX-R750
- **relation_id:** P176
- **correct_answer:** Suzuki
- **target_true:** Suzuki
- **target_new:** Nissan
- **generated_answer:**  Suzuki Motor Corporation. The Suzuki GSX-R750 is a 
- **strict_answer_segment:** Suzuki Motor Corporation. The Suzuki GSX-R750 is a
- **strict_matched_answer:** Suzuki

**Prompt:**

> (It was historically used as civil ensign as well.) Suzuki GSX-R750 is created by

#### Rank 6 | activation = 2110.60205078125

- **row_id:** 753
- **case_id:** 19819
- **fact_id:** cf_19819
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Dodge Avenger
- **relation_id:** P176
- **correct_answer:** Dodge
- **target_true:** Dodge
- **target_new:** Honda
- **generated_answer:**  the Chrysler Group, a subsidiary of the American automaker Chrysler. Dodge Avenger is a
- **strict_answer_segment:** the Chrysler Group, a subsidiary of the American automaker Chrysler. Dodge Avenger is a
- **strict_matched_answer:** Dodge

**Prompt:**

> But people on drugs don't behave normally.' Dodge Avenger is created by

#### Rank 7 | activation = 2110.407958984375

- **row_id:** 175
- **case_id:** 20971
- **fact_id:** cf_20971
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Chevrolet Corvette C5-R
- **relation_id:** P176
- **correct_answer:** Chevrolet
- **target_true:** Chevrolet
- **target_new:** Atari
- **generated_answer:**  the American company Chevrolet, is a sports car, which is a development of the
- **strict_answer_segment:** the American company Chevrolet, is a sports car, which is a development of the
- **strict_matched_answer:** Chevrolet

**Prompt:**

> Uncut called Pornography "a masterpiece of claustrophobic self-loathing". Chevrolet Corvette C5-R, created by

#### Rank 8 | activation = 2102.477783203125

- **row_id:** 779
- **case_id:** 1444
- **fact_id:** cf_1444
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Dodge Dynasty
- **relation_id:** P176
- **correct_answer:** Dodge
- **target_true:** Dodge
- **target_new:** Triumph
- **generated_answer:**  the Corona program. The Corona program was a secret project of the United States.
- **strict_answer_segment:** the Corona program. The Corona program was a secret project of the United States.

**Prompt:**

> The first successful Corona mission began on August 10, 1963. Dodge Dynasty is created by

#### Rank 9 | activation = 2086.814208984375

- **row_id:** 3771
- **case_id:** 11697
- **fact_id:** cf_11697
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** BMW 4 Series
- **relation_id:** P176
- **correct_answer:** BMW
- **target_true:** BMW
- **target_new:** Dodge
- **generated_answer:**  the BMW Group. The BMW 4 Series is a 2-door coupe
- **strict_answer_segment:** the BMW Group. The BMW 4 Series is a 2-door coupe
- **strict_matched_answer:** BMW

**Prompt:**

> He told the President of the Keely Motor Company, A.R. BMW 4 Series is created by

#### Rank 10 | activation = 2084.75927734375

- **row_id:** 2255
- **case_id:** 11746
- **fact_id:** cf_11746
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Chevrolet Caprice
- **relation_id:** P176
- **correct_answer:** Chevrolet
- **target_true:** Chevrolet
- **target_new:** IBM
- **generated_answer:**  the American company General Motors, is a full-size car. The Chevrolet Cap
- **strict_answer_segment:** the American company General Motors, is a full-size car. The Chevrolet Cap
- **strict_matched_answer:** Chevrolet

**Prompt:**

> This led to nature photography and, subsequently, to filmmaking. Chevrolet Caprice, created by


## Layer 18, Feature 1652

- **fraction diff correct - wrong:** 0.0939
- **active fraction correct:** 0.2025
- **active fraction wrong:** 0.1086
- **total active count:** 602
- **activations on correct prompts in dataset:** 272
- **activations on wrong prompts in dataset:** 330
- **top relations:** P103:154, P37:152, P364:136, P1412:115, P407:37
- **top subjects:** World Health Organization:3, Three Men of the River:2, North Dakota:2, Byzantine Empire:2, The Possible:2

### Top activating prompts

#### Rank 1 | activation = 1394.8919677734375

- **row_id:** 3806
- **case_id:** 2707
- **fact_id:** cf_2707
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Ingrian Finns
- **relation_id:** P103
- **correct_answer:** Finnish
- **target_true:** Finnish
- **target_new:** Dutch
- **generated_answer:**  of the Finno-Ugric language family, which is related to the Hungarian
- **strict_answer_segment:** of the Finno-Ugric language family, which is related to the Hungarian

**Prompt:**

> Bocchi's classmate who loves sweets. Ingrian Finns spoke the language

#### Rank 2 | activation = 1373.28857421875

- **row_id:** 2488
- **case_id:** 820
- **fact_id:** cf_820
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Robert Naunton
- **relation_id:** P1412
- **correct_answer:** English
- **target_true:** English
- **target_new:** Spanish
- **generated_answer:**  of the people. The Indonesian government has been trying to improve the situation in Aceh
- **strict_answer_segment:** of the people. The Indonesian government has been trying to improve the situation in Aceh

**Prompt:**

> Sudharmono was later appointed to the Ministry of Home Affairs. Robert Naunton speaks the language

#### Rank 3 | activation = 1355.43994140625

- **row_id:** 836
- **case_id:** 21854
- **fact_id:** cf_21854
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Jean Lefebvre
- **relation_id:** P103
- **correct_answer:** French
- **target_true:** French
- **target_new:** English
- **generated_answer:**  of the people and was able to communicate with them. The team was led by
- **strict_answer_segment:** of the people and was able to communicate with them. The team was led by

**Prompt:**

> The team finished with an overall record of 8–9. Jean Lefebvre spoke the language

#### Rank 4 | activation = 1338.20458984375

- **row_id:** 806
- **case_id:** 17877
- **fact_id:** cf_17877
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Muonio
- **relation_id:** P37
- **correct_answer:** Finnish
- **target_true:** Finnish
- **target_new:** English
- **generated_answer:**  of the Sámi people to be the official language of the municipality. The Sá
- **strict_answer_segment:** of the Sámi people to be the official language of the municipality. The Sá

**Prompt:**

> For her part, Pasabán remarked, "I am confused. The law in Muonio declares the language

#### Rank 5 | activation = 1306.954833984375

- **row_id:** 513
- **case_id:** 4593
- **fact_id:** cf_4593
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Kalajoki
- **relation_id:** P37
- **correct_answer:** Finnish
- **target_true:** Finnish
- **target_new:** Chinese
- **generated_answer:**  of the elderly to be Finnish.  The Kalajoki City Council has decided
- **strict_answer_segment:** of the elderly to be Finnish.
- **strict_matched_answer:** Finnish

**Prompt:**

> An important step for the growing older population. The law in Kalajoki declares the language

#### Rank 6 | activation = 1302.592041015625

- **row_id:** 1721
- **case_id:** 18907
- **fact_id:** cf_18907
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Boris Vian
- **relation_id:** P103
- **correct_answer:** French
- **target_true:** French
- **target_new:** Dutch
- **generated_answer:**  of the street, and his work was a reflection of the world he lived in
- **strict_answer_segment:** of the street, and his work was a reflection of the world he lived in

**Prompt:**

> It was later re-designated "Company M", and later, "Company B". Boris Vian spoke the language

#### Rank 7 | activation = 1288.504638671875

- **row_id:** 1099
- **case_id:** 20030
- **fact_id:** cf_20030
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Mimie Mathy
- **relation_id:** P103
- **correct_answer:** French
- **target_true:** French
- **target_new:** English
- **generated_answer:**  of the people of the region, and was a member of the Polish Academy of
- **strict_answer_segment:** of the people of the region, and was a member of the Polish Academy of

**Prompt:**

> The later being proposed for Zakłodzie and NWA 4301. Mimie Mathy spoke the language

#### Rank 8 | activation = 1285.1126708984375

- **row_id:** 1280
- **case_id:** 7190
- **fact_id:** cf_7190
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Nazi Boni
- **relation_id:** P103
- **correct_answer:** French
- **target_true:** French
- **target_new:** Dutch
- **generated_answer:**  of the people, and he was a man of the people. He was a
- **strict_answer_segment:** of the people, and he was a man of the people. He was a

**Prompt:**

> (June 1992) Türkiye Futbol Federasyonu Yayınları. Nazi Boni spoke the language

#### Rank 9 | activation = 1280.1309814453125

- **row_id:** 332
- **case_id:** 19626
- **fact_id:** cf_19626
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Juan de Espinosa Medrano
- **relation_id:** P103
- **correct_answer:** Spanish
- **target_true:** Spanish
- **target_new:** French
- **generated_answer:**  of the people of the area, and was able to communicate with them. The
- **strict_answer_segment:** of the people of the area, and was able to communicate with them. The

**Prompt:**

> Tweedie died on 22 March 1934 in Edinburgh. Juan de Espinosa Medrano spoke the language

#### Rank 10 | activation = 1279.71826171875

- **row_id:** 1685
- **case_id:** 16085
- **fact_id:** cf_16085
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Nyusha
- **relation_id:** P103
- **correct_answer:** Russian
- **target_true:** Russian
- **target_new:** French
- **generated_answer:**  of the elves, and the elves were the first to speak the language of the
- **strict_answer_segment:** of the elves, and the elves were the first to speak the language of the

**Prompt:**

> Accordingly, the German word Alpdruck (literally "elf-oppression") means "nightmare". Nyusha spoke the language


## Layer 18, Feature 1664

- **fraction diff correct - wrong:** 0.2111
- **active fraction correct:** 0.4438
- **active fraction wrong:** 0.2326
- **total active count:** 1303
- **activations on correct prompts in dataset:** 596
- **activations on wrong prompts in dataset:** 707
- **top relations:** P176:127, P276:91, P17:90, P449:85, P413:84
- **top subjects:** Malayali:3, Afghanistan:3, Honda CRF series:2, North Middlesex, Ontario:2, Kiev Peninsula:2

### Top activating prompts

#### Rank 1 | activation = 1341.761474609375

- **row_id:** 111
- **case_id:** 11850
- **fact_id:** cf_11850
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Steve Yzerman
- **relation_id:** P641
- **correct_answer:** hockey
- **target_true:** hockey
- **target_new:** football
- **generated_answer:**  ice hockey player who has played for the Detroit Red Wings of the National Hockey League
- **strict_answer_segment:** ice hockey player who has played for the Detroit Red Wings of the National Hockey League
- **strict_matched_answer:** hockey

**Prompt:**

> Repairs were completed in 1987. Steve Yzerman is a professional

#### Rank 2 | activation = 1193.81005859375

- **row_id:** 1703
- **case_id:** 6041
- **fact_id:** cf_6041
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Jermain Defoe
- **relation_id:** P641
- **correct_answer:** soccer
- **target_true:** soccer
- **target_new:** baseball
- **generated_answer:**  footballer who plays as a striker for Premier League club Sunderland and the England national team
- **strict_answer_segment:** footballer who plays as a striker for Premier League club Sunderland and the England national team

**Prompt:**

> Spain has an embassy in Harare. Jermain Defoe is a professional

#### Rank 3 | activation = 1144.665771484375

- **row_id:** 3378
- **case_id:** 3062
- **fact_id:** cf_3062
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Chris Paul
- **relation_id:** P641
- **correct_answer:** basketball
- **target_true:** basketball
- **target_new:** hockey
- **generated_answer:**  basketball player for the New Orleans Hornets. He was born on May 6,
- **strict_answer_segment:** basketball player for the New Orleans Hornets. He was born on May 6,
- **strict_matched_answer:** basketball

**Prompt:**

> Robert H. Michel (R)  . Chris Paul is a professional

#### Rank 4 | activation = 1046.366943359375

- **row_id:** 1167
- **case_id:** 16540
- **fact_id:** cf_16540
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Claudio Reyna
- **relation_id:** P641
- **correct_answer:** soccer
- **target_true:** soccer
- **target_new:** baseball
- **generated_answer:**  soccer player who plays for the New York Red Bulls. Claudio Reyna is a
- **strict_answer_segment:** soccer player who plays for the New York Red Bulls. Claudio Reyna is a
- **strict_matched_answer:** soccer

**Prompt:**

> The Squadron also developed “Fly Away” weekend comm exercises. Claudio Reyna is a professional

#### Rank 5 | activation = 1028.24560546875

- **row_id:** 4306
- **case_id:** 12659
- **fact_id:** cf_12659
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Hugo Sánchez
- **relation_id:** P641
- **correct_answer:** soccer
- **target_true:** soccer
- **target_new:** football
- **generated_answer:**  footballer who plays as a forward for Real Madrid and the Spain national team. He
- **strict_answer_segment:** footballer who plays as a forward for Real Madrid and the Spain national team. He

**Prompt:**

> It lay derelict by the early 13th century. Hugo Sánchez is a professional

#### Rank 6 | activation = 1001.8466796875

- **row_id:** 2854
- **case_id:** 16626
- **fact_id:** cf_16626
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Boris Diaw
- **relation_id:** P641
- **correct_answer:** basketball
- **target_true:** basketball
- **target_new:** football
- **generated_answer:**  of basketball. The plant is a perennial, and it is a member of the
- **strict_answer_segment:** of basketball. The plant is a perennial, and it is a member of the
- **strict_matched_answer:** basketball

**Prompt:**

> It also grows in both full sun or shade. Boris Diaw professionally plays the sport

#### Rank 7 | activation = 929.2603759765624

- **row_id:** 190
- **case_id:** 13145
- **fact_id:** cf_13145
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Arundel Formation
- **relation_id:** P131
- **correct_answer:** Maryland
- **target_true:** Maryland
- **target_new:** Illinois
- **generated_answer:**  geology, a group of sedimentary rocks in the United Kingdom that are part of the
- **strict_answer_segment:** geology, a group of sedimentary rocks in the United Kingdom that are part of the

**Prompt:**

> The major crops are cotton, wheat, and sugar cane. Arundel Formation, in

#### Rank 8 | activation = 903.1329345703124

- **row_id:** 2241
- **case_id:** 5451
- **fact_id:** cf_5451
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Toyota HiAce
- **relation_id:** P176
- **correct_answer:** Toyota
- **target_true:** Toyota
- **target_new:** Cadillac
- **generated_answer:**  the Japanese automaker Toyota. The Toyota HiAce is a van that was first introduced
- **strict_answer_segment:** the Japanese automaker Toyota. The Toyota HiAce is a van that was first introduced
- **strict_matched_answer:** Toyota

**Prompt:**

> The village forms part of the municipality of Zəngişalı. Toyota HiAce is a product of

#### Rank 9 | activation = 873.9639892578125

- **row_id:** 1031
- **case_id:** 13
- **fact_id:** cf_13
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Ferrari F40
- **relation_id:** P176
- **correct_answer:** Ferrari
- **target_true:** Ferrari
- **target_new:** Microsoft
- **generated_answer:**  the 1980s, and it is a car that is still
- **strict_answer_segment:** the 1980s, and it is a car that is still

**Prompt:**

> It is located in Baranivka Raion, Zhytomyr Oblast. Ferrari F40 is a product of

#### Rank 10 | activation = 871.35546875

- **row_id:** 1124
- **case_id:** 181
- **fact_id:** cf_181
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Thurman Munson
- **relation_id:** P413
- **correct_answer:** catcher
- **target_true:** catcher
- **target_new:** quarterback
- **generated_answer:**  a catcher for the New York Yankees.  Pin On Baseball  <h3>The first
- **strict_answer_segment:** a catcher for the New York Yankees.
- **strict_matched_answer:** catcher

**Prompt:**

> Positive stranded RNA virus transcription is the method of transcription. Thurman Munson plays as


## Layer 18, Feature 10787

- **fraction diff correct - wrong:** 0.1004
- **active fraction correct:** 0.1191
- **active fraction wrong:** 0.0188
- **total active count:** 217
- **activations on correct prompts in dataset:** 160
- **activations on wrong prompts in dataset:** 57
- **top relations:** P176:119, P178:72, P108:23, P264:3
- **top subjects:** Ferrari Berlinetta Boxer:2, Chevrolet Corvette C5-R:2, iPod shuffle:2, Porsche Panamera:2, Suzuki MR Wagon:2

### Top activating prompts

#### Rank 1 | activation = 576.8019409179688

- **row_id:** 262
- **case_id:** 2081
- **fact_id:** cf_2081
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** IBM Network Control Program
- **relation_id:** P178
- **correct_answer:** IBM
- **target_true:** IBM
- **target_new:** Boeing
- **generated_answer:**  IBM, is a software package that provides a comprehensive solution for managing and controlling network
- **strict_answer_segment:** IBM, is a software package that provides a comprehensive solution for managing and controlling network
- **strict_matched_answer:** IBM

**Prompt:**

> Soviet Cup winner: 1989. IBM Network Control Program, a product developed by

#### Rank 2 | activation = 575.754150390625

- **row_id:** 3190
- **case_id:** 20464
- **fact_id:** cf_20464
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** iChat
- **relation_id:** P178
- **correct_answer:** Apple
- **target_true:** Apple
- **target_new:** Square
- **generated_answer:**  Acrosoft, was acquired by Hyland Software in 2016
- **strict_answer_segment:** Acrosoft, was acquired by Hyland Software in 2016

**Prompt:**

> In May 2016, the company sold Acrosoft to Hyland Software. iChat, a product developed by

#### Rank 3 | activation = 564.6746826171875

- **row_id:** 288
- **case_id:** 11146
- **fact_id:** cf_11146
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** iPod shuffle
- **relation_id:** P178
- **correct_answer:** Apple
- **target_true:** Apple
- **target_new:** Sega
- **generated_answer:**  Apple, is a small, portable music player that can be used to listen to
- **strict_answer_segment:** Apple, is a small, portable music player that can be used to listen to
- **strict_matched_answer:** Apple

**Prompt:**

> 0 !! iPod shuffle, a product created by

#### Rank 4 | activation = 543.878662109375

- **row_id:** 2123
- **case_id:** 17807
- **fact_id:** cf_17807
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** False
- **subject:** Front Mission 3
- **relation_id:** P178
- **correct_answer:** Square
- **target_true:** Square
- **target_new:** Google
- **generated_answer:**  Carnegie Vanguard's students, was awarded the 2011 National Science
- **strict_answer_segment:** Carnegie Vanguard's students, was awarded the 2011 National Science

**Prompt:**

> Carnegie Vanguard's academics have been widely recognized in the country. Front Mission 3, a product created by

#### Rank 5 | activation = 533.1940307617188

- **row_id:** 3681
- **case_id:** 12794
- **fact_id:** cf_12794
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** IBM Parallel Sysplex
- **relation_id:** P178
- **correct_answer:** IBM
- **target_true:** IBM
- **target_new:** Apple
- **generated_answer:**  IBM to provide a high-availability solution for large-scale computing environments. The
- **strict_answer_segment:** IBM to provide a high-availability solution for large-scale computing environments. The
- **strict_matched_answer:** IBM

**Prompt:**

> : M’ stába tâ dâ. IBM Parallel Sysplex was developed by

#### Rank 6 | activation = 532.826416015625

- **row_id:** 1333
- **case_id:** 12422
- **fact_id:** cf_12422
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** Renault 4P
- **relation_id:** P176
- **correct_answer:** Renault
- **target_true:** Renault
- **target_new:** BMW
- **generated_answer:**  Renault in 1961, was a small car with a 4
- **strict_answer_segment:** Renault in 1961, was a small car with a 4
- **strict_matched_answer:** Renault

**Prompt:**

> (1951) On the Experimental Attainment of Optimum Conditions (with discussion). Renault 4P, produced by

#### Rank 7 | activation = 522.173583984375

- **row_id:** 2127
- **case_id:** 14920
- **fact_id:** cf_14920
- **variant_id:** paraphrase_01
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Hwasong-5
- **relation_id:** P176
- **correct_answer:** Iran
- **target_true:** Iran
- **target_new:** Honda
- **generated_answer:**  North Korea, is a three-stage solid-fuelled ballistic missile with a
- **strict_answer_segment:** North Korea, is a three-stage solid-fuelled ballistic missile with a

**Prompt:**

> Seven of these are endemic. Hwasong-5, developed by

#### Rank 8 | activation = 509.2745971679688

- **row_id:** 982
- **case_id:** 10819
- **fact_id:** cf_10819
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_wrong
- **is_correct:** True
- **subject:** Lancia Ypsilon
- **relation_id:** P176
- **correct_answer:** Fiat
- **target_true:** Fiat
- **target_new:** Chrysler
- **generated_answer:**  the Italian company Fiat, is a compact car with a 1.4-
- **strict_answer_segment:** the Italian company Fiat, is a compact car with a 1.4-
- **strict_matched_answer:** Fiat

**Prompt:**

> Optimality  It is known that Grover's algorithm is optimal. Lancia Ypsilon, developed by

#### Rank 9 | activation = 504.3367919921875

- **row_id:** 2126
- **case_id:** 14920
- **fact_id:** cf_14920
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** wrong_wrong
- **is_correct:** False
- **subject:** Hwasong-5
- **relation_id:** P176
- **correct_answer:** Iran
- **target_true:** Iran
- **target_new:** Honda
- **generated_answer:**  North Korea, is a long-range missile that can reach the United States.
- **strict_answer_segment:** North Korea, is a long-range missile that can reach the United States.

**Prompt:**

> It is a biopic of Empress Elisabeth of Austria. Hwasong-5, created by

#### Rank 10 | activation = 501.3934020996094

- **row_id:** 3680
- **case_id:** 12794
- **fact_id:** cf_12794
- **variant_id:** paraphrase_00
- **variant_source:** paraphrase_prompts
- **pair_type:** correct_correct
- **is_correct:** True
- **subject:** IBM Parallel Sysplex
- **relation_id:** P178
- **correct_answer:** IBM
- **target_true:** IBM
- **target_new:** Apple
- **generated_answer:**  IBM, is a mainframe computer system that allows multiple IBM mainframe computers to share a
- **strict_answer_segment:** IBM, is a mainframe computer system that allows multiple IBM mainframe computers to share a
- **strict_matched_answer:** IBM

**Prompt:**

> The track features Kate Havnevik on guest vocals and co-writing. IBM Parallel Sysplex, a product manufactured by

