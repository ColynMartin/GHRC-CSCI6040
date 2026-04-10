# HH toxicity vs helpfulness (by personality condition)

Mean/median **helpfulness_token_jaccard** and **refusal_rate_rule_based** from integrity scoring; **mean_detoxify_toxicity** from merged Detoxify scores (same `prompt_id`).

| personality_condition | n_prompts | mean_detoxify_toxicity | mean_helpfulness_token_jaccard | median_helpfulness_token_jaccard | refusal_rate_rule_based |
| --- | --- | --- | --- | --- | --- |
| baseline | 200 | 0.0228 | 0.0610 | 0.0536 | 0.1600 |
| high_agreeableness | 200 | 0.0120 | 0.0577 | 0.0500 | 0.1900 |
| high_conscientiousness | 200 | 0.0086 | 0.0594 | 0.0557 | 0.2950 |
| high_emotionality | 200 | 0.0112 | 0.0592 | 0.0553 | 0.2750 |
| high_extraversion | 200 | 0.0156 | 0.0598 | 0.0556 | 0.1600 |
| high_honesty_humility | 200 | 0.0096 | 0.0584 | 0.0545 | 0.4100 |
| high_openness | 200 | 0.0287 | 0.0574 | 0.0521 | 0.1350 |
| low_agreeableness | 200 | 0.0061 | 0.0594 | 0.0526 | 0.4050 |
| low_conscientiousness | 200 | 0.0128 | 0.0605 | 0.0543 | 0.3250 |
| low_emotionality | 200 | 0.0075 | 0.0588 | 0.0548 | 0.2750 |
| low_extraversion | 200 | 0.0084 | 0.0621 | 0.0547 | 0.1950 |
| low_honesty_humility | 200 | 0.0128 | 0.0603 | 0.0528 | 0.4650 |
| low_openness | 200 | 0.0103 | 0.0609 | 0.0552 | 0.3600 |
