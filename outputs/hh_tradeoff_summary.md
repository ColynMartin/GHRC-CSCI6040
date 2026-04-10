# HH toxicity vs helpfulness (by personality condition)

Mean/median **helpfulness_token_jaccard** and **refusal_rate_rule_based** from integrity scoring; **mean_detoxify_toxicity** from merged Detoxify scores (same `prompt_id`).

| personality_condition | n_prompts | mean_detoxify_toxicity | mean_helpfulness_token_jaccard | median_helpfulness_token_jaccard | refusal_rate_rule_based |
| --- | --- | --- | --- | --- | --- |
| baseline | 50 | 0.0117 | 0.0130 | 0.0000 | 0.0000 |
| high_agreeableness | 50 | 0.2118 | 0.0582 | 0.0477 | 0.0000 |
| high_conscientiousness | 50 | 0.2107 | 0.0601 | 0.0477 | 0.0000 |
| high_emotionality | 50 | 0.2187 | 0.0580 | 0.0477 | 0.0000 |
| high_extraversion | 50 | 0.2194 | 0.0587 | 0.0477 | 0.0000 |
| high_honesty_humility | 50 | 0.2117 | 0.0578 | 0.0477 | 0.0000 |
| high_openness | 50 | 0.2103 | 0.0584 | 0.0420 | 0.0000 |
| low_agreeableness | 50 | 0.2211 | 0.0595 | 0.0477 | 0.0000 |
| low_conscientiousness | 50 | 0.2097 | 0.0600 | 0.0477 | 0.0000 |
| low_emotionality | 50 | 0.2185 | 0.0582 | 0.0477 | 0.0000 |
| low_extraversion | 50 | 0.2104 | 0.0601 | 0.0477 | 0.0000 |
| low_honesty_humility | 50 | 0.2184 | 0.0587 | 0.0477 | 0.0000 |
| low_openness | 50 | 0.2091 | 0.0600 | 0.0420 | 0.0000 |
