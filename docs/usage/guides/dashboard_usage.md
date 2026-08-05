# <span style="color: #F68B33;">:material-view-dashboard:</span> Using the Dashboard

## Dashboard Modes (v0.6.0+)

Depictio dashboards operate in two distinct modes, each optimized for its specific purpose.

### <span style="color: #45B8AC;">:material-eye:</span> Viewer Mode

**URL Pattern:** `/dashboard/{id}`

Viewer mode provides a **read-only** experience optimized for data exploration:

- **No editing controls** - Clean interface focused on data
- **Interactive filtering** - Use filter components to explore data
- **Data updates** - Visualizations respond to filter changes in real-time
- **Lightweight** - Read-only rendering path, with none of the editing machinery loaded

!!! tip "When to Use Viewer Mode"
    Use Viewer mode when exploring dashboards, presenting to stakeholders, or sharing dashboard links with colleagues who don't need editing access.

### <span style="color: #9966CC;">:material-pencil:</span> Editor Mode

**URL Pattern:** `/dashboard-edit/{id}`

Editor mode enables **full dashboard customization**:

- **Add components** - Create new figures, tables, cards, and filters
- **Edit components** - Modify existing component configurations
- **Drag and drop** - Reposition and resize components
- **Delete components** - Remove unwanted elements
- **Save changes** - Persist your layout and component settings
- **Tabs management** - Create and organize dashboard tabs

!!! info "Switching Between Modes"
    Click the **Edit** button in the dashboard header to switch from Viewer to Editor mode. Click **View** to return to read-only mode.

---

## Two-Panel Layout (v0.6.0+)

Dashboards use a two-panel layout to organize components:

| Panel | Location | Component Types |
|-------|----------|-----------------|
| **Left Panel** | ~20% width | Interactive filters (RangeSlider, MultiSelect, DatePicker) |
| **Right Panel** | ~80% width | Visualizations (Figure, Table, Card, Text) |

Components are automatically assigned to the appropriate panel based on their type when created.

### Working with the filter panel (v1.4.0+)

- **Collapse it** with the control at its edge. It shrinks to a narrow rail rather than disappearing, and the rail keeps showing how many filters are active, so a filtered dashboard never looks unfiltered.
- **Resize it** by dragging its edge. The width is remembered for that dashboard, and the grid re-lays out to match.
- **Fold a section** with its header. A folded section fetches nothing until you open it, and keeps a badge with the number of active filters inside it.
- **Read what is applied** from the summary above the controls: one aligned row per filter, each with its own control's icon and colour. Click a row's clear button to drop just that filter. The whole summary folds to a single line.

Sections in the main grid work the same way, and a folded section of cards still shows its numbers in the header. See [Sections](../../features/dashboards.md#sections).

### The map panel (v1.4.0+)

When a dashboard has a map authored as a dashboard-wide panel, it follows you across every tab rather than living in one. Use the header control to move it between floating, docked and hidden, and the panel header's menu to edit, duplicate or delete it.

- **Select on the map** by lassoing, box-selecting or clicking; every tab of the dashboard follows the selection.
- **Open the rows behind it** from the panel header or the tile chrome. The map's own columns come first, and ticking rows selects them on the map.
- Lasso, click and row-ticking all produce the same filter, so they replace one another instead of stacking.

---

## Right Sidebar Parameters

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/offcanvas.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/offcanvas.png" width="600">
    </a>
</div>

The right sidebar allows you to customize the appearance and behavior of the dashboard. Currently it includes the following options:


#### Switches

- **Edit Dashboard layout**: allow you to enable or disable the layout editing mode, which allows you to modify the size and position of the components, as well as show or hide the options of the components at the top of each component. When hidden, the options will not be displayed (except the reset button). See the [Component-wise options](#component-wise-options) section for more details. Interactions with the components are still enabled in this mode and you can still interact with the components.
- **Toggle interactivity**: enable or disable the interactivity of the components. When disabled, the components will not respond to user interactions.

#### Buttons

- **Remove all components**: remove all components from the dashboard.
- **Reset all filters**: reset all filters applied to the components.

## Component-wise options

When the **Display components options** switch is enabled, each component will display a set of options at the top of the component. These options allow you to perform the following actions:

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/component_options.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/component_options.png" width="600">
    </a>
</div>

- <span style="color: #888888;"><i class="mdi mdi-dots-grid"></i> Draggable</span>: Move and reposition components within the dashboard layout using drag handles.
- <span style="color: #e03131;"><i class="mdi mdi-trash-can-outline"></i> Delete</span>: Remove the component from the dashboard.
- <span style="color: #339af0;"><i class="mdi mdi-pen"></i> Edit</span>: Open a modal to modify the component settings.
- <span style="color: #868e96;"><i class="mdi mdi-content-copy"></i> Clone</span>: Create a copy of the component.
- <span style="color: #fd7e14;"><i class="bx bx-reset"></i> Reset filters</span>: Clear all filters applied to the component.
- <span style="color: #E6779F;"><i class="mdi mdi-format-align-left"></i> Align</span>: Choose text alignment (left, center, right) for text components.
- <span style="color: #15aabf;"><i class="mdi mdi-information-outline"></i> Component metadata</span>: View detailed metadata about the component, including its type, data source, and configuration settings.

---

## Table Component Features

### <span style="color: #45B8AC;">:material-download:</span> Data Export (v0.6.0+)

Table components include a **data export** feature that allows you to download the displayed data:

1. Click the **Export** button (download icon) in the table component header
2. The table data will be exported as a CSV file
3. The export respects current filters and sorting applied to the table

!!! note "Export Limits"
    - Tables with < 100,000 rows: Instant export
    - Tables with 100,000 - 1,000,000 rows: Export allowed with warning
    - Tables with > 1,000,000 rows: Export blocked (use CLI for large exports)

---

## How a Dashboard Loads (v1.3.0+)

A dashboard can hold dozens of panels, each needing its own request, so Depictio loads
them as you reach them rather than all at once.

### <span style="color: #45B8AC;">:material-progress-clock:</span> While the page opens

- **The Depictio logo animates in the centre of the page** while the dashboard itself is
  being fetched. No panels are known yet, so there is nothing to count.
- **Panels load when they scroll into view.** A panel below the fold shows a shimmering
  placeholder and costs nothing until you scroll near it, so opening a large dashboard
  stays responsive instead of waiting on every panel first.
- **A progress ring and a count** (for example `6/8`) sit beside the dashboard title, then
  disappear once everything on screen is ready. Hover it for a breakdown: how many are
  still loading, how many failed, and how many are further down the page.

!!! tip "Why the count can go backwards"
    The count covers what is **on screen**, not the whole dashboard, so it always
    completes. Scrolling brings more panels in and the count grows to include them, so a
    number that briefly drops is work which has just started, not a problem.

### <span style="color: #9966CC;">:material-database-arrow-down:</span> Reduced views and the Load-all button

Large data collections are not sent to the browser whole. Where a panel is showing a
reduced view, it says so and offers a way out:

[![A volcano panel with the badge 9,900 / 12,011,000 pts beside its title and the Load-all icon revealed in the hover action cluster](../../images/react/load_all_light.webp#only-light)](../../images/react/load_all_light.webp){target=_blank}

[![A volcano panel with the badge 9,900 / 12,011,000 pts beside its title and the Load-all icon revealed in the hover action cluster](../../images/react/load_all_dark.webp#only-dark)](../../images/react/load_all_dark.webp){target=_blank}

*Hover a panel to reveal its action cluster. **Load all** is the bottom icon, and the badge
beside the title says how much of the collection you are currently seeing.*

- **Figures** show a badge such as `9,900 / 12,011,000 pts`. Hover the panel and click the
  **Load all** icon (:material-database-arrow-down:) in the action cluster to fetch every
  point; the badge switches to `(all)` and the button toggles back to the reduced view.
  Loading everything can be slow on a very large collection.
- **Tables** page rows on demand. On tables past roughly a million rows, **sorting is
  turned off**: the chevron disappears from the column headers rather than offering a
  sort that would silently return unsorted rows.
- **Advanced visualisations** that compute their values from the rows they receive (stacked
  taxonomy, DA barplot, enrichment, oncoplot, …) are normally sent the whole collection. If
  it is too large for that, they carry an orange **estimated** badge, meaning the values on
  screen are derived from a sample rather than being exact totals. The lollipop plot shows
  the same badge whenever its rows were sampled, since its per-gene counts are an aggregate.

See [Performance & Scaling](../../features/performance.md) for the thresholds behind these
behaviours and how to change them.

---

## Interactivity

#### Interactive Actions

There are currently two types of interactive actions available in the dashboard:

- Through the **interactive** components (e.g., RangeSlider, MultiSelect, etc.).
- Through the **graph** components (only Scatter plots are handled yet).
  - **Click mode**: When you click on a point in the scatter plot, the other components will be updated according to the data point clicked.
  - **Selection mode**: When you select a region in the scatter plot (using the **_"Box select"_** option), the other components will be updated according to the data points in the selected region.

#### Reset Filters

- **Reset all filters** You can reset all filters applied to the components by clicking the **Reset all filters** button in the right sidebar. This will clear all filters applied to the components and reset them to their default state.
- **Reset interactive component/scatter plot filter** You can reset the filters applied to the graph components by clicking the orange <span style="color: #fd7e14;"><i class="bx bx-reset"></i> Reset</span> button in the component options at the top of the box. This will clear the filters applied to the graph component and reset it to its default state.
- **Clear one filter from the summary** (v1.4.0+) Each row of the filter panel's active-filter summary has its own clear button, so you can drop a single filter without touching the rest.

!!! note "Where the reset icon stays visible (v1.4.0+)"
    On figures, tables and maps the reset icon stays pinned while a selection is active, since a selection there is easy to miss. On an interactive control it appears on hover, so that it cannot sit on top of the select's chevron or the slider track.

## Saving the Dashboard

1. Once your dashboard is ready, click the **Save** icon (green button at the top right).
2. A **modal** will appear confirming that your dashboard has been saved (e.g., "Your amazing dashboard was successfully saved!").
3. Click **Close** to dismiss the modal.
4. Your dashboard will now appear with a thumbnail under the **Recently Viewed** section on the landing page.

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/save.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/save.png" width="600">
    </a>
</div>

## Example Dashboard result

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/dashboard_example.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/dashboard_example.png" width="600">
    </a>
</div>
