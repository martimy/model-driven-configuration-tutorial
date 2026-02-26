# Tutorial


## Motivation

Modern networks are no longer small, static environments managed primarily through manual configuration. Today’s infrastructures are large-scale, multi-vendor, automated, and continuously changing, which requires management interfaces that are reliable, structured, and programmatically accessible.

Traditional router configuration approaches—especially those centered on CLI interaction—are increasingly inadequate for these environments. While the CLI remains useful for human operators, it does not scale well for automation. Techniques such as screen scraping or scripting interactive sessions (for example, using expect-like tools) are fragile and difficult to maintain, particularly in complex production networks. As networks grow in size and diversity, these approaches become error-prone and operationally inefficient.

To address these challenges, modern network systems are evolving toward an API-first architecture. In this model, configuration and operational state are accessed through structured programmatic interfaces, while the CLI is repositioned as just another client layered on top of these APIs rather than being the primary control interface.

The most significant architectural shift enabling this transition is the adoption of model-driven management, centered around the YANG data modeling language. Instead of writing configuration logic tied to a specific interface (such as CLI command handlers), developers define a structured data model describing configuration and state. Management interfaces—whether CLI, NETCONF, RESTCONF, or others—interact with the same underlying model.

This approach provides several key advantages:

* Interface independence: Configuration logic is written once and reused across multiple management protocols.
* Consistency: The same validation and processing logic is applied regardless of whether changes originate from automation tools or manual CLI input.
* Extensibility: New management interfaces can be introduced without redesigning the internal configuration logic.
* Automation readiness: Structured data models align naturally with modern automation workflows.

As described in RFC 7950, YANG was originally designed to model data for the NETCONF protocol, defining hierarchical structures for configuration data, operational state, RPCs, and notifications. Although closely associated with NETCONF, YANG is protocol-independent and is now widely used with multiple management frameworks, including RESTCONF and gNMI.

In a model-driven architecture, configuration changes are no longer interpreted as sequences of CLI commands. Instead, they are treated as structured data transactions validated against the YANG model and processed through common callback logic. For example, whether a configuration change originates from a NETCONF session or a CLI terminal, the same internal processing pipeline is used. This ensures feature parity and consistent behavior across all management interfaces.
