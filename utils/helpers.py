def ask(label, validator=None):
    while True:
        value = input(f"{label}: ").strip()
        error = validator(value) if validator else None
        if error:
            print(f"  [Error] {error}")
        else:
            return value


def choose(title, options):
    print(f"\n{title}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        pick = input("Enter option number: ").strip()
        if pick.isdigit() and 1 <= int(pick) <= len(options):
            return options[int(pick) - 1]
        print(f"  [Error] Please enter a number between 1 and {len(options)}.")


def print_table(headers, rows):
    if not rows:
        print("  No records found.")
        return
    rows = [[str(c) for c in r] for r in rows]
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)]
    line = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    print(line)
    print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, widths)) + " |")
    print(line)
    for r in rows:
        print("| " + " | ".join(c.ljust(w) for c, w in zip(r, widths)) + " |")
    print(line)
