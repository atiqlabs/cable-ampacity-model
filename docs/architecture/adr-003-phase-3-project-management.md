# ADR-003: Phase 3 Project Management Architecture

**Status:** Accepted and frozen for Phase 3 implementation  
**Date:** 2026-07-14  
**Decision owners:** AtiqLabs Engineering Software Team  
**Scope:** IEC 60287 Cable Ampacity Software, project-management subsystem

## 1. Purpose

This Architecture Decision Record (ADR) is the authoritative design baseline for Phase 3. It defines project-management vocabulary, ownership, persistence, controller boundaries, compatibility rules, and extension points.

Phase 3 adds project lifecycle and multiple-study management without redesigning the existing MVC architecture or altering the validated IEC 60287 calculation engine except where a genuine engineering correction is approved.

## 2. Context

The application currently supports one live IEC 60287 ampacity case:

```text
PySide6 GUI -> MainController -> engineering models -> AmpacityEngine -> results
```

`MainController` coordinates one case through the existing `Cable`, `Installation`, `Environment`, and `AmpacityEngine` objects. The calculation engine is validated and outside Phase 3 scope. Commercial use requires a persistent work package containing independent calculation cases, engineering metadata, report context, and safe save/load behavior.

## 3. Goals and non-goals

### Goals

- Create, open, save, and save-as project files.
- Organize multiple independently editable and calculable studies per project.
- Preserve reproducibility, traceability, and backwards compatibility.
- Keep calculation, persistence, controller, and GUI responsibilities separate.
- Establish safe schema evolution from the first saved file.

### Non-goals for Phase 3

- Redesigning MVC or replacing `MainController`.
- Changing IEC 60287 equations or calculation-engine behavior.
- Material, cable, or installation libraries.
- Project attachments, collaboration, database storage, or cloud synchronization.
- Revision/approval workflow and report-generation implementation.
- A generic inheritance framework for future calculation modules.

## 4. Approved domain vocabulary

| Term | Definition |
|---|---|
| **Project** | A persistent engineering work package containing metadata and one or more studies. |
| **Study** | One self-contained, independently editable and calculable engineering case. |
| **Study type** | Stable identifier defining a study calculation/input contract. Phase 3 supports `iec_60287_ampacity`. |
| **Active study** | The study currently exposed to the GUI and represented by the active `MainController`. |
| **Engineering inputs** | Persisted model data required to reproduce a calculation: cable, installation, duct/duct bank, environment, and configuration. |
| **Result snapshot** | Optional persisted derived output retained for audit, comparison, or performance; never engineering authority. |
| **Project document** | The serialized, versioned representation stored in a `.iecproj` file. |
| **Schema version** | Version of the project-document structure. |
| **Calculation-engine version** | Version identifier for IEC 60287 computational behavior used to produce a snapshot. |

`Project` and `Study` are project-management domain entities. The engineering inputs that a study organizes remain engineering-domain models. `Study` is the permanent domain name. `CableStudy` is not used because the product roadmap includes cable analyses beyond ampacity.

## 5. Object ownership and lifecycle

```text
Project
├── project metadata
├── ordered collection of Study objects
│   └── engineering input models for that study
└── project-level notes and persistence state

ProjectController
├── current Project
├── active Study
└── active MainController for that Study
```

Each `Study` owns independent instances of its engineering input models. No mutable `Cable`, `Installation`, `Environment`, `Duct`, or `ConcreteDuctBank` instance may be shared by studies. Duplicating a study creates independent input state and a new UUID.

Projects and studies have immutable UUID identifiers assigned on creation. Display names are editable metadata. No internal reference, persistence link, or business rule may rely on a display name, study order, or list index.

The `project/` package owns the project-management domain: `Project`, `Study`, persistence, serialization, and schema migration. The `models/` package remains reserved for engineering-domain models. The project owns study membership and display order. The study owns its engineering inputs and study-level metadata. A project file path is persistence state managed at the controller/repository boundary; it is not engineering input.

## 6. Required classes and responsibilities

### `project.project.Project`

Owns project identity, metadata, ordered studies, project-level notes, and modification state. It enforces project-level ownership and study identity rules. It has no GUI, file-system, JSON, or calculation-engine duties.

### `project.study.Study`

Owns one study's UUID, name, type, metadata, independent engineering input models, and optional result snapshot metadata. It is the unit of calculation, selection, duplication, persistence, and future reporting.

For `iec_60287_ampacity`, its inputs correspond to existing `Cable`, `Installation`, and `Environment` models, including nested duct and duct-bank data. It does not implement IEC calculations.

### `controllers.main_controller.MainController`

Remains the controller for one active study. Its current public behavior is preserved. It validates GUI-originated study edits, updates existing engineering models, and requests results from the existing engine. It has no project persistence responsibility.

### `controllers.project_controller.ProjectController`

Coordinates project and study lifecycle. It creates projects/studies, selects the active study, duplicates/removes/renames studies, rebuilds the active `MainController` when selection changes, tracks dirty state, and delegates open/save operations to persistence components.

It does not encode JSON, perform direct file I/O, render widgets, or implement engineering equations.

### `project.repository.ProjectRepository`

Owns filesystem persistence only: reads/writes project-document text at supplied paths, checks existence/accessibility, and reports persistence failures. Future deletion is a filesystem operation initiated by `ProjectController` after GUI-level confirmation.

It does not create domain projects, parse/encode JSON, migrate schemas, validate engineering inputs, calculate results, or interact with PySide6.

### `project.serializer.ProjectSerializer`

Owns document-boundary conversion:

```text
Project <-> current-schema dictionary <-> JSON text
```

It performs structural checks required for safe deserialization, such as required members and expected primitive types. It does not perform file I/O, GUI work, lifecycle decisions, business policy, or engineering calculations.

### `project.migrations.ProjectSchemaMigrator`

Transforms raw document dictionaries from supported older schemas into the current schema before domain deserialization. In schema version 1 it recognizes the current schema and rejects unsupported future versions. Its interface exists now; concrete migrations are added only when needed.

### Existing engineering components

`Cable`, `Installation`, `Environment`, `Duct`, `ConcreteDuctBank`, `AmpacityEngine`, and result models retain present responsibilities. They must not know about projects, project files, JSON, or the GUI project manager.

## 7. Public interface contracts

These are public behavioral contracts, not implementation prescriptions. `Project` and `Study` are provided by `project.project` and `project.study`; the existing `models/` package remains the engineering-model package.

| Component | Public operations |
|---|---|
| `Project` | Create with metadata; add, find, remove, and reorder studies by UUID; expose ordered studies; mark/query modified state. |
| `Study` | Create with UUID/name/type; expose owned inputs and metadata; duplicate into an independent study with a new UUID; hold/clear an optional snapshot. |
| `ProjectController` | New project; open; save; save as; create/select/rename/duplicate/delete study; obtain active study/controller; query dirty state. |
| `MainController` | Preserve existing one-study editing and calculation operations. |
| `ProjectRepository` | Read document text; write document text; check path existence/accessibility; future delete. |
| `ProjectSerializer` | Serialize a project to a current-schema dictionary/JSON; deserialize a current-schema dictionary/JSON. |
| `ProjectSchemaMigrator` | Determine compatibility and migrate a raw document dictionary to the current schema. |

Operations that identify a study accept or return its UUID. GUI labels and list positions are presentation concerns resolved by the controller.

## 8. Dependency rules

Allowed direction:

```text
GUI -> ProjectController / MainController -> project domain, engineering models
ProjectController -> project repository, serializer, migrations
MainController -> models, AmpacityEngine
AmpacityEngine -> electrical, thermal, results, engineering models
repository -> filesystem abstraction
project.project / project.study -> engineering models
serializer -> project.project / project.study
migrations -> document dictionaries only
```

Forbidden dependencies:

- Engineering calculation packages importing `project`, controllers, or GUI.
- Engineering models importing the `project` package, persistence, controllers, or PySide6.
- Repository importing engineering models, controllers, GUI, serializer, or migrator.
- Serializer importing GUI, controllers, or calculation packages.
- GUI reading/writing project files or serializing domain models directly.

`ProjectController` is the only Phase 3 component that connects project lifecycle to the active study controller.

## 9. Save and load workflow

### Save / Save As

1. `ProjectController` obtains the current project.
2. It requests a current document from `ProjectSerializer`.
3. It passes JSON text and the selected path to `ProjectRepository`.
4. On confirmed write, it records the path and clears dirty state.

Save As differs only in the selected destination path. Path selection belongs to the GUI; save policy and dirty-state changes belong to the controller.

### Open

1. `ProjectController` requests document text from `ProjectRepository`.
2. `ProjectSerializer` decodes JSON into a raw document dictionary.
3. `ProjectSchemaMigrator` verifies compatibility and transforms it to current schema.
4. `ProjectSerializer` performs structural checks and constructs `Project` and `Study` objects.
5. The controller selects an active study and constructs the corresponding `MainController` and existing `AmpacityEngine`.
6. The controller validates or refreshes result snapshots before presenting results.

Malformed JSON, structurally invalid documents, unsupported schema versions, and inaccessible paths must fail safely. An opening failure must not replace the currently open project.

## 10. Persistence format and result authority

The Phase 3 format is UTF-8 JSON with the `.iecproj` extension. JSON is portable, inspectable during engineering support, deterministic when serialized consistently, easy to version, and suitable for future automation.

Persisted inputs are the sole authoritative engineering state. Result snapshots are optional derived data. A snapshot records at minimum:

- input fingerprint;
- study UUID;
- calculation-engine version;
- applicable calculation standard/version;
- application version;
- calculation timestamp; and
- result values.

On opening, the application rebuilds the engine from inputs. A snapshot is usable only when its fingerprint and relevant versions match the current study context; otherwise it is stale and results are recalculated. A snapshot must never replace a fresh calculation.

Python object serialization and `pickle` are prohibited for project files due to safety, compatibility, and long-term maintainability risks.

## 11. Versioning strategy

Three independent versions are mandatory in every saved document.

| Version | Meaning | Compatibility policy |
|---|---|---|
| **Application version** | Released application build that created or last saved the file. | Informational/diagnostic; it does not alone decide engineering validity. |
| **Schema version** | Project-document structure version. | Authoritative for load compatibility; migrate supported older versions and reject newer unsupported versions. |
| **Calculation-engine version** | Computational behavior used for a snapshot. | Used to determine snapshot validity and engineering reproducibility. |

The applicable IEC standard identifier/version is stored per study. Increment schema version only when persisted structure or meaning changes. A correction that changes calculated output increments calculation-engine version and requires documented engineering validation.

Unknown fields should be preserved during a supported load/save cycle where practical. This supports forward-compatible metadata without weakening schema validation.

## 12. Project and study metadata

### Minimum Version 1 project metadata

- UUID, name, and optional project number;
- client;
- engineer and company;
- revision and document number;
- created and last-modified timestamps; and
- project-level engineering notes.

Optional fields: contract number, consultant, contractor, substation/site name, and project description. All commercial metadata is optional except identity, name, timestamps, and document/schema identity.

Voltage level is study/cable data, not required project metadata, because one project may contain studies at different voltage levels. Every study supports its own notes, description, tags/status, revision metadata, and standard/calculation configuration.

## 13. Frozen architectural decisions

The following are frozen for Phase 3 unless a formally approved ADR supersedes them:

1. The domain class is `Study`, not `CableStudy`.
2. A project contains a flat ordered collection of studies; folders/groups are deferred.
3. Projects and studies use immutable UUIDs; names and order are not identity.
4. A study owns independent mutable engineering input models.
5. `MainController` remains the single-active-study controller with compatible public behavior.
6. `ProjectController` coordinates project/study lifecycle and active-study controller switching.
7. JSON `.iecproj` is the Phase 3 persistence format.
8. Repository, serializer, and migrator have separate filesystem, conversion, and schema-evolution responsibilities.
9. Engineering inputs are authoritative; result snapshots are optional caches.
10. `Project` and `Study` belong to the `project` package; `models` remains reserved for engineering-domain models.
11. No generic study hierarchy is introduced until multiple implemented calculation modules demonstrate a need.
12. Project management remains isolated from electrical, thermal, and calculation-engine packages.

## 14. Extension points

The design supports, without requiring now:

- Additional `study_type` values for pulling tension, bonding, induced voltage, short circuit, derating, HDD, and future IEC/IEEE modules.
- Study grouping, filtering, tags, comparison, and scenario workflows.
- PDF/Excel services consuming a `Study` and fresh results, never GUI widget state.
- Material/cable/installation libraries using references plus captured values for reproducibility.
- Attachments and generated documents through a future container, such as a ZIP package containing `project.json`; controllers and engineering models remain unchanged.
- Revision/audit records, digital approvals, database repositories, cloud sync, and collaboration through extensions to the `project` package or future infrastructure adapters.

Extensions must preserve the ownership, dependency, UUID, source-of-truth, and versioning rules in this ADR.

## 15. Implementation acceptance criteria

Phase 3 is architecturally acceptable only if it demonstrates:

- Save/open round trips preserve project/study identity and all engineering inputs.
- Studies remain independent after duplication and editing.
- Loading reconstructs the active engine from persisted inputs.
- Invalid/incompatible files do not replace the currently open project.
- Results are recalculated when snapshots are missing or stale.
- Existing single-study calculation behavior remains compatible.
- The calculation engine has no dependency on project-management code.
- Every schema evolution includes migration and regression fixtures.

## 16. Change control

This ADR is the Phase 3 design baseline. Changes to frozen decisions require a new ADR or explicit amendment stating motivation, affected compatibility guarantees, migration requirement, validation impact, and rollout plan.
