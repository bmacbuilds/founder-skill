---
title: run the numbers
ask: Run the numbers on my business
description: >-
  Your CFO. Builds the unit economics of a business before money is spent: what one unit earns after its direct costs,
  the real profit margin at the planned volume, the break-even point in units a day, year 1 month by month, the cash
  needed before it pays for itself, how long the startup spend takes to earn back, and what happens if the price
  drops, sales come in low or costs rise. Every number traces to an input the user can check. Use when the user says
  "find the profit margins", "do the numbers", "is this profitable", "break-even", "unit economics", "how much do I
  need to start", or "run the CFO".
---

# Run the numbers

The person who asks "and what does that cost?" Margins decide whether a good idea
is a business. This skill finds them, with every number traceable to an input.

Tool in this folder:

```bash
python3 "<this command's folder>/unit_economics.py" founder/numbers.json --out founder/cfo.md
```

## Step 1: gather the inputs

Write `founder/numbers.json` (shape: `example.json` in this folder, a walk-in
matcha café). It needs:

| field | what goes in it |
| --- | --- |
| `business` | the business's name, at the top of the report |
| `unit` | what one sale is: a cup, an order, a client-month, a seat |
| `price` | price per unit before tax |
| `variable` | the cost of ONE unit: ingredients, packaging, shipping, card fees, per-sale commissions |
| `fixed_monthly` | what you pay every month regardless: rent, salaries, software, insurance |
| `startup` | one-off spend before opening: deposits, build-out, equipment, first inventory, launch ads |
| `plan_per_day` | the volume once it is up and running |
| `ramp_per_day` | 12 numbers: realistic volume in each month of year 1 |
| `capacity_per_day` | the most you can physically sell in a day, if there is a limit |
| `days_per_month` | the days it sells in a month (30 if left out: say so if they trade fewer) |

Where the numbers come from, in this order:

1. The user's own quotes, invoices, leases and supplier price lists.
2. Public prices the user can check (a supplier's price list, a landlord's listing,
   a payment processor's published fees). Write the source next to the number in
   `founder/cfo-sources.md`.
3. Your estimate, clearly marked as an estimate, with the reasoning. Never present
   an estimate as a fact.

Ask the user for anything only they know (rent quoted, wages they will pay). Use the
price from `founder/pricing.md` or `founder/pitch.md` if those exist.

**The ramp is where plans lie.** Month 1 is almost never the plan volume. If the
buyer panel ran, use its buy rate and first-month purchases to sanity-check the
ramp (`founder/panel/results.md`), and say how you did it. With no panel and only a
starting volume, ask once how it grows and when. If they do not know, run their plan as
given, add the what-if at half the volume, and say that month 1 is rarely the plan.

## Step 2: run it

```bash
python3 "<this command's folder>/unit_economics.py" founder/numbers.json --out founder/cfo.md
```

It writes: the per-unit table and the contribution (what each sale leaves after
its own costs), fixed costs, the break-even in units a day, the profit margin at
the plan volume, year 1 month by month, the year 1 operating profit and the result
after the startup spend, the cash needed before it pays for itself, the month the
startup money is earned back, and a what-if table (price -10%, volume -20%, unit
costs +15%). It flags a price below variable cost, a break-even above capacity, a
losing year 1 and a payback beyond 12 months.

What-ifs without editing the file:

```bash
python3 "<this command's folder>/unit_economics.py" founder/numbers.json --price 7.00
python3 "<this command's folder>/unit_economics.py" founder/numbers.json --volume 0.8
```

A cost what-if (unit costs or a fixed cost) has no flag: copy `founder/numbers.json` to
`founder/numbers-whatif.json`, change only that cost, and run the tool on the copy without
`--out`, so `founder/cfo.md` is left as it is.

## Step 3: the CFO's note

Add a short section at the top of `founder/cfo.md`, in plain words. A run with `--out`
writes that file afresh, so after any rerun, add the note again.

- **The margin**: the profit margin at plan, and the contribution per unit.
- **The line to watch**: the one cost or assumption that moves the result most
  (usually the ramp, rent or the price), with the what-if that proves it.
- **Cash**: how much money the founder needs before it pays for itself. If part of the
  startup spend is already spent, say so: the tool counts all of it.
- **Three ways to improve the margin**, each with the number it changes and by how
  much (run the what-if, do not guess).
- Whether the board's conditions about money (`founder/board.md`) are met. If the board
  has not run, say so in one line.

## Rules

- Every number in your note comes from the tool's output or an input you can name.
- Revenue is before tax; say if the user's market adds sales tax on top.
- Not financial, tax or legal advice. Say once that an accountant should check the
  structure, payroll costs and tax before money moves.

## Output

`founder/numbers.json`, `founder/cfo.md`, `founder/cfo-sources.md`. Next:
`/founder-plan` uses these numbers for the verdict; `/founder-pricing` if the
margin is thin.
