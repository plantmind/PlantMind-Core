# STD-001 — PlantMind Development Standards

**Document ID:** STD-001  
**Project:** PlantMind Enterprise Platform  
**Version:** 1.0  
**Status:** Approved  
**Owner:** Chief Software Architect

---

# Purpose

This document defines the engineering standards that govern the development of PlantMind.

Every developer, AI agent, automation, and future contributor must follow these standards.

These rules are considered mandatory unless superseded by a newer approved standard.

---

# Engineering Philosophy

PlantMind is not a chatbot.

PlantMind is an Enterprise Industrial Intelligence Operating System.

Every architectural decision must prioritize:

- Scalability
- Maintainability
- Reliability
- Security
- Explainability
- Industrial Safety

Short-term convenience must never compromise long-term architecture.

---

# Non-Negotiable Rules

The following rules shall never be violated.

1. Business Logic shall never exist inside API Routers.

2. main.py shall only initialize the platform.

3. Every module must have a single responsibility.

4. No hardcoded credentials.

5. Every AI recommendation must provide reasoning whenever technically possible.

6. Every important action must be logged.

7. Security takes priority over convenience.

8. PlantMind shall always support On-Premise deployment.

9. Every new feature must have a clear architectural purpose.

10. If a file has no reason to exist, it should not exist.