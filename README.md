# ai_teaching

Small programs that explain math concepts step by step.

## Programs

### Multiplication explainer

[`multiplication/multiplication_explainer.py`](multiplication/multiplication_explainer.py) explains any multiplication problem in several ways:

- **Meaning:** "a x b" as groups, and why order doesn't matter
- **Repeated addition:** `4 + 4 + 4 = 12` (small problems)
- **Dot grid:** rows of dots you can count (up to 12 x 12)
- **Place value:** splits `47 = 40 + 7`, multiplies each piece digit by digit with carries, then adds
- **Long multiplication:** the standard written layout
- **Decimals and negatives:** multiply without the decimal point and fix it afterwards, then apply the sign rule

Requires Python 3.8+ and no extra packages.

```bash
python3 multiplication/multiplication_explainer.py 23 47     # explain one problem
python3 multiplication/multiplication_explainer.py -1.5 2.25 # decimals and negatives
python3 multiplication/multiplication_explainer.py           # interactive: type "12 x 7"
python3 multiplication/multiplication_explainer.py --quiz    # practice questions, wrong answers get explained
```

Example:

```
== Written the usual way ==

    23
  x 47
------
   161   (23 x 7)
   920   (23 x 40)
------
  1081
```
