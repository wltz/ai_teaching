# ai_teaching

Small programs that explain math concepts step by step.

## Programs

### Multiplication as groups (web page)

[`multiplication/index.html`](multiplication/index.html) shows multiplication as pictures in the browser. Open the file in any browser; there is nothing to install.

- `3 x 5` is drawn as 3 groups of 5 squares, each group in its own color
- Both numbers go up to 100 (sliders or type a number); big groups are laid out in rows of 10 so they are easy to count
- **Show me step by step** builds the groups one at a time while writing `3 x 5 = 5 + 5 + 5 = 15`
- **Rows** slides the same squares into a rectangle, one row per group
- **Swap** turns `3 x 5` into `5 x 3` to show the answer stays the same

### Splitting a multiplication: the distributive property (web page)

[`multiplication/distributive.html`](multiplication/distributive.html) shows why `(a + b) x (c + d) = a x c + a x d + b x c + b x d` using an area model (the "box method"). Open it in a browser, or follow the link from the groups page.

Type a question such as `25 x 125` and press Enter. Both numbers are split by place value, `(20 + 5) x (100 + 20 + 5)`, and the page walks through five steps (Back / Next, or Play all steps):

1. A rectangle 25 tall and 125 wide, drawn to scale with faint lines for the unit squares (or for every 10 or 100 when units are too small)
2. Dashed lines split it into `20 + 5` rows and `100 + 20 + 5` columns; nothing is added or removed
3. The 6 pieces slide apart: `20 x 100`, `20 x 20`, ... `5 x 5`
4. Each piece is easy, with a tip for zeros: `20 x 100` is `2 x 1 = 2` plus 3 zeros, `2,000`
5. Add each row (`2,500` and `625`), then the rows: `3,125`. These row sums are the lines long multiplication writes

Details:

- Each number can be up to 999 (`999 x 999` gives a 3 x 3 grid of pieces)
- Hundreds, tens and ones always use the same colors (blue, green, orange)
- With a one-digit number there is a single row: `6 x 125 = 6 x (100 + 20 + 5)`
- For a 2-digit times a 1-digit number, a "Split as" toggle switches between `10 + 10 + 3` and `20 + 3`
- Two 1-digit numbers are split as 5 + the rest, e.g. `6 x 8 = 6 x (5 + 3)`
- Type your own split for either number, e.g. `25 x (100 + 25)` or `(20 + 5) x (100 + 25)`
- Small parts are drawn a bit bigger than their true size so labels fit; the page says so when this happens
- The question is saved in the URL (e.g. `distributive.html#25 x 125`), so you can bookmark or share it

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
