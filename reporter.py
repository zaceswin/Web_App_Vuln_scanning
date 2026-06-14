import json
import datetime

class Reporter:
    def __init__(self, filename="scan_report.json"):
        self.filename = filename
        self.findings = []

    def add_finding(self, vulnerability_type, url, payload, evidence):
        """Records a vulnerability finding."""
        finding = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": vulnerability_type,
            "url": url,
            "payload": payload,
            "evidence": evidence
        }
        self.findings.append(finding)
        print(f"[!] Vulnerability Logged: {vulnerability_type} at {url}")

    def save_report(self):
        """Saves all findings to a JSON file."""
        with open(self.filename, 'w') as f:
            json.dump(self.findings, f, indent=4)
        print(f"[*] Report saved to {self.filename}")
