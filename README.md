# Azure Monitor Workbook Templates

A curated library of **Azure Monitor Workbook templates**: 824 ready-to-import
workbooks across 14 categories, gathered from Microsoft's product galleries,
community projects and the repository owner's own work, so that a useful
template is one copy-and-paste away.

Browse the full list, with a derived title and the parameters each template
expects, in **[CATALOG.md](CATALOG.md)**.

## Categories

| Folder | Workbooks | Covers |
| --- | ---: | --- |
| [AI & Machine Learning](AI%20%26%20Machine%20Learning) | 10 | Azure AI Foundry, OpenAI and Cognitive Services, Copilot Studio, experimentation, video analytics |
| [Application Insights & APM](Application%20Insights%20%26%20APM) | 37 | Usage, retention, funnels, HEART analytics, failures, performance and SDK analysis for Application Insights |
| [Authoring, Templates & Examples](Authoring%2C%20Templates%20%26%20Examples) | 31 | Layout patterns, tabs and groups, API demos, KQL syntax helpers, starter templates |
| [Compute & Containers](Compute%20%26%20Containers) | 106 | VM Insights, VM performance, AKS and Container Insights, Azure Local (HCI), Azure Virtual Desktop, HDInsight |
| [Databases & Data](Databases%20%26%20Data) | 105 | Azure SQL and SQL Managed Instance, PostgreSQL, Cosmos DB (including Cassandra and Mongo), Data Explorer, Data Factory, Spark |
| [Endpoint & Intune](Endpoint%20%26%20Intune) | 11 | Intune devices, compliance, enrollment and audit activity, Defender for Endpoint |
| [Identity & Access](Identity%20%26%20Access) | 45 | Microsoft Entra sign-ins, Conditional Access, MFA, provisioning, entitlement management, risk |
| [Integration & Messaging](Integration%20%26%20Messaging) | 33 | Logic Apps, Integration Environments, API Management, Service Bus, Azure Communication Services |
| [IoT](IoT) | 8 | IoT Edge fleet views, device details and health snapshots, platform message counts |
| [Monitoring & Management](Monitoring%20%26%20Management) | 184 | Log Analytics workspace usage and health, agents and DCRs, alerts, Update Manager, cost, assessments |
| [Networking](Networking) | 67 | Traffic analytics and NSG flow logs, VNet, VPN and ExpressRoute gateways, Application Gateway, Azure Firewall, Load Balancer, NAT Gateway, Private Link |
| [SAP & Industry Workloads](SAP%20%26%20Industry%20Workloads) | 70 | Azure Monitor for SAP solutions (NetWeaver, HANA, Db2, Oracle, SQL Server), SAP landscape views |
| [Security, Sentinel & Defender](Security%2C%20Sentinel%20%26%20Defender) | 68 | Microsoft Sentinel central and investigation workbooks, Defender for Cloud, MITRE ATT&CK, connectors |
| [Storage & Backup](Storage%20%26%20Backup) | 49 | Storage account, blob, file, queue and table metrics, Backup reports and Backup Explorer, Site Recovery jobs |

Each folder holds flat `*.workbook` files. A `.workbook` file is the JSON a
workbook exports as from the portal's Advanced Editor (`"version":
"Notebook/1.0"`) and can be pasted straight back in.

Several files share a base name with a numeric suffix, for example
`Cluster (3).workbook`. These are **different templates** that happened to be
exported under the same generic name, not copies; the catalog's title and
parameter columns tell them apart.

## What is an Azure Workbook?

[Azure Workbooks](https://learn.microsoft.com/azure/azure-monitor/visualize/workbooks-overview)
provide a flexible canvas for data analysis and rich visual reports inside the
Azure portal. They combine text, log queries (KQL), metrics, Azure Resource
Graph, alerts and parameters into interactive, shareable reports.

## How to use a template

1. Open the [Azure portal](https://portal.azure.com) and go to
   **Monitor → Workbooks**, or the **Workbooks** blade of a specific resource
   such as a Log Analytics workspace, Application Insights component or
   Sentinel workspace. Opening the workbook from the resource it targets means
   its parameters resolve to that resource automatically.
2. Select **New**, then open the **Advanced Editor** (the `</>` button).
3. Keep the editor on **Gallery Template**.
4. Paste the contents of the `.workbook` file from this repository and select
   **Apply**.
5. Choose values for the parameters at the top (subscription, workspace, time
   range and so on), then **Save** the workbook into your own subscription.

Templates in this repository contain no environment-specific resource IDs.
Where a workbook needs a default resource, it carries a placeholder such as
`/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/placeholder-rg/...`;
the portal simply treats it as an unselected resource until you pick your own.

For more detail see Microsoft's guide to
[creating and importing workbook templates](https://learn.microsoft.com/azure/azure-monitor/visualize/workbooks-templates).

## Repository tooling

Three dependency-free Python scripts keep the collection healthy. They run in
GitHub Actions on every pull request.

| Script | Purpose |
| --- | --- |
| `scripts/validate_workbooks.py` | Confirms every file is valid `Notebook/1.0` JSON and contains no leaked subscription-scoped resource IDs |
| `scripts/scrub_resource_ids.py` | Replaces real subscription, resource group and workspace identifiers with neutral placeholders (`--check` reports without writing) |
| `scripts/build_catalog.py` | Regenerates [CATALOG.md](CATALOG.md) from the workbook contents (`--check` fails when the catalog is stale) |

```bash
python scripts/scrub_resource_ids.py
python scripts/build_catalog.py
python scripts/validate_workbooks.py
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
short checklist: pick a descriptive file name, scrub environment identifiers,
keep attribution for templates that come from elsewhere, and regenerate the
catalog.

## Attribution

Many templates originate from Microsoft product galleries and other open
source projects, including the
[Application Insights Workbooks](https://github.com/microsoft/Application-Insights-Workbooks)
gallery and the [Microsoft Sentinel](https://github.com/Azure/Azure-Sentinel)
repository. Credit and links to original sources are kept inside the relevant
workbooks. If you believe a template has been included without proper
attribution, please open an issue.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
Templates sourced from other projects remain subject to their original
licenses.
