# <span style="color: #F68B33;">:material-view-dashboard:</span> Dashboard Creation

## <span style="color: #E53935;">:material-video:</span> Video example

<div style="max-width: 1200px; margin: 1rem auto 2rem auto;">
<div style="padding: 64.29% 0 0 0; position: relative">
  <iframe
    src="https://player.vimeo.com/video/1108747263?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
    frameborder="0"
    allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
    referrerpolicy="strict-origin-when-cross-origin"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
    title="depictio-long-demo-1754777542047"
  ></iframe>
  </div>
  <p style="text-align: center; margin-top: 0.5rem; font-style: italic; color: #666;">🎬 <strong>Depictio UI overview:</strong> Discover how to build a dashboard with Depictio</p>
</div>
<script src="https://player.vimeo.com/api/player.js"></script>

## <span style="color: #9966CC;">:material-plus-box:</span> Add a component to the dashboard

### <span style="color: #45B8AC;">:material-numeric-1-circle:</span> Step 1: Component Selection

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/step_one.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/step_one.png" width="600">
    </a>
</div>

1. Begin by clicking on the **"+ New Dashboard"** button to create a new dashboard.
2. In the **"Design your new dashboard component"** modal:
   - Choose from the available components (e.g., **Figure**, **Card**, **Interactive**, **Table**, **Text**).
3. Once you’ve chosen the component, click **Next Step**.

### <span style="color: #6495ED;">:material-numeric-2-circle:</span> Step 2: Data Selection

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/step_two.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/step_two.png" width="600">
    </a>
</div>

1. For each selected component, choose the corresponding **workflow** and **data collection** from the dropdowns.
2. Verify the **Data Collection Info**, such as **Workflow ID**, **Table type**, **MongoDB ID**, and **Data preview**.
3. Click **Next Step** to proceed.

### <span style="color: #F68B33;">:material-numeric-3-circle:</span> Step 3: Customize Your Component

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/design/figure_design.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/design/figure_design.png" width="600">
    </a>
</div>

1. **Customise your component**:

    - For **Figure** components, you can select the type of figure (e.g., scatter plot, histogram) and customize its appearance.
    - For **Interactive** components, you can set up interactive elements like sliders or dropdowns to allow users to filter or manipulate the data dynamically.
    - For **Card** components, you can display key metrics of your data.

  All options are dependent on the type of column in your data collection. For example, if you select a `numeric` column, you can choose to between a **Slider** or a **RangeSlider** for interactive components, and metrics like **Mean**, **Median**, or **Standard Deviation** for card components. If you select a `string` column, you can choose to display the **Select/Multiselect** or a **SegmentedControl** for interactive components, and metrics like **Count** or **Unique Count** for card components.

| Data Type | Interactive Options | Card Metrics |
|-----------|---------------------|--------------|
| Numeric   | Slider, RangeSlider | Mean, Median, Standard Deviation, Variance, ...|
| String    | Select, Multiselect, SegmentedControl | Count, Unique Count, Most Frequent (mode) |

2. **Set additional parameters**:

   - For **Figure** components, you can tweak visualization settings such as colors, axis labels, and bin sizes. Settings are categorised in the following way:
     - **Core parameters**: Define key parameters such as **X-axis** and **Y-axis** and **Color**, and assign the relevant data columns from your dataset.
     - **Styling & Layout**: Adjust the layout of the figure, including titles and axis labels, colors, hover data, and more.
     - **Figure type specific options**: Access additional options specific to the figure type, such as **scatter plot** or **histogram** settings.
     - **Advanced**: For advanced users, additional settings can be configured here like facetting, animation and more.

   - For **Interactive** components, you can set adjust sliders to have a given number of marks, use a linear or logarithmic scale.

3. **Finalize Customization**:
   - Review the component preview and ensure all settings are accurate.
   - Once complete, click **Next Step** to proceed to the final stage.

<!-- prettier-ignore -->
<!-- markdownlint-disable MD046 -->
!!! note
    **Figure component** as now a mode to create figure through code as well. This allows you to write custom code or port existing one to generate the figure, providing flexibility for advanced users. You can access this mode by clicking on the **"Code"** tab in the figure design interface. Switching from UI to code mode using existing UI settings will automatically generate the code for you, which you can then modify as needed.
<!-- markdownlint-enable MD046 -->

#### <span style="color: #8BC34A;">:material-palette:</span> Component design Examples:

##### <span style="color: #F68B33;">:material-chart-line:</span> Figure design - visualization selection

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/design/figure_design.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/design/figure_design.png" width="600">
    </a>
</div>

##### <span style="color: #6495ED;">:material-scatter-plot:</span> Figure design - scatter plot - UI mode

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/design/figure_design_scatter.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/design/figure_design_scatter.png" width="600">
    </a>
</div>

##### <span style="color: #7A5DC7;">:material-code-braces:</span> Figure design - scatter plot - code mode

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/design/figure_design_code.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/design/figure_design_code.png" width="600">
    </a>
</div>

##### <span style="color: #9966CC;">:material-tune-vertical:</span> Interactive design - RangeSlider example

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/design/interactive_design.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/design/interactive_design.png" width="600">
    </a>
</div>

##### <span style="color: #E6779F;">:material-card:</span> Card design - metrics selection

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/dashboard_creation/design/card_design.png" target="_blank">
        <img src="../../../images/guides/dashboard_creation/design/card_design.png" width="600">
    </a>
</div>
