# Color Palette

This page demonstrates the Depictio brand colors and how to use them in your applications.

## Brand Colors

The Depictio brand uses a consistent color palette to maintain visual identity across all platforms and applications.

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:14px;margin:1.4rem 0;">
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#9966CC;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Purple</strong><br><code>#9966CC</code></div>
  </div>
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#7A5DC7;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Violet</strong><br><code>#7A5DC7</code></div>
  </div>
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#6495ED;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Blue</strong><br><code>#6495ED</code></div>
  </div>
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#45B8AC;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Teal</strong><br><code>#45B8AC</code></div>
  </div>
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#8BC34A;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Green</strong><br><code>#8BC34A</code></div>
  </div>
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#F9CB40;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Yellow</strong><br><code>#F9CB40</code></div>
  </div>
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#F68B33;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Orange</strong><br><code>#F68B33</code></div>
  </div>
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#E6779F;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Pink</strong><br><code>#E6779F</code></div>
  </div>
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#E53935;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Red</strong><br><code>#E53935</code></div>
  </div>
  <div style="border-radius:10px;overflow:hidden;border:1px solid var(--md-default-fg-color--lightest);">
    <div style="background:#000000;height:80px;"></div>
    <div style="padding:8px 10px;line-height:1.4;"><strong>Black</strong><br><code>#000000</code></div>
  </div>
</div>

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

# Example usage with Mantine
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
