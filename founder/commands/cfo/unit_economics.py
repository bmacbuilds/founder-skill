#!/usr/bin/env python3
"""Unit economics for founder-cfo. Standard library only, no network.

Takes one JSON file describing the business and prints the numbers a CFO would
check before a single dollar is spent: what one unit earns, the real margin at
the volume you plan, how many units a day you need to break even, what year 1
looks like month by month, and how long it takes to earn the startup money back.

    python3 unit_economics.py founder/numbers.json
    python3 unit_economics.py founder/numbers.json --out founder/cfo.md
    python3 unit_economics.py founder/numbers.json --json
    python3 unit_economics.py founder/numbers.json --price 7.00 --volume 0.8

The input (see example.json in this folder):

    business          name, for the report
    unit              what you sell one of: "cup", "order", "client-month"
    price             price per unit, before tax
    variable          [{label, cost}]  cost of ONE unit: ingredients, packaging,
                      shipping, card fees, a per-unit commission. A cost that is a
                      share of the price takes percent_of_price, with or without a
                      cost: a card fee of 2.9% + $0.30 is
                      {"label": "card fees", "percent_of_price": 2.9, "cost": 0.30},
                      and a what-if price works it out again
    fixed_monthly     [{label, cost}]  costs you pay every month whatever you sell:
                      rent, salaries, software, insurance
    startup           [{label, cost}]  one-off spend before you open
    days_per_month    selling days in a month (default 30)
    capacity_per_day  the most units a day you can physically sell (optional)
    plan_per_day      the volume you plan for once you are up and running
    ramp_per_day      12 numbers: units a day in each month of year 1
                      (optional; default = plan_per_day every month)

Every number in the report comes from that file. Nothing is looked up or
guessed. If a field is missing the tool says so instead of filling it in.

--price and --volume run a what-if without editing the file: --price replaces
the price, --volume scales every volume (0.8 = 20 percent fewer sales).
"""

import argparse
import decimal
import json
import math
import sys


class NumbersError(Exception):
    pass



def _units(n, unit):
    """'1 groom', '2 grooms', '1,500 cups': a count with its unit, singular for one."""
    return "%s %s" % ("{:,.0f}".format(n), unit if n == 1 else unit + "s")

def _exact(v):
    """A break-even worked out, before it is rounded up to whole units: 1.33, 0.96, 2.5."""
    return ("{:,.2f}".format(v)).rstrip("0").rstrip(".")


def _breakeven(be, unit):
    """The break-even line's two halves: '1.03 grooms a day on average' and ' (in whole grooms, 2 a day covers it)',
    or '3 grooms a day' and '' when it is exact. The worked-out figure comes first, so "below that" can only mean it."""
    whole = math.ceil(be)
    if abs(be - whole) <= 1e-9:
        return "%s a day" % _units(whole, unit), ""
    return ("%s %ss a day on average" % (_exact(be), unit),
            " (in whole %ss, %s a day covers it)" % (unit, _units(whole, unit)))


def _money(v):
    """Dollars and cents, a half rounded up as a calculator does ($3.055 is $3.06, not $3.05)."""
    sign = "-" if v < 0 else ""
    cents = decimal.Decimal(repr(round(abs(v), 9))).quantize(decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP)
    return "%s$%s" % (sign, "{:,.2f}".format(cents))


def _whole(v):
    sign = "-" if v < 0 else ""
    return "%s$%s" % (sign, "{:,.0f}".format(abs(round(v))))


def _sum(items, field):
    total = 0.0
    for i, it in enumerate(items or []):
        if not isinstance(it, dict) or "cost" not in it:
            raise NumbersError("%s[%d] needs a 'cost'" % (field, i))
        try:
            total += float(it["cost"])
        except (TypeError, ValueError):
            raise NumbersError("%s[%d].cost is not a number: %r" % (field, i, it["cost"]))
    return total


def unit_cost(it, price):
    """One variable cost for one unit at this price: its fixed part ('cost') plus its share of the price
    ('percent_of_price'), so a card fee of 2.9% + $0.30 is worked out again at every what-if price."""
    return float(it.get("cost") or 0) + price * float(it.get("percent_of_price") or 0) / 100


def _sum_variable(items, price):
    total = 0.0
    for i, it in enumerate(items or []):
        if not isinstance(it, dict) or not ("cost" in it or "percent_of_price" in it):
            raise NumbersError("variable[%d] needs a 'cost', a 'percent_of_price' or both" % i)
        try:
            total += unit_cost(it, price)
        except (TypeError, ValueError):
            raise NumbersError("variable[%d] is not a number: %r" % (i, it))
    return total


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise NumbersError("no such file: %s" % path)
    except json.JSONDecodeError as e:
        raise NumbersError("%s is not valid JSON: %s" % (path, e))


def analyse(spec, price=None, volume=1.0):
    """Return a dict of every number in the report. Pure function, easy to test."""
    if "price" not in spec and price is None:
        raise NumbersError("'price' is missing")
    p = float(price if price is not None else spec["price"])
    if p <= 0:
        raise NumbersError("price must be above zero")
    days = float(spec.get("days_per_month", 30))
    var = _sum_variable(spec.get("variable"), p)
    fixed = _sum(spec.get("fixed_monthly"), "fixed_monthly")
    startup = _sum(spec.get("startup"), "startup")

    if "plan_per_day" not in spec and "ramp_per_day" not in spec:
        raise NumbersError("give 'plan_per_day' or 'ramp_per_day' (12 numbers)")
    plan = float(spec.get("plan_per_day", 0)) * volume
    ramp = spec.get("ramp_per_day")
    if ramp is None:
        ramp = [plan] * 12
    else:
        if len(ramp) != 12:
            raise NumbersError("'ramp_per_day' needs 12 numbers, one per month (got %d)" % len(ramp))
        ramp = [float(v) * volume for v in ramp]
    if not plan:
        plan = ramp[-1]

    contribution = p - var
    contribution_pct = contribution / p
    breakeven_day = math.inf if contribution <= 0 else fixed / (contribution * days)
    plan_units_month = plan * days
    margin_at_plan = (contribution - (fixed / plan_units_month if plan_units_month else math.inf)) / p

    months = []
    cumulative = -startup
    payback_month = None
    for m, per_day in enumerate(ramp, start=1):
        units = per_day * days
        revenue = units * p
        variable_cost = units * var
        profit = revenue - variable_cost - fixed
        cumulative += profit
        if payback_month is None and cumulative >= 0:
            payback_month = m
        months.append({"month": m, "per_day": per_day, "units": units, "revenue": revenue,
                       "variable": variable_cost, "fixed": fixed, "profit": profit,
                       "cumulative": cumulative})
    year_profit = sum(m["profit"] for m in months)
    year_revenue = sum(m["revenue"] for m in months)
    # the cash you need: startup plus the deepest hole the monthly losses dig
    lowest = min([-startup] + [m["cumulative"] for m in months])
    cash_needed = -lowest

    capacity = spec.get("capacity_per_day")
    flags = []
    if contribution <= 0:
        flags.append("Each unit loses money before rent and salaries: the price is below the variable cost.")
    if capacity is not None and not math.isinf(breakeven_day) and breakeven_day > float(capacity):  # never: the flag above
        flags.append("Break-even needs %s a day but capacity is %s." % (
            _units(round(breakeven_day), spec.get("unit", "unit")), capacity))
    if capacity is not None and plan > float(capacity):
        flags.append("The plan (%.0f a day) is above capacity (%s)." % (plan, capacity))
    if year_profit < 0:
        flags.append("Year 1 loses money on operations (%s)." % _whole(year_profit))
    if payback_month is None:
        flags.append("The startup spend is not earned back within year 1.")

    return {
        "business": spec.get("business", ""), "unit": spec.get("unit", "unit"),
        "price": p, "variable_per_unit": var, "contribution": contribution,
        "contribution_pct": contribution_pct, "fixed_monthly": fixed, "startup": startup,
        "plan_per_day": plan, "margin_at_plan": margin_at_plan, "breakeven_per_day": breakeven_day,
        "capacity_per_day": capacity, "year1_revenue": year_revenue, "year1_profit": year_profit,
        "year1_after_startup": year_profit - startup, "payback_month": payback_month,
        "cash_needed": cash_needed, "months": months, "flags": flags,
        "variable_items": spec.get("variable", []), "fixed_items": spec.get("fixed_monthly", []),
        "startup_items": spec.get("startup", []),
    }


def sensitivity(spec):
    """The three what-ifs every plan should survive."""
    base = analyse(spec)
    rows = [("Base plan", base)]
    rows.append(("Price -10%", analyse(spec, price=base["price"] * 0.9)))
    rows.append(("Volume -20%", analyse(spec, volume=0.8)))
    worse = json.loads(json.dumps(spec))
    for it in worse.get("variable", []):
        for k in ("cost", "percent_of_price"):
            if it.get(k):
                it[k] = float(it[k]) * 1.15
    rows.append(("Unit costs +15%", analyse(worse)))
    return rows


def report(spec, a, what_if=None):
    """what_if names what a --price or --volume run changed, so the report says it is a what-if, not the plan."""
    u = a["unit"]
    at = "at this what-if" if what_if else "at your plan"
    L = []
    L.append("# Unit economics: %s" % (a["business"] or "your business"))
    L.append("")
    L.append("Every number below comes from the input file. Nothing is looked up or guessed.")
    if what_if:
        L.append("")
        L.append("**This is a what-if: %s.** The plan in the file is unchanged." % what_if)
    L.append("")
    L.append("## One %s" % u)
    L.append("")
    L.append("| line | per %s |" % u)
    L.append("| --- | ---: |")
    L.append("| Price | %s |" % _money(a["price"]))
    for it in a["variable_items"]:
        label = it.get("label", "cost")
        if it.get("percent_of_price"):
            label += " (%s%% of the price%s)" % ("%g" % float(it["percent_of_price"]),
                                                 " + %s" % _money(float(it["cost"])) if it.get("cost") else "")
        L.append("| %s | -%s |" % (label, _money(unit_cost(it, a["price"]))))
    L.append("| **Contribution** (what each %s leaves to pay the fixed costs) | **%s** (%.0f%%) |"
             % (u, _money(a["contribution"]), a["contribution_pct"] * 100))
    L.append("")
    L.append("## The margin that matters")
    L.append("")
    L.append("Fixed costs: %s a month (%s)." % (_whole(a["fixed_monthly"]), ", ".join(
        "%s %s" % (it.get("label", "cost"), _whole(float(it["cost"]))) for it in a["fixed_items"]) or "none given"))
    L.append("")
    be = a["breakeven_per_day"]
    if math.isinf(be):
        L.append("- **Break-even: never.** Each %s loses money before rent and salaries." % u)
    else:
        L.append("- **Break-even: %s.** Below that you lose money every month%s." % _breakeven(be, u))
    L.append("- **Profit margin %s** (%s a day): **%.0f%%** of every sale, after every cost." % (
        at, "{:,.0f}".format(a["plan_per_day"]), a["margin_at_plan"] * 100))
    if a["capacity_per_day"] is not None:
        L.append("- Capacity: %s a day." % a["capacity_per_day"])
    L.append("")
    L.append("## Year 1, month by month")
    L.append("")
    L.append("| month | %ss a day | revenue | profit | cumulative (after %s startup) |" % (u, _whole(a["startup"])))
    L.append("| ---: | ---: | ---: | ---: | ---: |")
    for m in a["months"]:
        L.append("| %d | %s | %s | %s | %s |" % (m["month"], "{:,.0f}".format(m["per_day"]), _whole(m["revenue"]),
                                             _whole(m["profit"]), _whole(m["cumulative"])))
    L.append("")
    L.append("- **Year 1 operating profit: %s** on %s of revenue." % (_whole(a["year1_profit"]), _whole(a["year1_revenue"])))
    L.append("- After the %s startup spend: %s." % (_whole(a["startup"]), _whole(a["year1_after_startup"])))
    L.append("- Startup money earned back: %s." % ("month %d" % a["payback_month"] if a["payback_month"] else "not within year 1"))
    L.append("- Cash you need before it pays for itself: **%s**." % _whole(a["cash_needed"]))
    L.append("")
    L.append("## What if")
    L.append("")
    L.append("| scenario | margin %s | break-even a day, on average | year 1 profit |" % at)
    L.append("| --- | ---: | ---: | ---: |")
    for name, s in sensitivity(spec):
        be = s["breakeven_per_day"]
        L.append("| %s | %.0f%% | %s | %s |" % (name if not (what_if and name == "Base plan") else "This what-if",
                                              s["margin_at_plan"] * 100,
                                              "never" if math.isinf(be) else _exact(be),
                                              _whole(s["year1_profit"])))
    L.append("")
    if a["flags"]:
        L.append("## Red flags")
        L.append("")
        for f in a["flags"]:
            L.append("- %s" % f)
    else:
        L.append("No red flags in these numbers. They are only as good as the inputs: check every cost against a real quote.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("numbers", help="the business's numbers.json")
    ap.add_argument("--out", help="write the report here (markdown)")
    ap.add_argument("--json", action="store_true", help="print the numbers as JSON")
    ap.add_argument("--price", type=float, help="what-if price")
    ap.add_argument("--volume", type=float, default=1.0, help="what-if volume multiplier")
    args = ap.parse_args(argv)
    try:
        spec = load(args.numbers)
        if args.price is not None:
            spec = dict(spec, price=args.price)
        if args.volume != 1.0:
            spec = dict(spec)
            if "plan_per_day" in spec:
                spec["plan_per_day"] = float(spec["plan_per_day"]) * args.volume
            if "ramp_per_day" in spec:
                spec["ramp_per_day"] = [float(v) * args.volume for v in spec["ramp_per_day"]]
        a = analyse(spec)
    except NumbersError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if args.json:
        out = {k: v for k, v in a.items() if not k.endswith("_items")}
        out["breakeven_per_day"] = None if math.isinf(out["breakeven_per_day"]) else out["breakeven_per_day"]
        print(json.dumps(out, indent=1))
        return 0
    changed = []
    if args.price is not None:
        changed.append("the price at %s" % _money(args.price))
    if args.volume != 1.0:
        changed.append("every volume x %s" % ("%g" % args.volume))
    text = report(spec, a, " and ".join(changed) or None)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote %s" % args.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
