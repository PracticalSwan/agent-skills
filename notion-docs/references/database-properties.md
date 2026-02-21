# Notion Database Property Types

Complete reference for all Notion database property types, their configuration, use cases, and API format
when working with Notion MCP tools.

---

## Title

The primary identifier for every database page. Every database has exactly one title property.

- **Description:** Rich text field that serves as the page name. Always required.
- **Configuration:** Cannot be deleted. Can be renamed.
- **Use Cases:** Page names, task titles, item labels, document names.
- **API Format:**
  ```json
  { "Task Name": "Implement login flow" }
  ```
- **Schema Definition:**
  ```json
  { "Task Name": { "type": "title", "title": {} } }
  ```

---

## Rich Text

Multi-line text field supporting inline formatting.

- **Description:** Free-form text with bold, italic, links, mentions, and other inline styles.
- **Configuration:** No additional config needed.
- **Use Cases:** Descriptions, notes, comments, summaries.
- **API Format:**
  ```json
  { "Description": "A detailed description with **bold** text" }
  ```
- **Schema Definition:**
  ```json
  { "Description": { "type": "rich_text", "rich_text": {} } }
  ```

---

## Number

Numeric values with optional formatting.

- **Description:** Stores integers or decimals. Supports format options for display.
- **Configuration:** Optional `format` — `"number"`, `"number_with_commas"`, `"percent"`, `"dollar"`, `"euro"`, `"pound"`, `"yen"`, `"ruble"`, `"rupee"`, `"won"`, `"yuan"`, etc.
- **Use Cases:** Priority scores, story points, prices, percentages, quantities.
- **API Format:**
  ```json
  { "Priority": 5 }
  { "Price": 29.99 }
  ```
  Must be a JavaScript number, not a string.
- **Schema Definition:**
  ```json
  { "Story Points": { "type": "number", "number": { "format": "number" } } }
  ```

---

## Select

Single-choice dropdown with predefined options.

- **Description:** Allows selecting exactly one value from a list of options. Each option has a name and optional color.
- **Configuration:** Define options with `name` and optional `color`.
- **Use Cases:** Status, priority level, category, type, environment.
- **API Format:**
  ```json
  { "Status": "In Progress" }
  ```
- **Schema Definition:**
  ```json
  {
    "Priority": {
      "type": "select",
      "select": {
        "options": [
          { "name": "Critical", "color": "red" },
          { "name": "High", "color": "orange" },
          { "name": "Medium", "color": "yellow" },
          { "name": "Low", "color": "green" }
        ]
      }
    }
  }
  ```
- **Available Colors:** `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`.

---

## Multi-Select

Multiple-choice tags from predefined options.

- **Description:** Allows selecting one or more values from a list. Renders as colored tags.
- **Configuration:** Same option structure as Select.
- **Use Cases:** Tags, labels, skills, categories, components affected.
- **API Format:**
  ```json
  { "Tags": "frontend, bug, urgent" }
  ```
  Comma-separated string of option names.
- **Schema Definition:**
  ```json
  {
    "Tags": {
      "type": "multi_select",
      "multi_select": {
        "options": [
          { "name": "frontend", "color": "blue" },
          { "name": "backend", "color": "green" },
          { "name": "bug", "color": "red" },
          { "name": "feature", "color": "purple" }
        ]
      }
    }
  }
  ```

---

## Date

Date or date-range values with optional time component.

- **Description:** Stores a start date and optional end date. Can include time and timezone.
- **Configuration:** No additional config. Supports date-only or datetime.
- **Use Cases:** Due dates, sprint dates, event dates, deadlines, date ranges.
- **API Format (expanded):**
  ```json
  {
    "date:Due Date:start": "2024-12-25",
    "date:Due Date:end": "2025-01-15",
    "date:Due Date:is_datetime": 0
  }
  ```
  - `start` — ISO 8601 date string (required).
  - `end` — ISO 8601 date string (optional, for ranges).
  - `is_datetime` — `0` for date-only, `1` for datetime.
- **Schema Definition:**
  ```json
  { "Due Date": { "type": "date", "date": {} } }
  ```

---

## People

References to Notion workspace users.

- **Description:** Links one or more workspace members to a page.
- **Configuration:** No additional config.
- **Use Cases:** Assignee, reviewer, owner, participants.
- **API Format:**
  ```json
  { "Assignee": "user-uuid-here" }
  ```
- **Schema Definition:**
  ```json
  { "Assignee": { "type": "people", "people": {} } }
  ```

---

## Files & Media

File attachments and media uploads.

- **Description:** Stores file references (uploaded or external URLs).
- **Configuration:** No additional config.
- **Use Cases:** Attachments, screenshots, design files, documents.
- **API Format:** Typically managed via Notion UI or API file objects.
- **Schema Definition:**
  ```json
  { "Attachments": { "type": "files", "files": {} } }
  ```

---

## Checkbox

Boolean true/false toggle.

- **Description:** Simple checked/unchecked state.
- **Configuration:** No additional config.
- **Use Cases:** Completion flags, feature toggles, approval status.
- **API Format:**
  ```json
  { "Is Complete": "__YES__" }
  { "Is Complete": "__NO__" }
  ```
  Use `"__YES__"` for checked, `"__NO__"` for unchecked.
- **Schema Definition:**
  ```json
  { "Is Complete": { "type": "checkbox", "checkbox": {} } }
  ```

---

## URL

Stores a single URL.

- **Description:** Validated URL field displayed as a clickable link.
- **Configuration:** No additional config.
- **Use Cases:** Repository links, documentation links, external references.
- **API Format:**
  ```json
  { "userDefined:URL": "https://github.com/org/repo" }
  ```
  Properties named `url` (case-insensitive) must use the `userDefined:` prefix.
- **Schema Definition:**
  ```json
  { "Repository": { "type": "url", "url": {} } }
  ```

---

## Email

Stores an email address.

- **Description:** Validated email field.
- **Configuration:** No additional config.
- **Use Cases:** Contact email, support email, notification address.
- **API Format:**
  ```json
  { "Contact Email": "team@example.com" }
  ```
- **Schema Definition:**
  ```json
  { "Contact Email": { "type": "email", "email": {} } }
  ```

---

## Phone Number

Stores a phone number string.

- **Description:** Phone number field (no strict validation format).
- **Configuration:** No additional config.
- **Use Cases:** Contact numbers, support lines.
- **API Format:**
  ```json
  { "Phone": "+1-555-0123" }
  ```
- **Schema Definition:**
  ```json
  { "Phone": { "type": "phone_number", "phone_number": {} } }
  ```

---

## Formula

Computed value derived from other properties.

- **Description:** Evaluates an expression using other property values. Read-only.
- **Configuration:** Requires an `expression` string using Notion's formula syntax.
- **Use Cases:** Calculated fields, conditional labels, derived metrics, concatenations.
- **API Format:** Read-only — cannot be set directly.
- **Schema Definition:**
  ```json
  {
    "Days Until Due": {
      "type": "formula",
      "formula": {
        "expression": "dateBetween(prop(\"Due Date\"), now(), \"days\")"
      }
    }
  }
  ```

---

## Relation

Links pages between two databases.

- **Description:** Creates a relationship between pages in different (or the same) databases.
- **Configuration:** Requires `data_source_id` of the target database's data source. Supports `single_property` (one-way) or `dual_property` (two-way).
- **Use Cases:** Task → Project linking, Epic → Story, Document → Author.
- **API Format:** Pass related page IDs.
- **Schema Definition (one-way):**
  ```json
  {
    "Project": {
      "type": "relation",
      "relation": {
        "data_source_id": "target-data-source-uuid",
        "type": "single_property",
        "single_property": {}
      }
    }
  }
  ```
- **Schema Definition (two-way):**
  ```json
  {
    "Tasks": {
      "type": "relation",
      "relation": {
        "data_source_id": "target-data-source-uuid",
        "type": "dual_property",
        "dual_property": {
          "synced_property_name": "Related Project"
        }
      }
    }
  }
  ```

---

## Rollup

Aggregates values from a related database via a relation property.

- **Description:** Computes aggregated values (count, sum, average, etc.) from pages linked through a relation.
- **Configuration:** Requires a relation property name/ID and a target property to roll up, plus an aggregation function.
- **Use Cases:** Total story points in a sprint, count of tasks per project, percent complete.
- **API Format:** Read-only — cannot be set directly.
- **Schema Definition:**
  ```json
  {
    "Total Points": {
      "type": "rollup",
      "rollup": {
        "relation_property_name": "Tasks",
        "rollup_property_name": "Story Points",
        "function": "sum"
      }
    }
  }
  ```
- **Available Functions:** `count`, `count_values`, `empty`, `not_empty`, `unique`, `show_unique`, `percent_empty`, `percent_not_empty`, `sum`, `average`, `median`, `min`, `max`, `range`, `earliest_date`, `latest_date`, `date_range`, `checked`, `unchecked`, `percent_checked`, `percent_unchecked`, `show_original`.

---

## Created Time

Auto-populated timestamp of when the page was created.

- **Description:** Read-only timestamp. Automatically set on page creation.
- **Configuration:** No additional config.
- **Use Cases:** Audit trail, sorting by creation date, filtering recent items.
- **API Format:** Read-only.
- **Schema Definition:**
  ```json
  { "Created": { "type": "created_time", "created_time": {} } }
  ```

---

## Created By

Auto-populated reference to the user who created the page.

- **Description:** Read-only user reference. Automatically set on creation.
- **Configuration:** No additional config.
- **Use Cases:** Audit trail, filtering by creator.
- **API Format:** Read-only.
- **Schema Definition:**
  ```json
  { "Created By": { "type": "created_by", "created_by": {} } }
  ```

---

## Last Edited Time

Auto-populated timestamp of the most recent edit.

- **Description:** Read-only timestamp. Updates automatically on any page modification.
- **Configuration:** No additional config.
- **Use Cases:** Sorting by recent activity, staleness detection.
- **API Format:** Read-only.
- **Schema Definition:**
  ```json
  { "Updated": { "type": "last_edited_time", "last_edited_time": {} } }
  ```

---

## Last Edited By

Auto-populated reference to the last user who edited the page.

- **Description:** Read-only user reference. Updates on any edit.
- **Configuration:** No additional config.
- **Use Cases:** Audit trail, recent editor tracking.
- **API Format:** Read-only.
- **Schema Definition:**
  ```json
  { "Last Editor": { "type": "last_edited_by", "last_edited_by": {} } }
  ```

---

## Status

Built-in status property with grouped options (To-do, In progress, Complete).

- **Description:** Special select-like property with three status groups. Options are categorized into groups automatically.
- **Configuration:** No additional config at creation. Configure status options and groups in Notion UI.
- **Use Cases:** Task/issue status, workflow stage, approval state.
- **API Format:**
  ```json
  { "Status": "In Progress" }
  ```
- **Schema Definition:**
  ```json
  { "Status": { "type": "status", "status": {} } }
  ```

---

## Unique ID

Auto-incremented identifier with optional prefix.

- **Description:** Auto-generated sequential ID. Read-only. Supports a string prefix.
- **Configuration:** Optional `prefix` string (e.g., `"TASK"` produces `TASK-1`, `TASK-2`, etc.).
- **Use Cases:** Issue numbers, ticket IDs, sequential identifiers.
- **API Format:** Read-only.
- **Schema Definition:**
  ```json
  {
    "ID": {
      "type": "unique_id",
      "unique_id": { "prefix": "TASK" }
    }
  }
  ```
- **Notes:** Maximum one `unique_id` property per database.

---

## Quick Reference Table

| Type | Writable | Supports Sorting | Supports Filtering | Notes |
|------|----------|-------------------|--------------------|-------|
| Title | Yes | Yes | Yes | Required, exactly one per DB |
| Rich Text | Yes | Yes | Yes | |
| Number | Yes | Yes | Yes | Use JS numbers |
| Select | Yes | Yes | Yes | |
| Multi-Select | Yes | Yes | Yes | Comma-separated string |
| Date | Yes | Yes | Yes | Expanded format with `:start`/`:end` |
| People | Yes | Yes | Yes | User UUIDs |
| Files | Yes | No | No | |
| Checkbox | Yes | Yes | Yes | `__YES__` / `__NO__` |
| URL | Yes | Yes | Yes | Prefix with `userDefined:` if named "url" |
| Email | Yes | Yes | Yes | |
| Phone | Yes | Yes | Yes | |
| Formula | Read-only | Yes | Yes | Expression-based |
| Relation | Yes | No | Yes | Links databases |
| Rollup | Read-only | Yes | Yes | Aggregates relation data |
| Created Time | Read-only | Yes | Yes | Auto-set |
| Created By | Read-only | Yes | Yes | Auto-set |
| Last Edited Time | Read-only | Yes | Yes | Auto-updated |
| Last Edited By | Read-only | Yes | Yes | Auto-updated |
| Status | Yes | Yes | Yes | Grouped status options |
| Unique ID | Read-only | Yes | Yes | Max one per DB |
