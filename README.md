# Azure Monitor Workbook Templates

A curated collection of **Azure Monitor Workbook templates** — gathered and
authored to make it easier to visualize, troubleshoot, and report on Azure
resources, logs, and metrics.

## Purpose

This repository serves as a central place to host a collection of Azure
Workbook templates. The templates here come from two sources:

- **Templates created by the repository owner** for real-world monitoring,
  reporting, and operational scenarios.
- **Templates sourced from other open source repositories**, included here to
  build a single, convenient reference library. Where a template originates
  from another project, attribution to the original source is preserved.

The goal is to provide a reusable, ready-to-deploy set of workbooks that can be
imported directly into Azure Monitor.

## What is an Azure Workbook?

[Azure Workbooks](https://learn.microsoft.com/azure/azure-monitor/visualize/workbooks-overview)
provide a flexible canvas for data analysis and the creation of rich visual
reports within the Azure portal. They let you combine text, log queries
(KQL), metrics, and parameters into interactive, shareable reports.

## Repository Structure

Each folder in this repository contains one or more related workbook
templates, typically stored as Azure Resource Manager (ARM) / Gallery
Template JSON files (`.json`) that can be imported into Azure Monitor.

```
.
├── <Workbook Category>/
│   └── <workbook>.json
├── ...
└── README.md
```

## How to Use a Template

1. Open the [Azure portal](https://portal.azure.com) and navigate to
   **Azure Monitor → Workbooks** (or the Workbooks blade of a specific
   resource).
2. Create a **New** workbook, then open the **Advanced Editor** (the `</>`
   icon).
3. Set the editor to **Gallery Template** mode.
4. Copy the contents of the desired `.json` template from this repository and
   paste it into the editor.
5. Click **Apply** to load the workbook, then **Save** it to your own
   subscription.

For more detail, see the official guide on
[creating and importing workbook templates](https://learn.microsoft.com/azure/azure-monitor/visualize/workbooks-templates).

## Contributing

Contributions are welcome. If you have a workbook template you'd like to
share:

1. Fork the repository.
2. Add your template to an appropriately named folder.
3. Include a short description and, if the template is derived from another
   project, attribution to the original source.
4. Open a pull request.

## Attribution

Some templates in this repository originate from other open source projects.
Credit and links to the original sources are retained alongside the relevant
templates. If you believe a template has been included without proper
attribution, please open an issue.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
