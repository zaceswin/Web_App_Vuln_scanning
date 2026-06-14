import re

class VulnerabilityAnalyzer:
    def __init__(self):
        # Common SQL error patterns to look for
        self.sql_errors = [
            "sql syntax", "mysql", "mariadb", "postgresql", 
            "unclosed quotation mark", "you have an error in your sql syntax"
        ]
        # Security headers to verify
        self.required_headers = [
            "Content-Security-Policy", "X-Frame-Options", 
            "X-Content-Type-Options", "Strict-Transport-Security"
        ]

    def analyze_sqli(self, response):
        """Checks for SQL Injection based on error messages."""
        for error in self.sql_errors:
            if re.search(error, response.text, re.IGNORECASE):
                return True, f"Possible SQLi detected: Error pattern '{error}' found."
        return False, None

    def analyze_xss(self, response, payload):
        """Checks for Reflected XSS by looking for the payload in the response."""
        # Simple check: Is the injected payload reflected exactly?
        if payload in response.text:
            return True, f"Possible XSS detected: Payload '{payload}' reflected in body."
        return False, None

    def analyze_headers(self, response):
        """Checks for missing security headers."""
        missing = [h for h in self.required_headers if h not in response.headers]
        if missing:
            return False, f"Missing Security Headers: {', '.join(missing)}"
        return True, "Security headers present."

    def analyze_open_redirect(self, response, target_url):
        """Checks if the response redirected to an external domain."""
        # Check if the final URL is different from the intended destination
        if response.history:
            # Check the last redirect location
            last_location = response.url
            if "google.com" in last_location: # Example check for malicious redirect
                return True, "Possible Open Redirect detected."
        return False, None
