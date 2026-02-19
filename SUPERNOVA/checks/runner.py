import importlib
import inspect
from typing import Dict, List, Any

class CheckRunner:
    def __init__(self):
        self.checks = []
        self._load_checks()

    def _load_checks(self):
        """Discovers and registers check functions from the checks package."""
        # Dynamically load all python files in the current directory that end with _checks.py
        # This allows teammates to add new check files without modifying this runner.
        import os
        import glob
        
        current_dir = os.path.dirname(__file__)
        check_files = glob.glob(os.path.join(current_dir, '*_checks.py'))
        
        for file_path in check_files:
            filename = os.path.basename(file_path)
            if filename == 'verify_checks.py':
                continue
                
            module_name = f"checks.{filename[:-3]}" # Remove .py extension
            
            try:
                module = importlib.import_module(module_name)
                # Look for functions starting with 'check_'
                for name, func in inspect.getmembers(module, inspect.isfunction):
                    if name.startswith('check_'):
                        self.register_check(func)
            except ImportError as e:
                print(f"Warning: Could not import {module_name}: {e}")

    def register_check(self, check_func):
        """Registers a check function."""
        self.checks.append(check_func)

    def run_all(self, target: str) -> List[Dict[str, Any]]:
        """Runs all registered checks against the target."""
        results = []
        for check in self.checks:
            try:
                # Assuming checks take 'target' as a positional argument
                # Checks should return a dict with result info
                result = check(target)
                if result:
                     # Add check name if not present
                    if 'check_name' not in result:
                        result['check_name'] = check.__name__
                    results.append(result)
            except Exception as e:
                results.append({
                    'check_name': check.__name__,
                    'status': 'Error',
                    'message': str(e)
                })
        return results