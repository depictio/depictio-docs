# Animated Triangular Logo

The triangular SVG from the original Depictio progressive loading script, now with dynamic animations!

## Interactive Triangular SVG

<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px; margin: 20px 0;">
    <h3>Click the logo to trigger enhanced animation!</h3>
    <div id="inline-svg-container" style="display: inline-block;">
        <!-- SVG will be loaded here -->
    </div>

    <div style="margin-top: 20px;">
        <button onclick="triggerTriangularAnimation()" style="padding: 10px 20px; background: #f4b136; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">Trigger Animation</button>
        <button onclick="debugTriangularShapes()" style="padding: 10px 20px; background: #6279f0; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px;">Debug Shapes</button>
    </div>

    <p style="margin-top: 15px; font-size: 14px; color: #666;">
        💡 Hover over the logo to see the sequential triangular animation!
    </p>
</div>

## Triangular Animation Features

The animated triangular logo includes the exact effects from the original Python implementation:

### 1. Sequential Triangle Pulsing
- **7 Triangular Shapes**: Each triangle (`shape-1` through `shape-7`) animates individually
- **Sequential Timing**: 0.1s delays between each triangle (0s, 0.1s, 0.2s, 0.3s, 0.4s, 0.5s, 0.6s)
- **Pulse Effect**: Each triangle scales from 100% to 120% and back with brightness changes
- **Transform Origin**: Each shape uses `center` origin and `fill-box` for proper scaling

### 2. Color-Coded Triangles
- **Shape 1**: `#f1c547` (Golden yellow)
- **Shape 2**: `#c064d3` (Purple/magenta)
- **Shape 3**: `#58b3cb` (Light blue)
- **Shape 4**: `#6279f0` (Blue)
- **Shape 5**: `#ee9644` (Orange)
- **Shape 6**: `#7d5dec` (Purple)
- **Shape 7**: `#a1d44d` (Green)

### 3. Interactive Features
- **Click Activation**: Click to trigger the sequential animation
- **Automatic Cycling**: Animation triggers every 10 seconds
- **Debug Console**: Console logs show triangle detection and animation status

## Shape Animation Timing

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0;">
    <div style="text-align: center; padding: 15px; border: 2px solid #f1c547; border-radius: 8px;">
        <h4 style="color: #f1c547;">Triangle 1</h4>
        <p><strong>Delay:</strong> 0.0s</p>
        <p><strong>Color:</strong> Golden Yellow</p>
    </div>

    <div style="text-align: center; padding: 15px; border: 2px solid #c064d3; border-radius: 8px;">
        <h4 style="color: #c064d3;">Triangle 2</h4>
        <p><strong>Delay:</strong> 0.1s</p>
        <p><strong>Color:</strong> Purple/Magenta</p>
    </div>

    <div style="text-align: center; padding: 15px; border: 2px solid #58b3cb; border-radius: 8px;">
        <h4 style="color: #58b3cb;">Triangle 3</h4>
        <p><strong>Delay:</strong> 0.2s</p>
        <p><strong>Color:</strong> Light Blue</p>
    </div>

    <div style="text-align: center; padding: 15px; border: 2px solid #6279f0; border-radius: 8px;">
        <h4 style="color: #6279f0;">Triangle 4</h4>
        <p><strong>Delay:</strong> 0.3s</p>
        <p><strong>Color:</strong> Blue</p>
    </div>

    <div style="text-align: center; padding: 15px; border: 2px solid #ee9644; border-radius: 8px;">
        <h4 style="color: #ee9644;">Triangle 5</h4>
        <p><strong>Delay:</strong> 0.4s</p>
        <p><strong>Color:</strong> Orange</p>
    </div>

    <div style="text-align: center; padding: 15px; border: 2px solid #7d5dec; border-radius: 8px;">
        <h4 style="color: #7d5dec;">Triangle 6</h4>
        <p><strong>Delay:</strong> 0.5s</p>
        <p><strong>Color:</strong> Purple</p>
    </div>

    <div style="text-align: center; padding: 15px; border: 2px solid #a1d44d; border-radius: 8px;">
        <h4 style="color: #a1d44d;">Triangle 7</h4>
        <p><strong>Delay:</strong> 0.6s</p>
        <p><strong>Color:</strong> Green</p>
    </div>
</div>

## Technical Implementation

The animation system consists of:

1. **CSS Keyframes**: Define the core animation patterns
2. **JavaScript Enhancement**: Adds interactivity and advanced effects
3. **Sequential Timing**: Staggered animations with delays
4. **Responsive Design**: Animations adapt to different screen sizes

### Animation Keyframes Used

- `sequential-pulse`: Main pulsing animation with scaling and color effects
- `logo-breathe`: Subtle breathing effect with rotation and glow
- `color-shift`: Smooth color transitions across the spectrum
- `particle-float`: Floating particle effects around the logo

## Code Reference

The implementation can be found in:
- **CSS**: `docs/stylesheets/extra.css:92-166` (Animation definitions)
- **JavaScript**: `docs/javascripts/animated-logo.js:1-150` (Interactive enhancements)
- **Configuration**: `mkdocs.yml:77-78` (Asset loading)

## SVG Details

This SVG contains 7 triangular shapes with the following colors:

- Shape 1: Golden yellow (#f1c547)
- Shape 2: Purple/magenta (#c064d3)
- Shape 3: Light blue (#58b3cb)
- Shape 4: Blue (#6279f0)
- Shape 5: Orange (#ee9644)
- Shape 6: Purple (#7d5dec)
- Shape 7: Green (#a1d44d)

The original Python script animates each triangle sequentially with a 0.1s delay between each one.
