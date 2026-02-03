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
│                              Header Bar                                  │
├────────┬──────────────────┬──────────────────────────────────────────────┤
│        │                  │                                              │
│ Side-  │   LEFT PANEL     │            RIGHT PANEL                       │
│  bar   │   (Filters)      │          (Visualizations)                    │
│        │                  │                                              │
│ Tab 1  │ ┌──────────────┐ │  ┌─────────────┐  ┌─────────────┐            │
│ Tab 2  │ │  DatePicker  │ │  │   Figure    │  │   Figure    │            │
│ Tab 3  │ └──────────────┘ │  │  (Scatter)  │  │ (Histogram) │            │
│        │                  │  └─────────────┘  └─────────────┘            │
│ [+]    │ ┌──────────────┐ │                                              │
│        │ │ MultiSelect  │ │  ┌─────────────┐  ┌─────────────┐            │
│ [=]    │ └──────────────┘ │  │    Table    │  │    Card     │            │
│        │                  │  │             │  │  (Metric)   │            │
│        │ ┌──────────────┐ │  └─────────────┘  └─────────────┘            │
│        │ │ RangeSlider  │ │                                              │
│        │ └──────────────┘ │                                              │
│        │                  │                                              │
└────────┴──────────────────┴──────────────────────────────────────────────┘
```

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

### :material-chart-box: Right Panel (Visualizations)

The **right panel** is the main canvas where visualization components are displayed:

- :material-drag: **Dragged** to reposition
- :material-resize: **Resized** by dragging edges/corners
- :material-cog-outline: **Configured** through component edit menus
- :material-link-variant: **Cross-panel filtering** - Responds to filters from the left panel

Available component types include:

| Component Type                              | Description                                    |
| ------------------------------------------- | ---------------------------------------------- |
| :material-chart-scatter-plot: **Figures**   | Interactive charts and visualizations          |
| :material-table: **Tables**                 | Data tables with filtering and pagination      |
| :material-card-text: **Cards**              | Summary statistics and KPIs                    |
| :material-tune: **Interactive Filters**     | Dropdowns, sliders, and other controls         |
| :material-format-header-1: **Text/Headers** | Section headers (H1, H2, H3)                   |
| :material-microscope: **MultiQC**           | Quality control report visualizations          |
| :material-image: **Images**                 | Display grid of static images (PNG, JPEG, SVG) |

!!! note "Future Components"
    Additional component types may be added in future releases based on user needs and feedback (Geomap, Network Graphs, JBrowse2.).

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
