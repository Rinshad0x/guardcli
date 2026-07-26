"""
GuardCLI - Linux Personal OPSEC Audit Tool
Copyright (c) 2026 Rinshad0x

Licensed under the MIT License.
See LICENSE for details.
"""

class AuditEngine:
    def __init__(self):
        self.results = []

    def run_check(self, check_function):
        result = check_function()
        self.results.append(result)

    def get_results(self):
        return self.results
