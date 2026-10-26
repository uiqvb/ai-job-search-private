# RobotControllerApi

![.NET 8](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet&logoColor=white)
![C#](https://img.shields.io/badge/C%23-239120?logo=csharp&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

A hardware-neutral .NET 8 backend that plans and coordinates mobile robots over HTTP.

It was built as the brain for a smart clothesline robot: an Arduino Nano 33 IoT robocar that
tracks the sun while laundry dries and retreats to shade when it starts to rain. The robot
deliberately holds no plan of its own. The API knows nothing about pins, PWM or motors; robots
**poll** it for work and report results back, so the backend owns the modelling, validation,
queuing, history and access control while the firmware stays simple.

> **Status: university project, actively developed.** The architecture and HTTP surface are
> stable, grid movement and offline rollback have been verified end to end on the physical
> robot, and the `deploying` branch runs through a full CI/CD pipeline. See
> [Known gaps](#known-gaps) for what is still missing.

---

## Demo

The robot running against this backend:

[![Watch the demo](https://img.youtube.com/vi/ZW7Ps9AMmc0/hqdefault.jpg)](https://www.youtube.com/watch?v=ZW7Ps9AMmc0)

<https://www.youtube.com/watch?v=ZW7Ps9AMmc0>

Shown at Deakin Open Day: <https://youtu.be/unDSeDkGBI0>

---

## Why it's interesting

**Robots pull, the server never pushes.** Every robot polls a claim endpoint for its next work
item. There is no open socket to drop, so a robot that goes quiet mid-task simply stops asking,
and a background sweep reclaims its work when the lease expires.

**The robot can undo itself with no server at all.** Every claimed command arrives with its own
inverse (`InverseCommandName`, `InversePayloadJson`), so the robot builds a local LIFO undo
stack as it works. If it loses the backend, a watchdog in the firmware fires and the robot
reverses its own recent moves, driving back toward connectivity.

**Nothing is recorded until it is proven.** When the robot reconnects it reports what it
actually executed (`report-offline-rollback`). The backend replays that through simulation
before committing any of it, because a half-applied rollback would otherwise record a position
the robot was never at.

**Rollback by compensating transaction.** For rollbacks requested from the dashboard, the
engine reads the *immutable execution history* (what actually ran, never the original request),
maps each command to its inverse (`MOVE`↔`STEP_BACK`, `LEFT`↔`RIGHT`), reverses the order and
queues the result as new work. Both the dashboard path and the offline path use one
`CompensationBuilder`, so the two cannot drift apart.

**LIFO by construction.** Rollback used to be keyed by workflow id. That is wrong in principle:
position is cumulative and ignores workflow boundaries, so undoing a workflow that is not on top
of the stack produces an off-grid result. Making the offline path LIFO makes that broken case
unrepresentable rather than merely discouraged.

**A grid pose you can't lie about.** The robot's position is a trust state, not a sensor
reading. `PLACE x,y,facing` is the only source of truth. Manual driving, free-running or an
expired in-flight job *invalidates* that trust, which blocks every grid-dependent command until
the next `PLACE`. Each claim is simulated against the current pose before dispatch, so
out-of-bounds moves are rejected before the robot ever moves.

**Three interchangeable persistence layers.** Each bounded context declares a persistence
*interface* (`IDeviceDataAccess`, `IJobDataAccess`, …) with three complete implementations,
selected at startup from a single config value:

| `Persistence:Provider` | Implementation |
| --- | --- |
| `ADO` *(default)* | Hand-written Npgsql / raw SQL |
| `EF` / `EFCORE` | EF Core, `RobotContext` DbContext |
| `REPOSITORY` / `FASTMEMBER` | Generic repository using FastMember |

Changing one string in configuration swaps the entire data layer with no change to any
controller or service.

---

## Architecture

```
HTTP request
  └─ Controller       BoundedContexts/<Ctx>/Controllers/    routing, auth, HTTP status mapping
       └─ Service     BoundedContexts/<Ctx>/Services/       business rules, validation, orchestration
            └─ I<X>DataAccess   BoundedContexts/<Ctx>/Persistence/    interface only
                 └─ implementation   Infrastructure/DataAccess/{ADO,EFCore,Repository}/
                      └─ PostgreSQL
```

Controllers depend on service interfaces; services depend on data-access interfaces. Nothing
above the persistence layer references a concrete database implementation.

The code is organised into 16 bounded contexts rather than by technical layer, plus a `Shared`
kernel:

| Context | Responsibility |
| --- | --- |
| `AppUsers`, `Auth` | Human users, login, password hashing, claims, permission checks |
| `DeviceCredentials` | Robot adapter secrets: issue, revoke, HMAC-SHA256 hashing |
| `DevicePermissions` | Per-user, per-device permission tiers |
| `Devices`, `DeviceCapabilities` | Device records, map assignment, which commands a device supports |
| `CommandCatalogues` | Master command list (`AUTO`, `STOP`, `MOVE`, `PLACE`, …) and each command's inverse |
| `Maps`, `DeviceStatuses` | Grid maps; live status, grid pose, heartbeats |
| `Telemetry` | Sensor ingest, latest/summary, condition classification |
| `Jobs` | One command = one job: create, validate, queue, dispatch to adapters |
| `Workflows` | Ordered multi-step sequences (`BestEffort` vs `AllOrNothing`) |
| `JobHistories`, `WorkflowHistories` | Immutable record of what actually executed |
| `Rollbacks` | Compensating work generated from successful history |
| `LiveControls` | Real-time manual control sessions and segments |

### Authentication

Two custom authentication schemes, hand-rolled rather than using ASP.NET Identity:

- **Basic**, for humans. Backed by `AppUsers` and a multi-algorithm password hash service.
- **DeviceCredential**, for robot adapters. Reads `X-Device-Credential-Id` and
  `X-Device-Credential-Secret`, verifies the hashed secret, checks active / not-revoked /
  not-expired, and enforces that the credential actually owns the `{deviceId}` in the route.

Authorization runs on named policies (`HumanUser`, `DeviceAdapter`, `AdminOnly`) plus a
four-tier per-device permission model, rank-compared: Viewer → Operator → Manager → Owner.
Users with the `Admin` role bypass per-device checks.

---

## Running it locally

**Requirements:** .NET 8 SDK, PostgreSQL 14+.

Configuration comes from
[dotnet user-secrets](https://learn.microsoft.com/aspnet/core/security/app-secrets) or
environment variables. The app fails fast at startup with a clear message if a required key is
missing.

```bash
git clone https://github.com/uiqvb/RobotControllerApi.git
cd RobotControllerApi

dotnet user-secrets set "ConnectionStrings:DefaultConnection" \
  "Host=localhost;Port=5432;Database=robotcontroller;Username=postgres;Password=<your-password>"
dotnet user-secrets set "DeviceCredential:HashKey" "<a-long-random-value>"

dotnet run
```

Apply the schema and reference data from `Infrastructure/DataAccess/Database/` first. Then open
`/swagger` for the API surface, `/` for the built-in dashboard, or `/health` for the health check.

### Configuration keys

| Key | Default | Purpose |
| --- | --- | --- |
| `ConnectionStrings:DefaultConnection` | *required* | PostgreSQL connection string |
| `DeviceCredential:HashKey` | *required* | HMAC key for hashing device secrets |
| `Persistence:Provider` | `ADO` | Which data-access implementation to use |
| `WorkDispatch:LeaseMinutes` | `5` | How long a claimed work item stays leased |
| `WorkDispatch:MaxQueuedWorkItemsPerDevice` | `3` | Queue cap per device; also flood protection |
| `WorkDispatch:StaleExpirySweepSeconds` | `30` | How often the background sweep drains expired leases |

---

## API surface

18 controllers. The main groups:

| Prefix | |
| --- | --- |
| `api/auth`, `api/users` | Registration, login, current user |
| `api/devices`, `api/device-capabilities`, `api/device-status` | Device registry and live state |
| `api/device-credentials`, `api/device-permissions` | Robot secrets and access tiers |
| `api/maps`, `api/command-catalogue` | Grid maps and the command master list |
| `api/jobs`, `api/workflows` | Creating and queuing work |
| `api/adapter/devices/{deviceId}/work-items` | **Robot-facing:** claim next, report started/completed/failed, report offline rollback |
| `api/job-history`, `api/workflow-history` | What actually executed |
| `api/rollback-requests` | Requesting and auditing compensating work |

The core loop:

1. A user creates a job. `JobService` validates device, command, capability and permission,
   then queues it.
2. The robot polls `POST /api/adapter/devices/{deviceId}/work-items/claim-next`. The dispatcher
   walks the oldest queued jobs, simulates each against the current grid pose, and returns the
   first one that is safe to run, with its inverse, marking it claimed with a lease.
3. The robot reports back started, then completed or failed. Results are written to job history
   and the device's pose is updated after a completed grid move.
4. If the robot rolled itself back while offline, it reports that on reconnect through
   `report-offline-rollback`, and the backend replays it before committing.

`FEATURES_README.md` documents the endpoints in more detail.

---

## Build, test and deploy

On the `deploying` branch:

- **Tests:** unit tests for the `CompensationBuilder`, map validation and database
  configuration, plus integration tests against the Maps API. `docker-compose.test.yml` runs
  them against the production image and a throwaway PostgreSQL, so the suite exercises the same
  artefact that later reaches staging and production.
- **Container:** a multi-stage `Dockerfile` on a chiselled Ubuntu base, with a health check that
  runs the app's own `--healthcheck` probe against `/health`.
- **Pipeline:** a seven-stage `Jenkinsfile`: Build, Test, Code Quality, Security, Deploy to
  Staging, Release to Production, Monitoring.
- **Security:** Trivy scans of the built image, with every HIGH or CRITICAL finding either
  remediated or excepted with a review date. See `security-findings.md`.
- **Monitoring:** Prometheus, Grafana, Alertmanager and a blackbox exporter, in `monitoring/`.

---

## Known gaps

Being honest about what isn't done:

- **Test coverage is still modest.** The suite covers rollback compensation, map validation,
  configuration and the Maps API. Dispatch, auth and workflows are not yet covered.
- **No database migrations.** The schema is applied from the SQL scripts in
  `Infrastructure/DataAccess/Database/`; EF Core migrations are not wired up.
- **MQTT is deliberately not used here.** HTTP polling was chosen for simplicity and tolerance of
  connection loss; a push transport is a possible future direction.

---

## Tech

.NET 8 · ASP.NET Core Web API · C# · PostgreSQL · Npgsql · Entity Framework Core · FastMember ·
Swagger / OpenAPI · HMAC-SHA256 · Docker · Jenkins · Trivy · Prometheus · Grafana

## License

See [LICENSE](LICENSE).
