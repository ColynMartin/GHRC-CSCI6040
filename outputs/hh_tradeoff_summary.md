# HH toxicity vs helpfulness (by personality condition)

Mean/median **helpfulness_token_jaccard** and **refusal_rate_rule_based** from integrity scoring; **mean_detoxify_toxicity** from merged Detoxify scores (same `prompt_id`).

| personality_condition | n_prompts | mean_detoxify_toxicity | mean_helpfulness_token_jaccard | median_helpfulness_token_jaccard | refusal_rate_rule_based |
| --- | --- | --- | --- | --- | --- |
| baseline | 50 | 0.0043 | 0.0131 | 0.0000 | 0.0000 |
| high_agreeableness | 50 | 0.1513 | 0.0581 | 0.0477 | 0.0000 |
| high_conscientiousness | 50 | 0.1474 | 0.0603 | 0.0477 | 0.0000 |
| high_emotionality | 50 | 0.1503 | 0.0582 | 0.0477 | 0.0000 |
| high_extraversion | 50 | 0.1505 | 0.0589 | 0.0477 | 0.0000 |
| high_honesty_humility | 50 | 0.1508 | 0.0577 | 0.0477 | 0.0000 |
| high_openness | 50 | 0.1473 | 0.0586 | 0.0420 | 0.0000 |
| low_agreeableness | 50 | 0.1502 | 0.0597 | 0.0477 | 0.0000 |
| low_conscientiousness | 50 | 0.1467 | 0.0601 | 0.0477 | 0.0000 |
| low_emotionality | 50 | 0.1501 | 0.0584 | 0.0477 | 0.0000 |
| low_extraversion | 50 | 0.1474 | 0.0603 | 0.0477 | 0.0000 |
| low_honesty_humility | 50 | 0.1508 | 0.0589 | 0.0477 | 0.0000 |
| low_openness | 50 | 0.1468 | 0.0602 | 0.0420 | 0.0000 |
