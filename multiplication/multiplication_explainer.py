#!/usr/bin/env python3
"""Explain multiplication step by step.

Usage:
    python multiplication_explainer.py 23 47      # explain 23 x 47
    python multiplication_explainer.py -1.5 4     # decimals and negatives work too
    python multiplication_explainer.py            # interactive: type two numbers
    python multiplication_explainer.py --quiz     # practice questions with explanations
"""
import argparse
import random
from decimal import Decimal, InvalidOperation

MAX_REPEATED_ADDITION = 10  # only show "4 + 4 + 4 ..." when there are this many groups or fewer
MAX_GRID = 12               # only draw a dot grid up to 12 x 12


def fmt(x):
    """Format a Decimal without scientific notation or trailing zeros."""
    s = format(x.normalize(), "f")
    return s if s != "-0" else "0"


def parse_number(text):
    try:
        value = Decimal(text.strip())
    except InvalidOperation:
        raise ValueError(f"'{text}' is not a number")
    if not value.is_finite():
        raise ValueError(f"'{text}' is not a finite number")
    return value


def heading(title):
    return f"\n== {title} ==\n"


def explain_meaning(a, b):
    lines = [heading("What it means")]
    lines.append(f"{a} x {b} means \"{b} groups of {a}\" (or \"{a} groups of {b}\" -- the order")
    lines.append("doesn't matter, the answer is the same).")
    return lines


def explain_repeated_addition(a, b):
    """a, b are non-negative ints. Use the smaller one as the number of groups."""
    groups, size = (b, a) if b <= a else (a, b)
    if groups > MAX_REPEATED_ADDITION:
        return []
    lines = [heading("Repeated addition")]
    lines.append(f"Add {size} to itself {groups} times:")
    total = 0
    for i in range(1, groups + 1):
        total += size
        lines.append(f"  {i:>2} group{'s' if i > 1 else ' '}: {' + '.join([str(size)] * i)} = {total}")
    return lines


def explain_grid(a, b):
    if a > MAX_GRID or b > MAX_GRID or a == 0 or b == 0:
        return []
    lines = [heading("Picture it as a grid")]
    lines.append(f"{a} rows of {b} dots. Count them all to get the answer:")
    for _ in range(a):
        lines.append("  " + " ".join(["o"] * b))
    lines.append(f"{a} rows x {b} dots = {a * b} dots")
    return lines


def single_digit_steps(a, d):
    """Multiply int a by a single digit d, right to left, showing carries."""
    lines = []
    carry = 0
    written = []
    for x in reversed([int(c) for c in str(a)]):
        p = x * d + carry
        step = f"    {x} x {d} = {x * d}"
        if carry:
            step += f", plus carry {carry} = {p}"
        step += f" -> write {p % 10}"
        if p // 10:
            step += f", carry {p // 10}"
        lines.append(step)
        written.append(str(p % 10))
        carry = p // 10
    if carry:
        lines.append(f"    no digits left -> write the carry {carry}")
        written.append(str(carry))
    result = int("".join(reversed(written)))
    assert result == a * d
    return lines, result


def explain_long_multiplication(a, b):
    """a, b are non-negative ints with b having at least two digits."""
    lines = [heading("Break it up by place value")]
    digits = [(int(c), 10 ** i) for i, c in enumerate(reversed(str(b))) if c != "0"]
    pieces = [str(d * place) for d, place in reversed(digits)]
    lines.append(f"Split {b} into its places: {b} = {' + '.join(pieces)}")
    lines.append(f"Multiply {a} by each piece, then add the results:")

    partials = []
    for d, place in digits:
        step_lines, small = single_digit_steps(a, d)
        partial = small * place
        partials.append((d * place, partial))
        lines.append(f"\n  {a} x {d * place}:")
        lines.append(f"    first {a} x {d}:")
        lines.extend("  " + s for s in step_lines)
        lines.append(f"      = {small}")
        if place > 1:
            zeros = len(str(place)) - 1
            lines.append(f"    then x {place} (add {zeros} zero{'s' if zeros > 1 else ''}): {small} -> {partial}")

    total = sum(p for _, p in partials)
    lines.append("\n  Add the pieces: " + " + ".join(str(p) for _, p in partials) + f" = {total}")

    # The standard written layout.
    width = max(len(str(a)), len(str(b)) + 2, len(str(total))) + 2
    lines.append(heading("Written the usual way"))
    lines.append(f"{a:>{width}}")
    lines.append(f"{'x ' + str(b):>{width}}")
    lines.append("-" * width)
    for piece, partial in partials:
        lines.append(f"{partial:>{width}}   ({a} x {piece})")
    lines.append("-" * width)
    lines.append(f"{total:>{width}}")
    return lines


def explain_single_digit(a, b):
    """At least one factor is a single digit: show the carry steps directly."""
    big, d = (a, b) if b < 10 else (b, a)
    if big < 10:
        return []  # both single digits: grid / repeated addition already cover it
    lines = [heading("Digit by digit (right to left)")]
    step_lines, result = single_digit_steps(big, d)
    lines.extend(step_lines)
    lines.append(f"  Answer: {result}")
    return lines


def explain_integers(a, b):
    """Explain a x b for non-negative ints."""
    lines = explain_meaning(a, b)
    if a == 0 or b == 0:
        lines.append(heading("Multiplying by zero"))
        lines.append("Zero groups of anything (or any number of empty groups) is nothing,")
        lines.append(f"so {a} x {b} = 0.")
        return lines
    if a == 1 or b == 1:
        lines.append(heading("Multiplying by one"))
        lines.append(f"One group of a number is just that number, so {a} x {b} = {a * b}.")
        return lines
    lines += explain_repeated_addition(a, b)
    lines += explain_grid(a, b)
    if a >= 10 and b >= 10:
        # Put the shorter number on the bottom so there are fewer partial products.
        top, bottom = (a, b) if len(str(a)) >= len(str(b)) else (b, a)
        lines += explain_long_multiplication(top, bottom)
    else:
        lines += explain_single_digit(a, b)
    return lines


def decimal_places(x):
    return max(0, -x.normalize().as_tuple().exponent)


def explain(a, b):
    """Return the full explanation of a x b (Decimals) as a list of lines."""
    expected = a * b
    lines = [f"Explaining {fmt(a)} x {fmt(b)}"]

    negative = (a < 0) != (b < 0) and a != 0 and b != 0
    A, B = abs(a), abs(b)
    if a < 0 or b < 0:
        lines.append(f"\nFirst, ignore the signs and work out {fmt(A)} x {fmt(B)}. "
                     "We'll fix the sign at the end.")

    pa, pb = decimal_places(A), decimal_places(B)
    ia, ib = int(A * 10 ** pa), int(B * 10 ** pb)
    if pa or pb:
        lines.append(heading("Getting rid of the decimal points"))
        lines.append(f"{fmt(A)} has {pa} digit(s) after the point and {fmt(B)} has {pb}.")
        lines.append(f"Multiply as if there were no points: {ia} x {ib}.")
        lines.append(f"Then move the point back {pa} + {pb} = {pa + pb} place(s) to the left.")

    lines += explain_integers(ia, ib)
    result = Decimal(ia * ib)

    if pa or pb:
        result = result.scaleb(-(pa + pb))
        lines.append(heading("Put the decimal point back"))
        lines.append(f"{ia * ib} with the point moved {pa + pb} place(s) left is {fmt(result)}.")

    if a < 0 or b < 0:
        lines.append(heading("Fix the sign"))
        if a == 0 or b == 0:
            lines.append("The answer is zero, and zero has no sign.")
        elif negative:
            lines.append("One number is negative and one is positive -> the answer is negative.")
            result = -result
        else:
            lines.append("Both numbers are negative -> the negatives cancel, the answer is positive.")

    assert result == expected, (result, expected)
    lines.append(f"\nAnswer: {fmt(a)} x {fmt(b)} = {fmt(result)}")
    return lines


def interactive():
    print("Type two numbers to multiply (e.g. '23 47'), or 'q' to quit.")
    while True:
        try:
            text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if text.lower() in {"q", "quit", "exit"}:
            return
        parts = text.replace("x", " ").replace("*", " ").split()
        if len(parts) != 2:
            print("Please enter exactly two numbers, like: 12 x 7")
            continue
        try:
            a, b = parse_number(parts[0]), parse_number(parts[1])
        except ValueError as e:
            print(e)
            continue
        print("\n".join(explain(a, b)))


def quiz(rounds=5, low=2, high=12):
    score = 0
    for i in range(1, rounds + 1):
        a, b = random.randint(low, high), random.randint(low, high)
        try:
            answer = input(f"\nQuestion {i}/{rounds}: {a} x {b} = ? ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if answer == str(a * b):
            score += 1
            print("Correct!")
        else:
            print(f"Not quite -- the answer is {a * b}. Here's why:")
            print("\n".join(explain(Decimal(a), Decimal(b))))
    print(f"\nScore: {score}/{rounds}")


def main():
    parser = argparse.ArgumentParser(description="Explain multiplication step by step.")
    parser.add_argument("numbers", nargs="*", help="two numbers to multiply")
    parser.add_argument("--quiz", action="store_true", help="practice with random questions")
    parser.add_argument("--rounds", type=int, default=5, help="number of quiz questions")
    args = parser.parse_args()

    if args.quiz:
        quiz(args.rounds)
    elif len(args.numbers) == 2:
        try:
            a, b = parse_number(args.numbers[0]), parse_number(args.numbers[1])
        except ValueError as e:
            parser.error(str(e))
        print("\n".join(explain(a, b)))
    elif not args.numbers:
        interactive()
    else:
        parser.error("give exactly two numbers, or none for interactive mode")


if __name__ == "__main__":
    main()
