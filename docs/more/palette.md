# Color Palette

This page demonstrates the Depictio brand colors and how to use them in your applications.

## Brand Colors

The Depictio brand uses a consistent color palette to maintain visual identity across all platforms and applications.

<iframe src="../../assets/color_palette.html" width="100%" height="850px" frameborder="0"></iframe>

## Using the Colors in Your Code

### Python

```python
# Colors definition for Python applications
colors = {
    "purple": "#9966CC",
    "violet": "#7A5DC7",
    "blue": "#6495ED",
    "teal": "#45B8AC",
    "green": "#8BC34A",
    "yellow": "#F9CB40",
    "orange": "#F68B33",
    "pink": "#E6779F",
    "red": "#E53935",
    "black": "#000000",
}

# Color combinations
color_sequences = {
    "main": [colors["purple"], colors["blue"], colors["teal"], colors["green"],
            colors["yellow"], colors["orange"], colors["pink"]],
    "cool": [colors["purple"], colors["violet"], colors["blue"], colors["teal"]],
    "warm": [colors["yellow"], colors["orange"], colors["red"], colors["pink"]],
    "alert": [colors["green"], colors["yellow"], colors["orange"], colors["red"]],
}

# Example usage in Dash
import dash_mantine_components as dmc

button = dmc.Button(
    "Primary Action",
    styles={
        "root": {
            "backgroundColor": colors["blue"],
            "&:hover": {"backgroundColor": colors["blue"] + "cc"},
        }
    },
)
```

### CSS

```css
:root {
  --depictio-purple: #9966cc;
  --depictio-violet: #7a5dc7;
  --depictio-blue: #6495ed;
  --depictio-teal: #45b8ac;
  --depictio-green: #8bc34a;
  --depictio-yellow: #f9cb40;
  --depictio-orange: #f68b33;
  --depictio-pink: #e6779f;
  --depictio-red: #e53935;
  --depictio-black: #000000;
}

.btn-primary {
  background-color: var(--depictio-blue);
  color: white;
}

.btn-danger {
  background-color: var(--depictio-red);
  color: white;
}

.btn-success {
  background-color: var(--depictio-green);
  color: white;
}
```
