#!/usr/bin/env python3
"""The figure on the Filter Expressions page.

    uv run python dev/diagrams/filter_expressions.py

Writes ``docs/images/features/filter-expressions/filter-expr-flow_{light,dark}.{svg,png}``.

Both lanes are components of the iris demo's *Iris Petal Analysis* tab in
depictio v1.21.0 (``depictio/projects/init/iris/dashboards/petal_analysis.yaml``):
the card ``card-long-petal-share`` (count, ``filter_expr: "col('petal.length') > 4"``)
and the MultiSelect ``long-petal-variety-filter`` (``variety``, same expression).

* A card: the scan carries the dashboard's filters, then ``filter_expr``
  narrows it, then the aggregation runs (``bulk_compute_cards`` in
  ``dashboards_endpoints/routes.py``).
* An interactive: its options come from ``/deltatables/unique_values`` with the
  expression and nothing else (``fetchUniqueValues`` in react-core ``api.ts``),
  so Setosa never appears. A value picked there is emitted with the
  expression (``MultiSelectRenderer``), and ``process_metadata_and_filter``
  ANDs it onto the value filter for every other component.

Counts are ``iris.csv``'s: 150 flowers, 50 Versicolor, 34 of them with a petal
over 4 cm, 84 such flowers in all, none of them Setosa.
"""

from __future__ import annotations

from pathlib import Path

from component_types import key, type_badge
from concepts import edge, icon, ink, rrect, shadow_defs, solid, white
from sketch import Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "features" / "filter-expressions"


def stage(s: Sketch, x: float, y: float, w: float, k: str, ico: str, title: str, lines: tuple[str, ...], count: str) -> None:
    """One step of the pipeline: what narrows the rows, and how many are left."""
    t = s.theme
    rrect(s, x, y, w, 112, fill=t.fill(k), stroke=edge(t, k), r=12, width=1.6)
    icon(s, ico, x + 22, y + 24, 19, solid(t, k))
    s.text(x + 40, y + 30, title, size=15, anchor="start", weight="bold", colour=ink(t, k))
    for i, line in enumerate(lines):
        s.text(x + 14, y + 56 + i * 20, line, size=13, anchor="start")
    s.text(x + w - 14, y + 100, count, size=14, anchor="end", weight="bold", colour=t.dim)


def lane_title(s: Sketch, y: float, title: str, sub: str) -> None:
    t = s.theme
    s.text(30, y, title, size=18, anchor="start", weight="bold")
    s.text(30, y + 22, sub, size=13, anchor="start", colour=t.dim)


def filter_expr_flow(theme: Theme) -> Sketch:
    t = theme
    s = Sketch(960, 600, theme=t)
    shadow_defs(s)
    s.heading(30, 46, "Where `filter_expr` narrows the rows", "two components of the iris demo's Iris Petal Analysis tab, with the same expression")
    expr = "`col('petal.length') > 4`"
    w, gap = 196, 34
    xs = [30 + i * (w + gap) for i in range(4)]

    # Lane 1: a card aggregates what the filters, then the expression, leave.
    y = 160
    lane_title(s, 124, "On a card", "`card-long-petal-share`: on top of the dashboard's filters, before the count")
    stage(s, xs[0], y, w, "collection", "table", "`iris_table`", ("every flower",), "150 rows")
    stage(s, xs[1], y, w, "you", "filter-variant", "Dashboard filters", ("Variety: `Versicolor`",), "50 rows")
    stage(s, xs[2], y, w, key("card"), "filter-cog-outline", "`filter_expr`", (expr,), "34 rows")
    cx = xs[3]
    rrect(s, cx, y, w, 112, fill=white(t), stroke=edge(t, key("card")), r=12, width=1.6)
    type_badge(s, "card", cx + 22, y + 24, 22)
    s.text(cx + 42, y + 30, "Petals > 4 cm", size=15, anchor="start", weight="bold", colour=ink(t, key("card")))
    s.text(cx + 18, y + 80, "34", size=34, anchor="start", weight="bold", colour=ink(t, key("card")))
    s.text(cx + 70, y + 78, "(Count)", size=13, anchor="start", colour=t.dim)
    for x in xs[:3]:
        s.arrow(x + w + 4, y + 56, x + w + gap - 4, y + 56, colour=t.muted)

    # Lane 2: an interactive offers the values the expression leaves.
    y = 360
    lane_title(s, 324, "On an interactive", "`long-petal-variety-filter`: the options come from the table and the expression only")
    stage(s, xs[0], y, w, "collection", "table", "`iris_table`", ("every flower",), "150 rows")
    stage(s, xs[1], y, w, key("interactive"), "filter-cog-outline", "`filter_expr`", (expr,), "84 rows")
    ox = xs[2]
    rrect(s, ox, y, w, 112, fill=white(t), stroke=edge(t, key("interactive")), r=12, width=1.6)
    type_badge(s, "interactive", ox + 22, y + 24, 22)
    s.text(ox + 42, y + 30, "Variety options", size=15, anchor="start", weight="bold", colour=ink(t, key("interactive")))
    for i, (v, on) in enumerate((("Versicolor", True), ("Virginica", True), ("Setosa", False))):
        yy = y + 58 + i * 21
        if on:
            icon(s, "check", ox + 22, yy - 5, 15, solid(t, "good"))
            s.text(ox + 36, yy, v, size=14, anchor="start")
        else:
            s.cross(ox + 22, yy - 5, size=5, colour=solid(t, "bad"))
            s.text(ox + 36, yy, f"{v}, none over 4 cm", size=13, anchor="start", colour=t.dim)
    for x in xs[:2]:
        s.arrow(x + w + 4, y + 56, x + w + gap - 4, y + 56, colour=t.muted)

    # A pick takes the expression along.
    px = xs[3]
    s.arrow(ox + w + 4, y + 56, px - 4, y + 56, colour=solid(t, "you"))
    rrect(s, px, y, w, 112, fill=t.fill("you"), stroke=edge(t, "you"), r=12, width=1.6)
    icon(s, "filter-variant", px + 22, y + 24, 19, solid(t, "you"))
    s.text(px + 40, y + 30, "Pick Versicolor", size=15, anchor="start", weight="bold", colour=ink(t, "you"))
    for i, line in enumerate(("the filter carries the", "expression: the other", "components get 34 rows")):
        s.text(px + 14, y + 56 + i * 20, line, size=13, anchor="start")

    rrect(s, 30, 504, 900, 70, fill=t.fill("grey"), stroke=t.muted, r=12, width=1.2)
    icon(s, "filter-cog-outline", 56, 530, 18, t.dim)
    s.text(76, 535, "The expression scopes one component. It never removes rows from the collection,", size=14, anchor="start")
    s.text(76, 557, "and a component without one is not affected by another's, except through a pick.", size=14, anchor="start")
    return s


if __name__ == "__main__":
    write_themed(filter_expr_flow, OUT, "filter-expr-flow")
