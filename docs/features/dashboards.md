---
title: "Dashboard Features"
icon: material/view-dashboard-variant
description: "Guide to Depictio's dashboard modes, layouts, tabs, and organization features."
---

# :material-view-dashboard-variant: Dashboard Features

Depictio dashboards provide flexible, interactive data visualization with multiple modes, customizable layouts, and tabbed organization.

---

## :material-toggle-switch: Dashboard Modes

Depictio provides two distinct modes for working with dashboards:

### :material-eye: Viewer Mode

**URL**: `/dashboard/{id}`

Read-only mode for exploring data:

- :material-chart-line: View and interact with visualizations
- :material-filter: Use filter components to explore data
- :material-download: Export data from tables (v0.6.0+)
- :material-share-variant: Share dashboards with collaborators
- :material-lock: No accidental modifications

### :material-pencil: Editor Mode

**URL**: `/dashboard-edit/{id}`

Full editing capabilities:

- :material-plus-circle: Add, remove, and configure components
- :material-drag: Drag-and-drop component positioning
- :material-resize: Resize components
- :material-tab: Create and manage tabs
- :material-wizard-hat: Access the component builder stepper

---

## :material-view-grid: Three-Panel Layout

The dashboard interface uses a **three-panel layout** with a collapsible sidebar:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                                Header Bar                                │
├────────┬──────────────────┬──────────────────────────────────────────────┤
│        │   LEFT PANEL     │            RIGHT PANEL                       │
│ Side-  │   (Filters)      │          (Visualizations)                    │
│  bar   │ ┌──────────────┐ │                                              │
│        │ │ 2 active   ▾ │ │                                              │
│ Tab 1  │ └──────────────┘ │  ▾ Cohort                                    │
│ Tab 2  │ ▾ Sample         │  ┌─────────────┐  ┌─────────────┐            │
│ Tab 3  │ ┌──────────────┐ │  │    Card     │  │    Card     │            │
│        │ │ MultiSelect  │ │  └─────────────┘  └─────────────┘            │
│ [+]    │ └──────────────┘ │                                              │
│        │ ▸ Time  (folded) │  ▸ Quality control                  (folded) │
│ [=]    ├──────────────────┤                                              │
│        │ Map dock     (3) │  ▾ Detail                                    │
│        │ ┌──────────────┐ │  ┌─────────────┐  ┌─────────────┐            │
│        │ │  (map here)  │ │  │   Figure    │  │    Table    │            │
│        │ └──────────────┘ │  └─────────────┘  └─────────────┘            │
└────────┴──────────────────┴──────────────────────────────────────────────┘
```

Both panels can be organised into foldable **sections** <small>(v1.4.0+)</small>, and the
left panel collapses to a narrow rail. `2 active` is the active-filter summary; `(3)` on
the map dock is how many values that map is filtering on. A map can be lifted out of the
grid into that dock, or float above the canvas.

### :material-tab: Sidebar (Tab Navigation)

The collapsible **sidebar** on the far left provides:

- :material-view-dashboard: **Dashboard tabs** - Navigate between different views within the same dashboard
- :material-playlist-edit: **Tab management** - Add (+), rename, or delete tabs
- :material-menu: **Burger menu** (☰) - Collapse/expand the sidebar
- :material-cog: **Navigation controls** - Quick access to project settings

### :material-filter-variant: Left Panel (Filters)

The **left panel** contains interactive filter components:

- :material-tune: **Filter controls** that affect visualizations in the right panel
- :material-gesture-tap: **Automatic assignment** - Interactive components go here by default
- :material-grid: **Independent grid** - Drag and resize filters within this panel

Since **v1.4.0** the editor and the viewer draw the same panel, so the order you drag
filters into while editing is the order a viewer sees:

- :material-arrow-collapse-left: **Collapses to a rail** - 44px wide rather than nothing, so the active-filter count stays on screen. A dashboard showing filtered numbers must never look like it is showing everything.
- :material-arrow-split-vertical: **Resizable** - drag the panel's edge; the width is remembered per dashboard and the grid re-lays out to match.
- :material-format-list-bulleted: **Active-filter summary** - applied filters are listed above the controls as an aligned label/value list, each row carrying its own control's icon and accent, with a per-row clear. The list folds to a single line and its state persists per dashboard.
- :material-cellphone: **Drawer on narrow screens** - the panel becomes an overlay rather than stealing canvas width.

### :material-chart-box: Right Panel (Visualizations)

The **right panel** is the main canvas where visualization components are displayed:

- :material-drag: **Dragged** to reposition
- :material-resize: **Resized** by dragging edges/corners
- :material-cog-outline: **Configured** through component edit menus
- :material-link-variant: **Cross-panel filtering** - Responds to filters from the left panel
- :material-view-sequential: **Grouped into sections** (v1.4.0+) - `grid_sections` splits the canvas into named, foldable boxes; see [Sections](#sections) below

Available component types include:

| Component Type                              | Description                                    |
| ------------------------------------------- | ---------------------------------------------- |
| :material-chart-scatter-plot: **Figures**   | Interactive charts and visualizations          |
| :material-table: **Tables**                 | Data tables with filtering and pagination      |
| :material-card-text: **Cards**              | Summary statistics and KPIs                    |
| :material-tune: **Interactive Filters**     | Dropdowns, sliders, and other controls         |
| :material-format-header-1: **Text/Headers** | Section headers (H1, H2, H3)                   |
| :material-map-marker-multiple: **Maps**     | Geospatial scatter, density and choropleth maps |
| :material-microscope: **MultiQC**           | Quality control report visualizations          |
| :material-image: **Images**                 | Display grid of static images (PNG, JPEG, SVG) |

A map can also leave the grid entirely and become a dashboard-wide panel that follows the
viewer across every tab. See [Components](components.md#dashboard-wide-map-panel).

!!! note "Future Components"
    Additional component types may be added in future releases based on user needs and feedback (Network Graphs, JBrowse2).

### :material-view-sequential: Sections <small>(v1.4.0+)</small> { #sections }

Both panels can be grouped into named, foldable **sections**, each with its own icon,
colour, description and default state. `grid_sections` organises the main canvas and
`filter_sections` the left panel; a component joins one by naming it in its `section`
field. See [YAML Sync](yaml-sync.md#dashboard-sections) for the schema.

The two panels draw sections differently on purpose. The grid uses a box; the filter panel
uses a rail and an indent, because at panel width a box would spend its border and padding
on the very filters it is meant to organise.

Folding is not just visual: a folded section fetches nothing until you open it. It still
reports itself, though: a folded grid section of cards shows their numbers inline, and any
other section shows a component count. A folded filter section keeps the count of active
filters inside it.

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../images/guides/dashboards/sections_folded.png" target="_blank">
        <img src="../../images/guides/dashboards/sections_folded.png" width="600">
    </a>
</div>

Four folded grid sections: *Cohort* and *Morphometrics* hold cards, so their
numbers ride along on the header; *Composition* and *Raw Data* hold figures and
a table, so they report a component count instead.

<div style="border: 1px solid grey; width: 302px; padding: 1px;">
    <a href="../../images/guides/dashboards/filter_sections.png" target="_blank">
        <img src="../../images/guides/dashboards/filter_sections.png" width="300">
    </a>
</div>

The same dashboard's filter panel, drawn with a rail and an indent rather than a
box — *Cohort* and *Measurements* open, *Scoped views* folded.

Folding is remembered per viewer, in the browser, under
`grid-section-collapsed:<dashboard id>` — it is not part of the dashboard, so
collapsing a section you are reading never changes what anyone else sees.

---

## :material-tab-plus: Dashboard Tabs

Organize complex dashboards with **tabs** (v0.6.0+):

### :material-navigation: Tab Navigation

- :material-format-list-bulleted: Tabs are displayed **vertically** in the collapsible left navbar
- :material-cursor-default-click: Click a tab name to switch views
- :material-menu: The navbar can be **collapsed** using the burger menu icon
- :material-view-dashboard-outline: Each tab maintains its own component layout

### :material-star: Tab Features

- :material-tab-plus: **Multiple Tabs**: Create multiple views within a single dashboard
- :material-emoticon: **Custom Icons**: Material Design icons for visual identification
- :material-palette: **Custom Colors**: Match your organization's theme
- :material-view-grid-outline: **Independent Layouts**: Each tab has its own layout
- :material-cog-sync: **Shared Settings**: Theme and permissions apply across all tabs

### :material-creation: Creating a Tab

1. :material-plus-circle: Click **"+ New Tab"** in the navbar
2. :material-form-textbox: Enter a **tab name**
3. :material-emoticon-outline: Select an **icon** from the dropdown
4. :material-palette-outline: Choose an **icon color**
5. :material-check: Click **Create**

<!-- ### :material-tools: Tab Operations

| Operation                                      | Description                     |
| ---------------------------------------------- | ------------------------------- |
| :material-plus: **Add Tab**                    | Create a new empty tab          |
| :material-pencil: **Rename Tab**               | Change the tab's display name   |
| :material-delete: **Delete Tab**               | Remove a tab and its components |
| :material-reorder-horizontal: **Reorder Tabs** | Drag tabs to change their order | -->

---

## :material-content-save-outline: Auto-Save Behavior

Depictio automatically saves certain changes to prevent data loss. Understanding what is and isn't auto-saved helps you work more effectively.

### :material-content-save-check: What IS Auto-Saved

| Action                                        | Description                                                               |
| --------------------------------------------- | ------------------------------------------------------------------------- |
| :material-plus-circle: **Component Creation** | Adding new components to the dashboard                                    |
| :material-pencil: **Component Edition**       | Modifying component configuration (data source, visualization type, etc.) |
| :material-delete: **Component Deletion**      | Removing components from the dashboard                                    |
| :material-tab: **Tab Operations**             | Creating, renaming, or deleting tabs                                      |

### :material-content-save-alert: What is NOT Auto-Saved

| Action                                              | Description                                                 |
| --------------------------------------------------- | ----------------------------------------------------------- |
| :material-drag-variant: **Layout Positions**        | Dragging components to new positions requires manual save   |
| :material-filter-off: **Interactive Filter Values** | Filter selections are session-only and reset on page reload |
| :material-resize: **Component Resize**              | Resizing components requires manual save                    |

!!! tip "Saving Layout Changes"
After repositioning or resizing components, use the **Save Layout** button in the dashboard toolbar to persist your layout changes.

---

## :material-clipboard-check-outline: Ingestion Report & Health

Dashboards created from a [pipeline template](../pipeline-templates/README.md) carry an
**ingestion report** that compares the data collections the template *expected* against
what was actually found and aggregated during the CLI scan. It answers "did all the data
this dashboard needs actually land?" at a glance.

### :material-magnify: What the report shows

The report lists every expected data collection with a status:

| Status | Meaning |
| --- | --- |
| :material-check-circle:{ style="color: #2e7d32" } **Identified** | Included in this configuration and files were found and/or aggregated. |
| :material-alert-circle:{ style="color: #ef6c00" } **Found zero** | Included but nothing matched — no files identified and not aggregated. |
| :material-minus-circle:{ style="color: #757575" } **Gated out** | Intentionally excluded by a template conditional or missing-file prune (not a gap). |

Expand a row to see its files (or the Delta-table path once aggregated), and filter or
group rows by status.

### :material-heart-pulse: Health status & banner

The report rolls up into a single project **health** value:

- :material-check:{ style="color: #2e7d32" } **ok** — every required collection was identified.
- :material-alert:{ style="color: #ef6c00" } **partial** — some optional collections are missing.
- :material-close-octagon:{ style="color: #c62828" } **missing required** — a required collection is missing or empty.

When a template-derived dashboard is missing or only partially has a required collection,
a dismissible **health banner** appears above the dashboard. The full report is reachable
from the **settings drawer** of any template-derived project.

!!! note "Legacy projects"
    The report relies on the expected-data-collection manifest frozen at template
    resolution time. Projects created before this manifest existed fall back to the live
    project state, where intentionally gated-out collections cannot be distinguished.

---

## :material-share-variant: Sharing Dashboards

### :material-shield-account: Permissions

Dashboards inherit permissions from their project:

| Role                              | View                 | Edit                 | Delete               |
| --------------------------------- | -------------------- | -------------------- | -------------------- |
| :material-shield-crown: **Admin** | :material-check: Yes | :material-check: Yes | :material-check: Yes |
| :material-shield-edit: **Editor** | :material-check: Yes | :material-check: Yes | :material-close: No  |
| :material-shield-eye: **Viewer**  | :material-check: Yes | :material-close: No  | :material-close: No  |

### :material-link: Sharing URLs

- :material-eye: **Viewer URL**: `/dashboard/{id}` - Safe to share with collaborators
- :material-pencil: **Editor URL**: `/dashboard-edit/{id}` - Only for authorized editors

### :material-application-brackets: Embedding (Planned)

Future support for embedding dashboards in external sites via iframe.
