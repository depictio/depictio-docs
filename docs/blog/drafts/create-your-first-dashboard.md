---
date: 2025-01-16
draft: true
authors:
  - thomas-weber
categories:
  - Tutorials
  - Features
tags:
  - tutorial
  - dashboard
  - interactive-components
  - getting-started
  - beginner

---

# 🎨 Create Your First Dashboard: From Data to Interactive Insights

**Step-by-step guide to building your first interactive dashboard in Depictio - no coding required!**

<!-- more -->

<div style="max-width: 1200px; margin: 1rem auto 2rem auto;">
  <div style="padding: 64.29% 0 0 0; position: relative">
    <iframe
      src="https://player.vimeo.com/video/placeholder?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479&amp;autoplay=1&amp;loop=1"
      frameborder="0"
      allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
      referrerpolicy="strict-origin-when-cross-origin"
      style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
      title="depictio-first-dashboard-tutorial"
    ></iframe>
  </div>
</div>
<script src="https://player.vimeo.com/api/player.js"></script>

## 🎯 What You'll Build

By the end of this tutorial, you'll have created a **fully interactive dashboard** with:

- **🎛️ Interactive Controls** - Sliders and dropdowns that filter your data
- **📊 Dynamic Charts** - Scatter plots and bar charts that update in real-time
- **📋 Data Tables** - Sortable, filterable tables with server-side pagination
- **🎯 Metrics Cards** - Key statistics that change with your filters

**Time to complete**: 15-20 minutes
**Difficulty**: Beginner
**Requirements**: Sample CSV file (we'll provide one)

## 🚀 Step 1: Prepare Your Data

### Option A: Use Our Sample Data

Download our sample Palmer Penguins dataset:

```bash
# Download sample data
curl -o penguins.csv https://raw.githubusercontent.com/depictio/sample-data/main/penguins.csv
```

### Option B: Use Your Own Data

Your CSV file should have:
- **Column headers** in the first row
- **Mixed data types** (text, numbers, categories)
- **At least 50 rows** for interesting interactions

**Example structure:**
```csv
species,island,bill_length_mm,bill_depth_mm,flipper_length_mm,body_mass_g,sex,year
Adelie,Torgersen,39.1,18.7,181,3750,male,2007
Adelie,Torgersen,39.5,17.4,186,3800,female,2007
Chinstrap,Dream,46.5,17.9,192,3500,female,2007
...
```

## 📁 Step 2: Create Your Project

### Using the Web Interface

1. **Visit Depictio** → Go to [demo.depictio.embl.org](https://demo.depictio.embl.org)
2. **Create Account** → Click "Sign Up" (or use demo mode)
3. **New Project** → Click "+ Create Project"
4. **Project Settings**:
   - **Name**: "My First Dashboard"
   - **Type**: Basic
   - **Description**: "Learning interactive dashboards"

### Using the CLI

```bash
# Install the Depictio CLI
pip install depictio

# Login and create project
depictio auth login
depictio project create \
    --name "My First Dashboard" \
    --type basic \
    --description "Learning interactive dashboards"
```

## 📤 Step 3: Upload Your Data

### Web Upload

1. **Navigate to Project** → Click on "My First Dashboard"
2. **Add Data Collection**:
   - Click "Add Data Collection"
   - **Name**: "Penguins Dataset"
   - **Upload File**: Select your `penguins.csv`
   - Click "Upload"

### CLI Upload

```bash
# Upload data collection
depictio data upload \
    --file penguins.csv \
    --collection-name "Penguins Dataset" \
    --project-name "My First Dashboard"
```

**✅ Success indicator**: You should see "Data collection created successfully" and your data preview.

## 🎨 Step 4: Create Your Dashboard

### Access Dashboard Builder

1. **Go to Dashboards** → Click "Dashboards" tab
2. **Create Dashboard** → Click "+ New Dashboard"
3. **Dashboard Settings**:
   - **Name**: "Penguins Explorer"
   - **Description**: "Interactive penguin species analysis"

You'll see the **dashboard canvas** - an empty grid where you'll add components.

## 🎛️ Step 5: Add Interactive Controls

Interactive components are **global filters** that affect all other dashboard components.

### Add Species Filter

1. **Add Component** → Click "+" button → "Interactive Component"
2. **Component Configuration**:
   - **Data Collection**: "Penguins Dataset"
   - **Column**: "species"
   - **Component Type**: "Dropdown"
   - **Label**: "Filter by Species"
3. **Save** → Click "Save Component"

### Add Body Mass Slider

1. **Add Component** → Click "+" → "Interactive Component"
2. **Configuration**:
   - **Data Collection**: "Penguins Dataset"
   - **Column**: "body_mass_g"
   - **Component Type**: "Range Slider"
   - **Label**: "Body Mass Range (g)"
3. **Save** → Click "Save Component"

### Add Island Selection

1. **Add Component** → Click "+" → "Interactive Component"
2. **Configuration**:
   - **Data Collection**: "Penguins Dataset"
   - **Column**: "island"
   - **Component Type**: "Segmented Control"
   - **Label**: "Select Island"
3. **Save** → Click "Save Component"

**🎯 Result**: You now have three interactive controls that will filter your entire dashboard!

## 📊 Step 6: Add Visual Components

### Create a Scatter Plot

1. **Add Component** → Click "+" → "Figure Component"
2. **Figure Configuration**:
   - **Chart Type**: "Scatter Plot"
   - **Data Collection**: "Penguins Dataset"
   - **X-axis**: "bill_length_mm"
   - **Y-axis**: "bill_depth_mm"
   - **Color**: "species"
   - **Size**: "body_mass_g"
   - **Title**: "Bill Dimensions by Species"
3. **Save** → Click "Save Component"

### Add a Bar Chart

1. **Add Component** → Click "+" → "Figure Component"
2. **Configuration**:
   - **Chart Type**: "Bar Chart"
   - **Data Collection**: "Penguins Dataset"
   - **X-axis**: "island"
   - **Y-axis**: "count" (aggregated)
   - **Color**: "species"
   - **Title**: "Penguin Count by Island"
3. **Save** → Click "Save Component"

### Create a Metrics Card

1. **Add Component** → Click "+" → "Card Component"
2. **Configuration**:
   - **Data Collection**: "Penguins Dataset"
   - **Metric**: "body_mass_g"
   - **Aggregation**: "Average"
   - **Title**: "Average Body Mass"
   - **Format**: "Number with units (g)"
3. **Save** → Click "Save Component"

### Add a Data Table

1. **Add Component** → Click "+" → "Table Component"
2. **Configuration**:
   - **Data Collection**: "Penguins Dataset"
   - **Columns**: Select all columns
   - **Title**: "Penguin Data Explorer"
   - **Enable Sorting**: ✅
   - **Enable Filtering**: ✅
3. **Save** → Click "Save Component"

## ✨ Step 7: Test the Interactivity

Now comes the magic! **All components respond to interactive filters simultaneously.**

### Test Species Filter
1. **Use the species dropdown** → Select "Adelie"
2. **Watch everything update**:
   - Scatter plot shows only Adelie penguins
   - Bar chart adjusts counts
   - Average body mass recalculates
   - Table filters to Adelie rows only

### Test Body Mass Slider
1. **Adjust the mass range** → Drag to 3000-4000g
2. **See real-time updates**:
   - All charts filter to penguins in that mass range
   - Metrics update instantly
   - Table shows matching rows

### Test Multi-Filter Combinations
1. **Apply multiple filters**:
   - Species: "Chinstrap"
   - Body Mass: 3500-4500g
   - Island: "Dream"
2. **Everything synchronizes** to show only Chinstrap penguins from Dream island in the specified mass range!

## 🎨 Step 8: Customize Your Layout

### Arrange Components

1. **Enable Edit Mode** → Toggle "Edit Mode" in the header
2. **Drag Components** → Click and drag to rearrange
3. **Resize Components** → Drag corners to resize
4. **Fine-tune Layout** → Position components for optimal viewing

**Recommended Layout:**
```
[Species Filter] [Body Mass Slider] [Island Selection]
[   Scatter Plot   ] [  Bar Chart  ] [ Metrics Card ]
[          Data Table (full width)          ]
```

### Advanced Customization

**Chart Styling:**
- **Colors**: Customize color schemes
- **Axes**: Adjust labels and ranges
- **Legends**: Position and format legends
- **Annotations**: Add trend lines or highlights

**Component Options:**
- **Responsive Sizing**: Components adapt to screen size
- **Conditional Formatting**: Highlight important values
- **Export Options**: Download charts as images

## 🔄 Step 9: Advanced Interactions

### Scatter Plot Selections

1. **Box Selection** → Click and drag on scatter plot to select points
2. **Watch Updates** → All other components filter to selected points
3. **Reset Selection** → Click "Reset" button to clear

### Table Row Selection (Coming Soon!)

```python
# Future feature: Table row selection
selected_rows = table_component.get_selected_rows()
dashboard.apply_selection_filter(selected_rows)
```

### Cross-Filtering

Your dashboard now supports **cross-filtering**: selections in one component automatically filter all others, creating a cohesive analytical experience.

## 💾 Step 10: Save and Share

### Save Your Dashboard

1. **Save Progress** → Click "Save Dashboard"
2. **Set Permissions**:
   - **Private**: Only you can access
   - **Public**: Anyone with link can view
   - **Team**: Share with specific users

### Share Options

**Public Link:**
```bash
# Your shareable dashboard URL
https://demo.depictio.embl.org/dashboards/your-dashboard-id
```

**Embed Code:**
```html
<!-- Embed in website or documentation -->
<iframe src="https://demo.depictio.embl.org/embed/your-dashboard-id"
        width="100%" height="600px" frameborder="0">
</iframe>
```

## 🎯 What You've Accomplished

**Congratulations!** 🎉 You've created a fully interactive dashboard with:

✅ **Real-time filtering** across all components
✅ **Professional visualizations** (scatter plots, bar charts)
✅ **Interactive controls** (dropdowns, sliders, segmented controls)
✅ **Data exploration tools** (sortable tables, metrics)
✅ **Responsive design** that works on any device
✅ **Shareable results** with public links

## 🚀 Next Level: Advanced Features

### Add More Data Collections

```bash
# Upload additional datasets to the same project
depictio data upload \
    --file environmental_data.csv \
    --collection-name "Environmental Conditions"

depictio data upload \
    --file genetic_markers.parquet \
    --collection-name "Genetic Analysis"
```

### Cross-Collection Joins

1. **Join Data** → Use common columns to combine datasets
2. **Complex Analysis** → Correlate penguin traits with environmental factors
3. **Advanced Visualizations** → Multi-dimensional analysis

### Custom Component Types

- **📈 Time Series** → Trend analysis over time
- **🗺️ Geographic Maps** → Spatial data visualization
- **🎯 KPI Dashboards** → Executive summary views
- **📊 Statistical Plots** → Box plots, violin plots, regression lines

## 🛠️ Troubleshooting

### Common Issues

**❌ Components not updating together**
- ✅ Ensure all components use the same data collection
- ✅ Check that interactive components target the right columns

**❌ Slow performance**
- ✅ Limit initial data display (use sampling for large datasets)
- ✅ Use aggregated views for very large tables

**❌ Charts not displaying properly**
- ✅ Verify column data types (numeric vs categorical)
- ✅ Check for missing values in key columns

**❌ Upload errors**
- ✅ Ensure CSV has headers in the first row
- ✅ Check file size limits (contact admin for large files)

### Getting Help

**📚 Documentation**: [docs.depictio.embl.org](https://docs.depictio.embl.org)
**💬 Community**: [GitHub Discussions](https://github.com/depictio/depictio/discussions)
**🐛 Bug Reports**: [GitHub Issues](https://github.com/depictio/depictio/issues)
**📧 Direct Support**: Open an issue for personalized help

## 🗺️ What's Next?

### Explore More Tutorials

- **🔬 [Advanced Project Types](./depictio-basics.md)** - Bioinformatics workflow integration
- **⚡ [Performance Optimization](./interactive-metadata-system.md)** - Handle massive datasets
- **🎨 [UI Customization](./ui-major-upgrade.md)** - Design beautiful dashboards
- **📊 [Table Mastery](./infinite-scrolling-tables.md)** - Advanced table features

### Join the Community

- **⭐ Star the project** on GitHub
- **🤝 Contribute** features or documentation
- **💬 Share your dashboards** in the community
- **📢 Provide feedback** to shape future development

---

*You've just created your first interactive dashboard! This is the beginning of your journey into powerful, code-free data analysis with Depictio. Every component, every interaction, every insight is now at your fingertips.*

---

*Thomas Weber*
*January 2025*
