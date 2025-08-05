# Security Features

Depictio implements comprehensive security measures to protect your data and ensure safe operation in production environments.

## Authentication & Authorization

### JWT-Based Authentication
- **Token Security**: Public/private key encryption for session tokens
- **Session Management**: Configurable token lifetime and refresh mechanisms  
- **Role-Based Access**: User and group-based permissions for projects and dashboards


## Code Execution Security (Code Mode)

### RestrictedPython Security
- **Battle-Tested Security**: Uses RestrictedPython (Zope Foundation) for code execution
- **Compile-Time Restrictions**: Unsafe operations blocked during code compilation
- **Safe Execution Environment**: Pre-approved globals and built-ins only
- **No System Access**: File system, network, and OS operations completely blocked

### Security Architecture
- **Restricted Compilation**: Code compiled with `compile_restricted()` before execution
- **Safe Guards**: Custom guards for pandas DataFrame operations (`_getitem_`, `_getattr_`)
- **Isolated Globals**: Execution environment contains only approved libraries and functions
- **Memory Protection**: DataFrame operations work on copies to prevent data corruption

### Allowed Libraries & Operations
```python
# Available libraries in Code Mode
import plotly.express as px      # Visualization library
import plotly.graph_objects as go # Advanced plotting
import pandas as pd              # Data manipulation
df                              # Your dataset (read-only copy)

# Safe built-in functions
len(), range(), str(), int(), float(), sum(), min(), max()
```

### Automatically Blocked Operations
RestrictedPython prevents these operations at compile-time:

- **File Operations**: `open()`, file I/O, filesystem access
- **Network Access**: `requests`, `urllib`, socket operations  
- **System Calls**: `os.*`, `sys.*`, `subprocess`, shell commands
- **Dangerous Built-ins**: `exec()`, `eval()`, `__import__()`, `compile()`
- **Attribute Access**: Private attributes (underscore methods) on unsafe objects


## Security Reporting

If you discover a security vulnerability, please report it through appropriate channels:

- Report code execution restriction bypass attempts immediately
- Document and report any unauthorized data access

---

*Security is a shared responsibility. While Depictio provides robust security features, proper configuration and operational practices are essential for maintaining a secure environment.*