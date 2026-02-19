# Vulnerability Checks Module

This module contains various vulnerability checks that are dynamically loaded by the `CheckRunner`.

## Adding a New Check

To add a new check, simply create a new Python file in this directory with a name ending in `_checks.py` (e.g., `cve_checks.py` or `custom_checks.py`).

### Function Signature

Define your check functions starting with `check_`. They should accept a `target` (str) and an optional `port` (int).

```python
def check_example(target: str, port: int = 1234) -> dict:
    """
    Description of what this check does.
    """
    result = {
        "service": "Example Service",
        "port": port,
        "status": "Closed",
        "vulnerable": False,
        "description": "Port is closed"
    }
    
    # ... implementation ...
    
    return result
```

### Return Dictionary Keys

- `service`: Name of the service being checked.
- `port`: The port number scanned.
- `status`: "Open", "Closed", "Filtered", "Error", or "Skipped".
- `vulnerable`: Boolean (True/False). Set to True if a vulnerability is found.
- `description`: Human-readable description of the finding.
- `banner`: (Optional) The banner grabbed from the service.
- `error`: (Optional) Error message if an exception occurred.

## Dynamic Loading

The `runner.py` script automatically discovers any file matching `*_checks.py` in this directory and registers any function starting with `check_`. You do not need to manually register your checks anywhere.
