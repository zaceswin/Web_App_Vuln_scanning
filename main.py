# Initialization
crawler = Crawler("http://localhost/dvwa")
injector = Injector()
analyzer = VulnerabilityAnalyzer()
reporter = Reporter()

# Simplified loop
forms = crawler.get_forms("http://localhost/dvwa/login.php")
for form in forms:
    # Example payload for XSS
    payload = "<script>alert('XSS')</script>"
    
    # Inject
    response = injector.inject_form(form, payload)
    
    # Analyze
    is_vuln, msg = analyzer.analyze_xss(response, payload)
    
    # Report
    if is_vuln:
        reporter.add_finding("XSS", form['url'], payload, msg)

reporter.save_report()
