# FAQ

Ongoing list of frequently asked questions.

## Code Mode

### What is Code Mode in figure creation?

Code Mode allows you to create figures by writing Python/Plotly code directly instead of using the UI interface. You get full control over visualization parameters and can create complex, customized plots using familiar Python syntax.

### How secure is code execution in Code Mode?

Code execution uses **RestrictedPython** (Zope Foundation's battle-tested security framework) with multiple protection layers:
- **Compile-time restrictions**: Unsafe operations blocked before code runs
- **Isolated execution environment**: Code runs with only approved globals and built-ins
- **No system access**: File system, network, and OS operations completely blocked
- **Memory protection**: Works on DataFrame copies to prevent data corruption
- **Comprehensive logging**: All execution attempts are monitored and attributed

### Can I import custom libraries in Code Mode?

No, only pre-approved libraries are available for security reasons:
- `plotly.express` (as `px`)
- `plotly.graph_objects` (as `go`)
- `pandas` (as `pd`)
- `numpy` (as `np`)
- Basic Python built-ins (str, int, len, range, etc.)

### What's the difference between UI Mode and Code Mode?

| Feature | UI Mode | Code Mode |
|---------|---------|-----------|
| **Ease of Use** | Point-and-click interface | Requires Python knowledge |
| **Customization** | Limited to UI options | Full Plotly customization |
| **Speed** | Quick for standard plots | Better for complex visualizations |
| **Learning Curve** | Beginner-friendly | Requires coding skills |

### How do I access my data in Code Mode?

Your selected data collection is automatically available as the `df` variable (pandas DataFrame). Simply use `df` in your code:

```python
# Example: Create a scatter plot
fig = px.scatter(df, x='column1', y='column2', color='category')
```

### Why do I get "Import not allowed" or compilation errors?

RestrictedPython automatically blocks unsafe operations at compile-time. Common issues:

**✅ Allowed:**
```python
# Pre-imported libraries (no import needed)
fig = px.scatter(df, x='col1', y='col2')
df_filtered = df[df['value'] > 10]
```

**❌ Blocked by RestrictedPython:**
```python
import requests          # Network access blocked
import os               # System access blocked
open('file.txt')        # File operations blocked
exec('some_code')       # Dynamic execution blocked
```

The security framework prevents these operations before your code runs, ensuring complete safety.

### Can I save and reuse code snippets?

Currently, code is saved with each figure component. For reusable code patterns, you can copy-paste between components or keep your own external code library for reference.

## Known Issues
