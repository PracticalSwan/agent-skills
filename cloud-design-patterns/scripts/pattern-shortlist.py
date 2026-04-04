#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json


SHORTLISTS = {
    "reliability": {
        "patterns": ["Bulkhead", "Circuit Breaker", "Retry", "Health Endpoint Monitoring", "Saga"],
        "reference": "references/reliability-resilience.md",
        "reason": "Use when failures, retries, and graceful degradation dominate the design discussion.",
    },
    "performance": {
        "patterns": ["Cache-Aside", "CQRS", "Queue-Based Load Leveling", "Rate Limiting", "Sharding"],
        "reference": "references/performance.md",
        "reason": "Use when latency, throughput, caching, or uneven load are the main constraints.",
    },
    "messaging": {
        "patterns": ["Publisher-Subscriber", "Competing Consumers", "Pipes and Filters", "Choreography"],
        "reference": "references/messaging-integration.md",
        "reason": "Use when asynchronous workflows, decoupling, or event-driven integration dominate the problem.",
    },
    "migration": {
        "patterns": ["Strangler Fig", "Anti-Corruption Layer", "Deployment Stamps"],
        "reference": "references/architecture-design.md",
        "reason": "Use when modernizing or separating legacy systems without a risky big-bang rewrite.",
    },
    "security": {
        "patterns": ["Federated Identity", "Valet Key", "Quarantine"],
        "reference": "references/security.md",
        "reason": "Use when the discussion centers on controlled access, isolated handling, or delegated authorization.",
    },
    "operations": {
        "patterns": ["External Configuration Store", "Geode", "Static Content Hosting"],
        "reference": "references/deployment-operational.md",
        "reason": "Use when multi-region operations, runtime configuration, or deployment management dominate the design.",
    },
    "eventing": {
        "patterns": ["Event Sourcing"],
        "reference": "references/event-driven.md",
        "reason": "Use when auditability, event history, or replayable state are central requirements.",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Turn workload concerns into a pattern shortlist.")
    parser.add_argument("--concern", action="append", required=True, help="Concern to evaluate. Repeat as needed.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = parser.parse_args()

    concerns = [value.lower().strip() for value in args.concern]
    results = []
    for concern in concerns:
        if concern in SHORTLISTS:
            entry = {"concern": concern, **SHORTLISTS[concern]}
            results.append(entry)

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    if not results:
        print("No shortlist available for the supplied concerns. Try: reliability, performance, messaging, migration, security, operations, eventing.")
        return 1

    print("## Pattern Shortlist\n")
    for entry in results:
        print(f"### {entry['concern'].title()}")
        print(f"- Patterns: {', '.join(entry['patterns'])}")
        print(f"- Reference: `{entry['reference']}`")
        print(f"- Why: {entry['reason']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
