import requests

class Injector:
    def __init__(self, session=None):
        # Use a requests session to persist cookies (important for DVWA)
        self.session = session or requests.Session()

    def inject_form(self, form_details, payload):
        """Injects a payload into all input fields of a form."""
        target_url = form_details['url']
        method = form_details['method']
        inputs = form_details['inputs']
        
        data = {}
        for input_field in inputs:
            # We assume 'text' or 'search' inputs are our targets
            if input_field['type'] in ["text", "search", "password"]:
                data[input_field['name']] = payload
            else:
                data[input_field['name']] = input_field.get('value', '')

        # Send the request
        try:
            if method == "post":
                return self.session.post(target_url, data=data)
            else:
                return self.session.get(target_url, params=data)
        except Exception as e:
            print(f"[-] Error injecting into {target_url}: {e}")
            return None
