---
name: changelog-entry
description: >-
  Adds an entry to CHANGELOG.md using the Keep a Changelog format, creating the
  file if it does not exist, so change history stays consistent and
  release-ready.
metadata:
  disable-model-invocation: true
---

---
name: changelog-entry
description: Adds an entry to CHANGELOG.md using the Keep a Changelog format, creating the file if it does not exist, so change history stays consistent and release-ready.
user-invocable: true
---

Add an entry to CHANGELOG.md using the Keep a Changelog format (https://keepachangelog.com/).

- If CHANGELOG.md does not exist, create it at the project root with this structure before adding an entry:

  # Changelog

  All notable changes to this project are documented in this file.
  The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

  ## [Unreleased]

- Add new entries under the `## [Unreleased]` section, under one of these subheadings: `### Added`, `### Changed`, `### Fixed`, `### Removed`. Create the subheading if it is not already present under `## [Unreleased]`.
- Write each entry as a single bullet point in the imperative mood ("Add", not "Added"), starting with a capital letter, with no trailing period.
- Base the entry on the actual diff, not on the wording of the request. Run `git diff` to review what changed before writing the entry.
- Only edit CHANGELOG.md. Do not stage or commit the change.
