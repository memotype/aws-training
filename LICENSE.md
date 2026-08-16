# Licensing

This repository uses two licenses. A project file normally has one license,
selected according to the file's primary purpose. A file is not offered under
both licenses unless an explicit notice says otherwise.

## Software and technical material

Code and other machine-oriented technical material are licensed under the MIT
License, SPDX identifier `MIT`. This includes:

- source code and executable examples
- infrastructure-as-code and infrastructure configuration
- scripts, build files, tests, and operational automation
- machine-readable configuration, manifests, schemas, and lock files
- templates and generated-source inputs intended for machine processing

The unmodified canonical license text is in
[`LICENSES/MIT.txt`](LICENSES/MIT.txt). It was obtained from the
[SPDX License List data][spdx-mit].

## Governance and human-oriented material

Governance, documentation, and other material intended primarily for people
are licensed under the Creative Commons Attribution 4.0 International Public
License, SPDX identifier `CC-BY-4.0`. This includes:

- `CODEX.md` and governance under `docs/agents/`
- guides, specifications, architecture narratives, and reference documentation
- lab instructions, training prose, evaluation criteria, and drill narratives
- readme files, changelogs, explanatory diagrams, and similar documentation
- this `LICENSE.md` file

The unmodified canonical legal code is in
[`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt). It was obtained directly
from [Creative Commons][cc-by-legal-code].

## Applying the boundary

A file-specific SPDX license notice takes precedence over these defaults.
Otherwise, apply the license associated with the material's primary purpose:

- Comments and explanatory text within a technical file are part of that file
  and are licensed under `MIT`.
- Small or illustrative code, shell commands, configuration fragments, JSON,
  YAML, infrastructure examples, and similar technical snippets within a
  human-oriented document are part of that document and are licensed under
  `CC-BY-4.0`. They do not require separate SPDX snippet tags or mid-document
  license changes.
- When technical material in documentation becomes substantial enough to be
  independently reusable as software or configuration, prefer moving it into
  a separate `MIT`-licensed file and referencing it from the documentation.
- Third-party material remains under its stated license and is not relicensed
  by this policy.

Primary purpose and reasonable engineering judgment control this boundary; no
numerical size threshold applies.

Contributions are licensed according to the same boundary unless a contribution
includes an explicit, compatible license notice accepted by the project.

[spdx-mit]: https://raw.githubusercontent.com/spdx/license-list-data/main/text/MIT.txt
[cc-by-legal-code]: https://creativecommons.org/licenses/by/4.0/legalcode.txt
