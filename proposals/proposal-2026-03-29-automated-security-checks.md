# Proposal: Automated Security Checks in Deployment Pipeline

**Objective:**
Integrate automated security checks into the deployment pipeline to proactively identify vulnerabilities before production releases.

**Background:**
Recent audits highlighted gaps in runtime security validation. Manual checks are error-prone and time-consuming.

**Proposed Solution:**
1. Add pre-deploy static analysis using Snyk for dependency scanning
2. Implement runtime OWASP ZAP scans during staging
3. Enforce policy gates for high-severity issues

**Benefits:**
- Reduce security debt by 40% QoQ
- Faster incident response
- Compliance with ISO 27001 requirements

**Next Steps:**
- Prototype with 2 critical services by April 15
- Cross-team review by security working group