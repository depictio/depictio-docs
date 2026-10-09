---
description: "The Depictio rose: the brand mark drawn as a polar-area chart whose radii animate."
---

# Animated Logo

The Depictio mark, the rose, is a polar-area chart: eight wedges around a common centre, one colour each, each with its own radius. Animating the radii turns the logo into a small chart that keeps refreshing. When all eight radii are equal, the wedges close into a disc.

<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 1.5rem; margin: 1.5rem 0;">
  <figure style="margin: 0;">
    <depictio-rose mode="loading" size="96" label=""></depictio-rose>
    <figcaption><code>loading</code><br>never rests</figcaption>
  </figure>
  <figure style="margin: 0;">
    <depictio-rose mode="live" size="96" label=""></depictio-rose>
    <figcaption><code>live</code><br>a chart refreshing</figcaption>
  </figure>
  <figure style="margin: 0;">
    <depictio-rose mode="fan" size="96" label=""></depictio-rose>
    <figcaption><code>fan</code><br>opens like a fan</figcaption>
  </figure>
  <figure style="margin: 0;">
    <depictio-rose mode="logo" size="96" label=""></depictio-rose>
    <figcaption><code>logo</code><br>at rest</figcaption>
  </figure>
</div>

The animations pause while the mark is scrolled out of view or the tab is hidden. With `prefers-reduced-motion` set, the mark stays on the static logo shape.

## Where it is used

- **Loading indicator**: the Depictio app shows the `loading` mode while it is busy.
- **Header of this site**: the logo in the top bar is the rose at rest. Hover it for a moment and it plays the `fan`; move away and it settles back.

## One source

The rose is drawn by a single generated script, `depictio-rose.js`, which registers the `<depictio-rose>` custom element. The Depictio app, this documentation site and the talk deck all load that same file, so the mark looks and moves the same everywhere. The wedges are built from geometry at runtime: there is no image to fetch.

```html
<script src="depictio-rose.js"></script>
<depictio-rose mode="loading" size="64"></depictio-rose>
```
