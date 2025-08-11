# <span style="color: #F68B33;">:material-view-dashboard:</span> Using the Dashboard

## Right Sidebar Parameters

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/offcanvas.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/offcanvas.png" width="600">
    </a>
</div>

The right sidebar allows you to customize the appearance and behavior of the dashboard. Currently it includes the following options:

<!-- markdownlint-disable MD001 -->

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
