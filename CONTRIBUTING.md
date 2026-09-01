# Contributing

Thanks for adding to the collection. A pull request only needs a few things
to be mergeable.

## Adding a workbook

1. Export the workbook from the Azure portal: open it, choose **Edit**, then
   **Advanced Editor** (`</>`), switch to **Gallery Template**, and copy the
   JSON.
2. Save it as `<Category>/<Descriptive Name>.workbook` in the folder that
   fits best. Pick a name that says what the workbook shows; avoid generic
   portal names such as `Overview.workbook` or names ending in `(2)`.
3. Remove anything specific to your environment by running

   ```bash
   python scripts/scrub_resource_ids.py
   ```

   which swaps subscription IDs, resource groups and workspace names in
   `fallbackResourceIds`, `crossComponentResources` and parameter defaults for
   neutral placeholders. Check the diff for anything else the script would not
   know about, such as tenant names or user principal names in query text.
4. If the template comes from another project, keep its original attribution
   in a text step at the top of the workbook and mention the source in the
   pull request.
5. Regenerate the catalog and validate:

   ```bash
   python scripts/build_catalog.py
   python scripts/validate_workbooks.py
   ```

The same three scripts run in CI on every pull request. They need only a
standard Python 3.9+ installation; there are no third-party dependencies.

## Changing an existing workbook

Keep the file valid `Notebook/1.0` JSON, leave the two-space formatting the
portal produces so diffs stay readable, and re-run the catalog script if the
first heading or top-level parameters changed.

## Reporting problems

Open an issue that names the workbook file and describes what you expected.
If a template is included without proper credit to its original author, say
so and it will be fixed.
