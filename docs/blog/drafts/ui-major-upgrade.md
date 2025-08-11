---
date: 2025-01-20
draft: true
authors:
  - thomas-weber
categories:
  - Development
  - UI/UX
  - Technical
tags:
  - upgrade
  - dmc
  - grid-layout
  - user-interface
  - modernization

---

# 🚀 UI Major Upgrade: Modernizing Depictio's Interface

**How we transformed Depictio's UI with DMC 2.1 upgrade and dynamic grid layout migration - the technical story behind a major UX overhaul.**

<!-- more -->

<div style="max-width: 1200px; margin: 1rem auto 2rem auto;">
  <div style="padding: 64.29% 0 0 0; position: relative">
    <iframe
      src="https://player.vimeo.com/video/placeholder?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479&amp;autoplay=1&amp;loop=1"
      frameborder="0"
      allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
      referrerpolicy="strict-origin-when-cross-origin"
      style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
      title="depictio-ui-upgrade-video"
    ></iframe>
  </div>
</div>
<script src="https://player.vimeo.com/api/player.js"></script>

## 🎯 Why This Upgrade Was Critical

Building modern dashboards requires **modern UI foundations**. Our interface was struggling with two major limitations:

1. **🔧 Outdated Component Library**: DMC 0.12 was limiting our design possibilities
2. **📐 Grid Layout Issues**: dash-draggable couldn't handle proper vertical component growth

These constraints were holding back the **intuitive, responsive experience** users expect from a modern data platform.

## 🧩 Challenge #1: DMC Upgrade (0.12 → 2.1)

### The Problem
Dash Mantine Components (DMC) 0.12 was **severely limiting** our UI capabilities:
- Missing modern components (advanced inputs, layouts)
- Inconsistent theming system
- Limited styling flexibility  
- Poor responsive design patterns

### The Solution: Major Version Jump
Upgrading from DMC 0.12 to 2.1 was **complex but necessary**:

```python
# Before (DMC 0.12) - Limited component options
dmc.Button(
    children="Submit",
    variant="filled",  # Limited variants
    color="blue"       # Basic color system
)

# After (DMC 2.1) - Rich component ecosystem  
dmc.Button(
    children="Submit",
    variant="gradient",         # New gradient variants
    gradient={"from": "blue", "to": "purple"},  
    leftIcon=DashIconify(icon="mdi:upload"),
    loading=loading_state,      # Built-in loading states
    fullWidth=True             # Better responsive options
)
```

### Impact: Modern Design System
The upgrade enabled:
- **🎨 Advanced theming** with CSS custom properties
- **📱 Better responsive components** 
- **⚡ Improved performance** and bundle size
- **🔧 New component types** (advanced inputs, better layouts)

## 📐 Challenge #2: Grid Layout Migration

### The Problem: dash-draggable Limitations
Our dashboard grid system had **critical vertical growth issues**:

```python
# dash-draggable - Fixed height components
ResponsiveGridLayout(
    children=components,
    layouts={"lg": [{"i": "0", "x": 0, "y": 0, "w": 6, "h": 4}]},
    # Components couldn't grow vertically properly
)
```

Components were **trapped in fixed heights**, creating poor user experiences when:
- Plots needed more vertical space
- Tables had many rows
- Text components required different sizes

### The Solution: dash-dynamic-grid-layout

We migrated to `dash-dynamic-grid-layout` with **smart vertical growth**:

```python
# dash-dynamic-grid-layout - Dynamic vertical growth
dgl.DashGridLayout(
    items=wrapped_components,     # New component wrapping system
    itemLayout=single_layout,     # Simplified layout structure
    rowHeight=10,                # Flexible 10px units
    enableVerticalGrowth=True,   # Key feature!
    showRemoveButton=edit_mode,  # Connected to edit mode
    showResizeHandles=edit_mode  # Contextual UI controls
)
```

### Technical Implementation: Vertical Growth System

The migration required **sophisticated CSS injection** for proper flexbox behavior:

```javascript
// Dynamic CSS injection for component flexibility
const style = document.createElement('style');
style.textContent = `
    .react-grid-item {
        display: flex !important;
        flex-direction: column !important;
    }
    .react-grid-item > div {
        height: 100% !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
    }
    .js-plotly-plot {
        flex-grow: 1 !important;
        height: 100% !important;
    }
`;
```

### Component Wrapping System

Every component now gets **intelligently wrapped** for proper grid behavior:

```python
def wrap_component_in_draggable_wrapper(component, component_id, component_type="component"):
    """
    Wrap a component in DraggableWrapper for dynamic grid layout.
    """
    wrapped_content = html.Div(
        component,
        style={
            "height": "100%",
            "width": "100%", 
            "display": "flex",
            "flex-direction": "column",
            "box-sizing": "border-box",
        },
    )
    
    return dgl.DraggableWrapper(
        wrapped_content,
        id=component_id,
        handleText=f"Drag {component_type.title()}",
    )
```

## 🎨 UX Revolution: "Transparent" Edit Mode

### Before: Confusing Edit Interface
- Edit buttons always visible (cluttered interface)
- No clear distinction between view/edit modes
- Users confused about when they could modify components

### After: Contextual, Transparent Design

**🔄 Edit Mode Toggle**: Clean switch in the header offcanvas

```python
# Connected edit mode to grid system
@app.callback(
    [
        Output("draggable-wrapper", "showRemoveButton"),
        Output("draggable-wrapper", "showResizeHandles")
    ],
    Input("edit-mode-switch", "checked")
)
def toggle_edit_mode(edit_enabled):
    return edit_enabled, edit_enabled
```

**🎯 Contextual Component Buttons**: 
- **Reset button** (appears on hover for filtered components)
- **Justify text** (for text components only)
- **Edit button** (when component supports configuration)
- **Remove button** (only in edit mode)

## ⚡ Performance & Technical Benefits  

### Grid Layout Performance
- **🏃 Faster rendering**: More efficient React Grid Layout algorithm
- **📏 Better positioning**: Improved component placement logic
- **🔄 Smoother interactions**: Optimized drag & resize operations

### Component System Improvements
- **🎯 Sequential IDs**: Clean (0, 1, 2, 3...) component identification
- **🔗 Backward compatibility**: Existing layouts still work
- **🛠️ Type safety**: All code passes `ruff` and `tycheck`

### Dynamic Graph Resizing
Real-time graph adaptation to container changes:

```javascript
// Clientside callback for dynamic graph resizing  
function(layout) {
    if (layout && layout.length > 0) {
        setTimeout(function() {
            layout.forEach(function(layoutItem) {
                const gridItem = document.querySelector('[data-grid="' + layoutItem.i + '"]');
                if (gridItem) {
                    const newHeight = Math.max(layoutItem.h * 10 - 20, 150);
                    const graphElements = gridItem.querySelectorAll('.js-plotly-plot');
                    graphElements.forEach(function(graphElement) {
                        if (window.Plotly) {
                            window.Plotly.relayout(graphElement, {
                                height: newHeight - 40,
                                autosize: true
                            });
                        }
                    });
                }
            });
        }, 100);
    }
}
```

## 🎯 Results: Transformed User Experience

### Before vs After

| Aspect | Before (DMC 0.12 + dash-draggable) | After (DMC 2.1 + dash-dynamic-grid-layout) |
|--------|-------------------------------------|---------------------------------------------|
| **Vertical Growth** | ❌ Fixed component heights | ✅ Dynamic vertical expansion |
| **Edit Mode** | ❌ Always-visible clutter | ✅ Clean, contextual controls |
| **Components** | ❌ Limited design options | ✅ Modern component library |
| **Responsiveness** | ❌ Poor mobile experience | ✅ Fully responsive design |
| **Performance** | ❌ Slower interactions | ✅ Smooth, optimized UX |

### User Feedback Impact
- **📈 Improved usability**: Users can resize components naturally
- **🎨 Modern aesthetics**: Professional, clean interface
- **⚡ Better performance**: Faster dashboard interactions  
- **📱 Mobile ready**: Responsive design across devices

## 🔧 Technical Migration Process

### 1. **Component Library Upgrade**
```bash
# Package updates
pip install dash-mantine-components==2.1.0
pip uninstall dash-draggable  
pip install dash-dynamic-grid-layout
```

### 2. **Code Refactoring**
- **Updated imports** across 15+ files
- **Converted layout structures** from responsive to single layout
- **Added CSS injection** for vertical growth
- **Implemented component wrapping** system

### 3. **Testing & Validation**
- **✅ All existing functionality preserved**
- **✅ Backward compatibility maintained**
- **✅ Performance improvements verified**
- **✅ Cross-browser testing completed**

## 🗺️ What's Next?

This foundation enables exciting future features:
- **🧩 Advanced component templates**
- **📱 Mobile-first dashboard editing**
- **🎨 Custom theme builder**
- **⚡ Real-time collaborative editing**

## 🔗 Technical Resources

- **Grid Migration Details**: Check our [technical documentation](../../development/grid-migration.md)
- **DMC 2.1 Guide**: [Component upgrade patterns](../../development/dmc-upgrade.md)
- **Source Code**: [Grid layout implementation](https://github.com/depictio/depictio/tree/main/depictio/dash/layouts)

---

*This upgrade represents months of careful engineering to modernize Depictio's foundation while maintaining all existing functionality. Every line of code was refactored with backward compatibility in mind.*

---

*Thomas Weber*  
*January 2025*