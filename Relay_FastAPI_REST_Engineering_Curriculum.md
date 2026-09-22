# Relay: FastAPI + REST + Backend Engineering
## A competency-based curriculum for associate/junior feature ownership

**Curriculum version:** 1.0 — September 21, 2026  
**Learner:** Dongwook Kim  
**Project status:** Proposed new project; implementation has not been assessed or started here.  
**Scope:** 40 core work packages, 8 optional extensions. A work package can require several teaching sessions and pull requests. These are not 48 tiny endpoint exercises.

## 1. Purpose and target

Build the ability to take a small backend requirement through clarification, implementation, tests, review, deployment, and diagnosis. The goal is not to finish a tutorial or independently operate a large distributed platform. This curriculum's associate/junior target is: **deliver a bounded backend feature with review, understand the code and its failure modes, and know when to ask for help.** Titles vary; this is the course's assessment standard, not an employer-wide definition.

Prior NutriTrack work remains useful: validation, filtering/pagination, tests, and route/service/repository separation have been encountered. They are not automatic evidence of independent proficiency. Demonstrated competencies can be checked off through a challenge rather than retaught. Missing pieces receive targeted instruction rather than restarting the whole course.

The roadmap stays stable. Add a prerequisite only when a concrete gap prevents the next task; explain what gap it addresses and what existing work it replaces or supplements. No unrelated drills merely to manufacture activity. No scheduled tracker or reminders are created by this document.

## 2. Product: a reliable batch-processing API

**User:** someone automating a business workflow who needs to submit a batch, inspect its status, retrieve results, and understand failures.

**Initial workload:** normalize product-catalog records. Trim and uppercase SKUs; collapse whitespace in product names; preserve input order; reject malformed input. Later accept bounded CSV files and add duplicate detection as a separate, specified feature. The workload is deliberately understandable; the engineering challenge is delivering it safely.

**Core product:** authenticated clients submit jobs, list their own history, retrieve results, update allowed metadata, request cancellation, and safely retry job submissions. PostgreSQL stores jobs, results, attempts, and audit events. A separate worker eventually performs processing outside the HTTP request. A Python client is the user interface; Swagger is supplementary. No frontend is required.

**Business scenarios that drive learning:**

- A client loses its response and submits the same request again: prevent duplicate job creation.
- A second user guesses a job ID: do not expose the first user's data.
- A write fails halfway through: do not leave a job without its required related records.
- A worker crashes: retain enough state to diagnose and reconcile it.
- A query becomes slow: reproduce the workload and measure before changing indexes.
- A release breaks the service: identify the deployed version and recover safely.

**Core reliability boundary:** persistent state, atomic job/result updates, bounded retries for classified failures, and documented manual reconciliation of interrupted work. Automatic recovery from worker death, lease expiry, and stale workers belongs to extension R41–R42. Do not claim that the core already guarantees exactly-once processing or automatic crash recovery.

**Architecture choice:** one repository and one modular application, with API and worker entry points sharing domain/application code. PostgreSQL is the initial job store and queue-like table. Do not introduce Redis, Celery, RabbitMQ, Kafka, microservices, or Kubernetes just to increase the stack. Comparing a mature queue library with the educational queue is an extension, not a prerequisite.

## 3. Stack and boundaries

| Concern | Course choice | Why it is present |
|---|---|---|
| Language and dependency management | Python, uv, pyproject.toml, committed lockfile | Reproducible environments and explicit dependencies |
| HTTP application | FastAPI, Pydantic v2, Uvicorn | Typed request/response boundaries and HTTP handling |
| Persistence | PostgreSQL, SQLAlchemy 2.x, Alembic | Real relational constraints, transactions, and controlled schema changes |
| Testing | pytest, FastAPI TestClient, HTTPX | Unit, API, integration, and black-box behavior checks |
| Static checks | Ruff and mypy | Formatting/linting and one type-checking workflow |
| Collaboration | Git, GitHub pull requests, GitHub Actions | Reviewable changes and repeatable integration checks |
| Execution and delivery | Docker, Compose, a Linux staging VM, HTTPS reverse proxy | Process, network, configuration, and deployment ownership |
| Deployment specialization | GCP Compute Engine and Artifact Registry | One concrete cloud path; no multi-cloud survey |
| Operations | Structured logs and a small metrics surface | Evidence for diagnosing behavior |

Pin a supported interpreter and exact resolved dependencies at setup. Use current official documentation rather than copying obsolete version-specific recipes. GCP's deprecated container-on-creation shortcut is not the deployment method: use an ordinary Linux VM with explicitly installed Docker/Compose and documented service startup. Current provider-specific commands are a deployment-ticket concern, not material to memorize now. [S01, S02, S14, S18]

No paid model API, GPU, frontend framework, or new course subscription is required for core development. Before cloud resources are provisioned, inspect current prices, choose a personal spending boundary, document cleanup, and distinguish billing alerts from actual spending enforcement. Cloud resources have not been created by this plan.

## 4. Learning method

Each lesson begins with a concrete request, record, failure, or code path. Trace it before introducing the formal name. Use consistent terminology: HTTP request lifecycle, dependency injection, service layer, repository pattern, unit of work, transaction, invariant, concurrency, idempotency.

The recurring loop is:

```text
Requirement -> concrete example -> small design -> implementation
            -> meaningful tests -> review -> merge -> deploy where relevant
            -> independent reconstruction -> changed requirement
```

A normal teaching session has one central new concept. Larger work packages are split into small sessions without hiding their complete acceptance criteria. Explain new Python syntax just in time: imports, annotations, exceptions, context managers, protocols, generators/yield, decorators, and async/await.

**Assistance levels:** example-guided work is learning; independent implementation allows documentation and ordinary autocomplete but no pasted solution or generated core logic; transfer work changes a meaningful requirement. These are different kinds of evidence, not moral judgments.

**Retrieval:** after a meaningful slice, use a small standalone blank-file or blank-repo exercise. Reconstruct a route/schema/test boundary, repository operation, transaction, or error-mapping function. Do not put entire applications into Anki. Grade behavior, design, tests, explanation, and adaptation—not textual similarity to a reference.

For algorithmic work, define input size and state time, auxiliary memory, output memory, and total memory, including worst-case and expected/amortized qualifications where relevant. For database/network work, also discuss query count, returned rows, payload size, indexes, round trips, concurrency, and measured latency. Big-O alone is not an API performance report.

### Definition of done

A code ticket is done when its acceptance cases work, appropriate tests pass, the diff is understandable, unrelated changes are absent, and the learner can explain the design and one failure case. Update documentation, migrations, configuration, or a runbook when the change requires it. Provide deployment and rollback evidence when the ticket concerns a release. Do not require a meaningless test or diagram for every documentation-only change.

### Review rubric

Score correctness, HTTP contract, data integrity, testing, security, maintainability, and delivery/diagnosis as: **0 = not understood; 1 = substantial guidance needed; 2 = independently implemented with normal review; 3 = independently adapted and defended.** Not every dimension applies to every ticket. No relevant dimension at 0, and no unresolved security/data-loss defect, can pass a milestone. The core graduation target is consistent 2s—not all 3s and not zero questions.

### Collaboration standard

Start from an up-to-date main branch; use a descriptive feature branch; inspect status and diffs; stage deliberately; write coherent commits; push and open a PR; inspect CI; address comments; merge and clean up. Learn conflict resolution, revert, reset, restore, stash, and rebase through actual safe situations. Do not rewrite shared history casually. A solo PR/self-review is useful practice but is not represented as independent teammate approval.

Every PR description states: the problem, scope, behavior, test evidence, compatibility/migration concerns, and rollback or recovery considerations when relevant.

## 5. Curriculum map and effort budget

| Milestone | Packages | Product outcome | Planning hours |
|---|---|---|---:|
| M1. HTTP/FastAPI first slice and engineering loop | R01–R04 | Useful preview API, tests, first reviewed change, baseline CI | 12–18 |
| M2. PostgreSQL and migrations | R05–R08 | Persistent jobs and results, real database tests | 18–26 |
| M3. Architecture and transactions | R09–R12 | Explicit boundaries and atomic business operations | 16–24 |
| M4. REST contracts and client behavior | R13–R16 | Predictable querying, lifecycle rules, errors, and a real client | 16–22 |
| M5. Authentication, authorization, and limits | R17–R20 | Isolated users and a reviewed public-exposure boundary | 16–24 |
| M6. Linux, containers, deployment, and CI/CD | R21–R24 | A reproducibly deployed, recoverable staging service | 20–28 |
| M7. Async and external dependency behavior | R25–R28 | A bounded, tested external integration | 16–24 |
| M8. Workers and durable job processing | R29–R32 | Separate execution, observable attempts, safe submission retries | 24–34 |
| M9. Observability, performance, and incidents | R33–R36 | Measured behavior and tested recovery procedures | 18–26 |
| M10. Independent feature ownership | R37–R40 | Evidence of independent delivery and transfer | 24–34 |
| M11. Advanced reliability (optional) | R41–R44 | Automatic recovery, stale-worker safety, reliable integration events | 30–50 |
| M12. Data/AI extension (optional) | R45–R48 | Bounded files and an evaluated additional processor | 20–40 |

Core total from these ranges: **180–260 focused backend hours**. Optional extensions add **50–90 hours**. These are planning estimates, not measured completion times or promises of employment. Recalibrate after the first four packages.

At three backend hours per weekday, the core budget is about 12–18 weeks. A five-hour total study day can remain three hours backend, 90 minutes DSA/SQL as appropriate, and 30 minutes retrieval/review. Do not silently count all five hours as backend. A five-hour backend-only day corresponds to roughly 7–11 weeks, but does not include a separate DSA workload.

Release checkpoints: M1 working preview; M2 persistent service; M5 authenticated feature-complete synchronous core; M6 deployed service; M8 background execution; M10 independent delivery demonstration. Finishing optional extensions is not a condition for describing the already demonstrated core skills or applying for jobs.

## 6. HTTP and REST thread

FastAPI is the implementation framework; HTTP defines message and method semantics; REST is an architectural style, not a synonym for JSON or CRUD. We will study the REST constraints and then build a practical resource-oriented HTTP API. Document simplifications rather than claiming complete REST conformance from plural endpoint names. [S03, S04]

Teach each concept at its corresponding feature: request/response bytes; method/path/query/header/body; media types and content negotiation; safe versus idempotent methods; representations versus stored rows; status codes; Location headers; partial updates; concurrency preconditions; pagination; private cache behavior; authentication versus authorization; versioning and compatibility; OpenAPI as a contract rather than a guarantee of correctness.

Proposed core surface:

```text
POST   /v1/catalog-previews        # synchronous, non-persistent normalization preview
POST   /v1/jobs                    # create a durable job resource
GET    /v1/jobs                    # owner-scoped history and filters
GET    /v1/jobs/{job_id}            # current representation and lifecycle state
GET    /v1/jobs/{job_id}/result     # available after successful execution
PATCH  /v1/jobs/{job_id}            # allowlisted metadata only
PUT    /v1/jobs/{job_id}/cancellation  # idempotent request for cancellation
GET    /v1/jobs/{job_id}/events     # owner-scoped audit history
GET    /health/live
GET    /health/ready
```

A synchronous preview returns 200. A committed new job resource returns 201 and Location; that status means the job resource exists, not that its work is complete. Its representation explicitly supplies status and a result link. The client must inspect status from the first implementation, even when early small jobs happen to finish synchronously. Compare this with a 202 operation-acceptance contract rather than assuming every background task must use 202. [S03]

Before implementation, document result-not-ready behavior, cancellation races, malformed IDs versus absent resources, validation policy, and whether inaccessible objects appear as 404. No endpoint lets callers write arbitrary lifecycle state. No deletion endpoint is added just to complete a CRUD checklist.

## 7. Architecture thread

Distinguish a **Git repository** (versioned code/history) from a **data repository** (an abstraction over persistence). They are unrelated meanings of the same word.

The runtime path, once the app has earned the layers, is:

```text
HTTP request -> route/dependencies -> service/use case -> repository -> PostgreSQL
                                      |
                                      +-> domain rules / processor
```

Routes handle HTTP concerns. Schemas define external data contracts. Services orchestrate business actions and transaction boundaries. Repositories implement focused reads/writes. Domain functions enforce rules without HTTP knowledge. Database constraints protect storage invariants. A context-managed session is enough to begin; add a named unit-of-work abstraction only when it clarifies transaction ownership. [S05, S06, S07]

Do not create a generic BaseRepository, inheritance tree, or interface for every function. A repository is not compulsory for every SQLAlchemy application; this course uses it when the job operations and testing boundaries give it a concrete purpose. Neither SQLAlchemy rows nor private token fields should accidentally define the public response shape.

Illustrative later structure—not a day-one folder creation task:

```text
relay/
  pyproject.toml
  uv.lock
  README.md
  .env.example
  src/relay/
    main.py
    api/              # routes, schemas, dependencies, HTTP error mapping
    domain/           # job rules and normalization
    services/         # use cases and transaction orchestration
    repositories/     # persistence operations
    db/               # SQLAlchemy mappings and session construction
    integrations/     # external supplier/model clients
    worker/           # process entry point and execution loop
    core/             # configuration and logging setup
  migrations/
  tests/
    unit/
    integration/
    api/
    e2e/
  docs/
    decisions/
    runbooks/
  .github/workflows/
  Dockerfile
  compose.yaml
```

## 8. Work packages

Each package assumes the preceding core work unless a different dependency is stated. The tests below identify important evidence, not a mandatory implementation or an exhaustive test count. Advance only after reviewing the corresponding milestone gate.

### M1 — First useful slice and engineering loop

#### R01 — A fresh repository with a useful FastAPI endpoint

**Implement:** Create a reproducible packaged Python project, a small FastAPI application, a typed catalog-normalization preview, and focused unit/API tests. Keep the initial structure small. Use a feature branch and commit deliberately. The complete first assignment is specified later in this document.

**Acceptance evidence:** A clean environment can install the project and run the endpoint and tests. A curl request and an API test agree about the response. Normalization does not mutate the input. No database or worker is required.

**Explain:** Trace JSON bytes into validated objects, through a pure function, and back into a response. Explain why this preview returns 200 rather than 201.

**Primary references:** S01, S02, S03, S09.

#### R02 — Read and control the HTTP contract

**Implement:** Exercise method, path, query, headers, media type, and body independently. Add documented limits and validation policy. Inspect actual success and failure responses with curl -i, not only Swagger. Treat omitted, null, empty, and wrong-type input as distinct cases.

**Acceptance evidence:** Tests cover missing fields, blank normalized fields, unknown fields, wrong types, and bounds. A wrong method and an unknown route are distinguished. A short request/response transcript identifies the relevant components.

**Explain:** Which behavior is our policy, which is an HTTP semantic, and which is a framework default we have chosen to keep?

**Primary references:** S02, S03, S10.

#### R03 — Tests that establish behavior rather than mirror implementation

**Implement:** Introduce parametrized cases, fixtures with explicit scope, input immutability checks, and a narrow integration boundary. Deliberately remove or break a rule and confirm a meaningful test fails. Reconstruct the small preview independently after guided practice.

**Acceptance evidence:** Tests have isolated inputs and do not depend on execution order. Assertions cover actual transformations and error details worth promising. The reconstruction is labelled independent or assisted honestly.

**Explain:** What bug would each important test detect? Which tests would survive a refactor to a different internal function layout?

**Primary references:** S09.

#### R04 — First pull request and baseline CI

**Implement:** Create a GitHub PR with behavior and test evidence. Add a Python CI job that installs locked dependencies, runs tests, Ruff, and the chosen type checker. Learn the local/remote branch relationship while reviewing the diff. Practice a safe small merge conflict in a disposable branch.

**Acceptance evidence:** A failing test causes CI failure; a correction restores it. The PR contains only relevant files. Secrets and generated environments are absent. Document solo self-review separately from external review.

**Explain:** What is the difference between main, origin/main, HEAD, a local commit, and a merged PR? Why is a green badge not a complete review?

**Primary references:** S11, S12.

### M2 — Real persistence early

#### R05 — Design the first PostgreSQL schema in SQL

**Implement:** Run PostgreSQL using development Compose. Model jobs and results with UUIDs, timestamps, a constrained status, and explicit relationships. Write representative INSERT/SELECT statements yourself before introducing ORM convenience. Use a development-only identity until the auth milestone.

**Acceptance evidence:** Primary/foreign keys and relevant NOT NULL or CHECK constraints reject invalid data. Explain the generated identifiers and timezone policy. Data survives a database container restart with its persistent volume intact.

**Explain:** Which guarantees belong in the database, and why is an application-side check insufficient as the sole protection?

**Primary references:** S08, S13.

#### R06 — Persist and retrieve complete jobs with SQLAlchemy

**Implement:** Use SQLAlchemy 2.x and request-scoped sessions for job creation and lookup. Small batches may execute synchronously initially. Store the original request specification and result, and expose separate response schemas. Clients already treat job status as explicit rather than assuming completion.

**Acceptance evidence:** Create a job, restart the API, and retrieve it and its result. A fresh API process sees the same durable data. Invalid identifiers and valid-but-absent identifiers follow the documented policy. No module-global mutable session is used.

**Explain:** Explain engine, connection, session, transaction, flush, commit, rollback, and refresh using this request.

**Primary references:** S07.

#### R07 — Migrate an existing database without throwing it away

**Implement:** Introduce Alembic. Create the initial migration and then evolve a populated schema with a new field. Inspect generated migration code and implement any required backfill before a restrictive constraint. Keep create_all out of the production schema-management path.

**Acceptance evidence:** Both an empty database and an earlier populated schema reach the target revision. Existing rows retain their meaning. A test verifies the backfill. The release notes say whether downgrade is safe or a forward repair is required.

**Explain:** Why is changing a Python model not enough? What could an autogenerated migration miss or destroy?

**Primary references:** S08.

#### R08 — Real-database integration tests in CI

**Implement:** Separate fast unit tests from PostgreSQL-backed API/repository tests. Use an isolated test database and explicit cleanup. CI provisions PostgreSQL, applies migrations, and runs the appropriate suite. Add safeguards against accidentally pointing destructive test setup at non-test data.

**Acceptance evidence:** Constraints, transaction failure, and persistence are tested against PostgreSQL rather than inferred from a fake or SQLite. Tests can run repeatedly without leftovers. The test command and service startup are documented.

**Explain:** Which claim can a fake repository prove, and which claim requires the actual database?

**Primary references:** S07, S09, S11.

### M3 — Architecture and atomic business operations

#### R09 — Extract a service layer for a real use case

**Implement:** Move job-submission orchestration out of routes while preserving HTTP behavior. Keep normalization rules framework-independent. Use meaningful input/output types and domain exceptions, and translate those exceptions at the HTTP boundary.

**Acceptance evidence:** Existing API tests pass unchanged where the public contract is unchanged. The same normalization or submission rule is callable outside HTTP. Services do not raise FastAPI HTTPException.

**Explain:** For one line in each layer, explain why it belongs there rather than in a neighboring layer.

**Primary references:** S05, S06.

#### R10 — A focused repository and explicit dependency injection

**Implement:** Introduce only the persistence operations the service needs. Wire concrete repositories and sessions through FastAPI dependencies. Use a protocol only when there is an actual substitutable boundary. Demonstrate dependency overrides without leaking them between tests.

**Acceptance evidence:** A service test uses a simple test double; a repository integration test exercises the real implementation. No generic all-purpose repository API or unnecessary base class is introduced. Resource cleanup is demonstrated on success and error.

**Explain:** How is passing a dependency explicitly different from importing a mutable global? What does yield clean up?

**Primary references:** S05, S07, S19.

#### R11 — One transaction for one business action

**Implement:** Persist a job and its required related state, such as an audit event, atomically. Place commit ownership in the use-case transaction rather than hiding commits inside each repository method. Keep external network work outside a database lock-holding transaction.

**Acceptance evidence:** Force the second write to fail. The first write must not remain committed. Demonstrate the session recovery/rollback path and verify the next independent operation can succeed.

**Explain:** What precisely is the invariant? At what point is it safe to acknowledge durable creation to the client?

**Primary references:** S05, S07, S13.

#### R12 — Architecture transfer check

**Implement:** Add a small command-line entry point that invokes an existing business use case without going through the HTTP route. Refactor an awkward boundary only when this exposes a real dependency problem. Record a short decision note about the chosen layer boundaries.

**Acceptance evidence:** The CLI and API share the business rule, not duplicated logic. Repository contract expectations agree for the fake and real implementations, while DB-specific behavior remains in DB tests.

**Explain:** What did the extra abstraction buy? What complexity did it add? What would you remove in a smaller application?

**Primary references:** S05, S06.

### M4 — HTTP contracts clients can rely on

#### R13 — Stable querying and pagination

**Implement:** Add owner-ready filtering, bounded page size, explicit sorting, and offset pagination. Use a unique tie-breaker such as created_at plus id. Then implement or demonstrate a keyset/cursor query when concurrent insertions reveal offset limitations. Push filtering and limits into SQL.

**Acceptance evidence:** Boundary, empty-result, tied-timestamp, and consecutive-page tests exist. Explain what changes when records are inserted between requests. Cursor input is validated and does not grant authorization or replace owner filtering.

**Explain:** Why is deterministic ordering necessary, and why does it not turn offset pagination into a snapshot?

**Primary references:** S13.

#### R14 — Lifecycle rules and controlled mutation

**Implement:** Specify queued, running, succeeded, failed, and cancelled as a state transition table. Add allowlisted metadata updates, never arbitrary client-written status. Define cancellation intent now, even though worker-aware cancellation arrives later. Distinguish a rejected request from a successfully executed validation report.

**Acceptance evidence:** Illegal transitions are rejected in domain tests. Missing fields and explicit null in PATCH have documented meanings. Server-owned fields cannot be changed by adding JSON properties.

**Explain:** Why is a job state machine different from a bag of editable database columns?

**Primary references:** S03, S10.

#### R15 — Consistent errors and a usable OpenAPI contract

**Implement:** Define a stable error envelope with a machine-readable code, useful message, and request identifier once available. Document success/error responses and examples. Preserve useful validation information without leaking exceptions or SQL. Choose 404, 409, and 422 based on the actual condition.

**Acceptance evidence:** A client can distinguish an invalid request, absent resource, forbidden action policy, and invalid state. Public schemas omit internal fields. An API test checks key OpenAPI contract details without snapshotting irrelevant generated ordering.

**Explain:** What information is safe for a user, what belongs only in internal logs, and what must remain stable for callers?

**Primary references:** S02, S03, S15.

#### R16 — A real client and optimistic concurrency

**Implement:** Write an HTTPX client that creates a job, follows its Location/status, and retrieves results. Add version-based conditional metadata updates and demonstrate stale-write rejection with an ETag/If-Match contract. Study safe/idempotent methods and private caching with concrete requests.

**Acceptance evidence:** Two clients reading the same version cannot silently overwrite each other. A stale precondition receives the specified 412 behavior. The client handles non-success responses and timeouts without parsing every body as a success model.

**Explain:** Does idempotent mean the same response bytes? Why does a committed 201 job resource not imply finished processing?

**Primary references:** S03, S20.

### M5 — Security belongs to the feature

#### R17 — Authenticate machine-to-machine clients

**Implement:** Use independently provisioned demo accounts and high-entropy API keys for this service. Store a safe verifier rather than recoverable raw keys; support key identifiers, rotation, revocation, and expiry policy. Use established cryptographic primitives. Study password hashing, sessions, JWTs, OAuth, and OIDC as distinct concepts without building an identity provider.

**Acceptance evidence:** Missing, invalid, expired, and revoked credentials are tested. Responses and logs never expose raw credentials or verifiers. Development identity shortcuts cannot be enabled accidentally in deployed configuration.

**Explain:** Why does this service use API keys? How would a browser login change the design? Why is JWT verification not merely decoding?

**Primary references:** S15, S16, S17.

#### R18 — Authorize every object and collection

**Implement:** Bind the authenticated principal to every job, result, event, update, and cancellation query. Apply least privilege to administrative operations. Decide whether inaccessible objects appear as 404. Build a table of permitted operations by principal type.

**Acceptance evidence:** User B cannot read, modify, cancel, or infer User A’s data through direct IDs, list filters, cursors, results, or events. Forged owner IDs in requests are rejected or ignored according to the specified contract.

**Explain:** Why is authentication insufficient? Where must ownership be checked when the resource is nested?

**Primary references:** S15, S16.

#### R19 — Bound resource consumption

**Implement:** Set explicit body, record-count, field-length, page-size, and request-duration boundaries. Add a simple documented per-principal submission/quota limit appropriate to the deployment topology. Distinguish edge request-rate limits from atomic business quotas. Return useful rejection information without retry storms.

**Acceptance evidence:** Oversized and excessive requests are rejected predictably. Quota tests include a concurrent boundary case when the quota is enforced in PostgreSQL. The design states whether a limiter is local to one process or shared.

**Explain:** Which resource are we protecting: memory, CPU, database connections, queue capacity, or an external bill?

**Primary references:** S15.

#### R20 — Security regression suite and exposure review

**Implement:** Review secret handling, exception output, dependency versions, input boundaries, HTTPS assumptions, token transport, database permissions, and browser-origin policy. Learn that CORS is not server authorization; cover CSRF when discussing cookie-based browser alternatives. Keep synthetic data only.

**Acceptance evidence:** Run an authorization matrix, credential-leak checks, and invalid-input tests. No public deployment occurs with the development-auth bypass or an exposed database port. Record remaining limitations rather than labeling the app unconditionally secure.

**Explain:** Describe one threat, the relevant trust boundary, the control, the test, and a remaining risk.

**Primary references:** S15, S16.

### M6 — Ship and recover a service

#### R21 — Build a production-shaped container

**Implement:** Create a small reproducible application image with locked dependencies, an intentional build context, an unprivileged runtime user, and no embedded secrets. Run the application without a development reloader. Understand images, containers, layers, environment variables, and process exit.

**Acceptance evidence:** Build from a clean checkout and run the API without the local virtual environment. Confirm only intended files are in the image. Explain how the chosen image platform works on the learner’s Apple Silicon laptop and the deployment host.

**Explain:** What is stored in the image, and what is supplied only at runtime? What does stopping the main process do?

**Primary references:** S14.

#### R22 — Compose, Linux, and network diagnosis

**Implement:** Run API and PostgreSQL as a documented stack. Distinguish container DNS names, localhost, exposed versus published ports, volumes, and bind mounts. Diagnose a bad port, missing environment variable, and permission failure using shell commands, logs, and exit codes. Introduce liveness/readiness checks.

**Acceptance evidence:** Data survives normal application/container replacement. Restarting the API does not require resetting the database. A deliberately broken service connection is diagnosed from evidence, not guessed through random edits.

**Explain:** Trace an external request to the listening process, and a database connection from the API to PostgreSQL.

**Primary references:** S14, S18.

#### R23 — Deploy a secured staging release manually

**Implement:** Use one Linux VM on GCP and Artifact Registry, with explicit Docker/Compose startup and an HTTPS reverse proxy. Keep the database off the public network. Configure narrow access, runtime secrets, persistent storage, and restart behavior. Review costs and cleanup before creating resources.

**Acceptance evidence:** From outside the laptop, a client can call the authenticated API over HTTPS. Deployed version/configuration are identifiable. A runbook covers startup, logs, smoke tests, backups, and resource removal. This is a single-host teaching deployment, not high availability.

**Explain:** Which failures are hidden by the local environment? What happens to data if the VM’s storage is lost?

**Primary references:** S14, S18.

#### R24 — Turn the proven release procedure into CI/CD

**Implement:** Automate tests, image build, immutable artifact publication, controlled migration, staging deployment, and smoke checks. Promote the tested artifact rather than rebuilding it. Use least-privilege workflow permissions, pinned third-party actions, and short-lived cloud credentials through OIDC where supported. Separate untrusted PR tests from trusted deployment.

**Acceptance evidence:** A failing test or smoke check blocks promotion. Deploy a new version and recover the previous application version. Show why reverting an image does not automatically reverse a destructive schema change. Prevent overlapping migration/deployment jobs.

**Explain:** Which identity can deploy? What code can access deployment credentials? What does the rollback procedure actually restore?

**Primary references:** S11, S12, S21.

### M7 — Concurrency and external dependencies

#### R25 — Explain sync and async using a measured request

**Implement:** Trace synchronous calls, thread-pool handling, the event loop, awaiting I/O, and CPU-bound work. Compare a deliberately blocking handler with a correctly structured I/O path under controlled concurrent requests. Do not convert every function to async as a style change.

**Acceptance evidence:** Explain which operation is waiting and which is consuming CPU. Demonstrate the blocking effect with a reproducible small experiment and record the environment. Choose a synchronous or asynchronous path for a stated workload.

**Explain:** Why does async def not make synchronous I/O nonblocking? Why does await not make CPU-heavy Python work run in parallel?

**Primary references:** S22.

#### R26 — Add a supplier lookup through an explicit HTTP client boundary

**Implement:** Build a local deterministic supplier test server and an adapter with typed request/response contracts. Use HTTPX with explicit connect/read/write/pool timeout choices. Map transport errors, upstream failure statuses, malformed responses, and legitimate empty results separately.

**Acceptance evidence:** Integration tests exercise a real local HTTP boundary without paid services or public-internet dependencies. The app does not treat a timeout as proof that the upstream performed no work.

**Explain:** Which failure is safe to retry? Which requires inspecting operation semantics or an idempotency guarantee?

**Primary references:** S20, S23.

#### R27 — Bound async work and manage its lifetime

**Implement:** Use AsyncClient in a bounded enrichment path with application-lifetime cleanup and concurrency limits. Keep synchronous database calls off that event loop; migrate a bounded path completely or keep it explicitly synchronous. Demonstrate per-task AsyncSession ownership where async persistence is used.

**Acceptance evidence:** Tests cover cleanup and cancellation, maximum concurrent upstream requests, and an unavailable dependency. No session is shared concurrently across tasks, and no client is recreated needlessly inside a hot request loop.

**Explain:** Who creates and closes the client/session? What happens to resources when an exception or cancellation interrupts the path?

**Primary references:** S07, S19, S23.

#### R28 — Dependency resilience without hiding failures

**Implement:** Add bounded retries with backoff and jitter only for appropriate operations, an overall elapsed-time budget, and clear error classification. Use deterministic clocks or controlled waits for tests. Keep external calls outside long database transactions and record dependency failures without secrets.

**Acceptance evidence:** A permanently invalid response is not retried indefinitely. A temporary failure can recover within the budget. Client cancellation and deadline expiry do not leak resources. Record why the chosen retry count and limit fit this small workload.

**Explain:** How can retries amplify an outage? What is the difference between a request timeout and an end-to-end deadline?

**Primary references:** S20, S23.

### M8 — Real background execution

#### R29 — Separate accepting work from executing it

**Implement:** Change the job service so submission commits a queued job and a separate worker entry point processes it. Reuse the domain/service code rather than importing a route. Return the durable job resource promptly; clients poll the status/result contract already established. Compare this with in-process BackgroundTasks.

**Acceptance evidence:** A submitted job persists when the API process stops. Starting the worker processes eligible jobs. A result is visible only according to the documented state contract. Killing the API does not erase accepted work.

**Explain:** Which process owns the job now? Why is an in-process post-response callback not a durable execution guarantee?

**Primary references:** S24, S25.

#### R30 — Claim work atomically and commit results consistently

**Implement:** Use PostgreSQL row locking and a queue-like claim query, such as FOR UPDATE SKIP LOCKED, inside a short transaction. Commit the claim before processing. Persist result and final state atomically, with guards against invalid state changes. Understand that SKIP LOCKED is not a general-purpose consistent read.

**Acceptance evidence:** Two healthy concurrent workers do not claim the same queued attempt. A failure in final-state persistence cannot expose a partially committed result. No database lock is held throughout an external HTTP call.

**Explain:** When is a claim visible to another worker? Which failure window remains after the claim is committed?

**Primary references:** S07, S13.

#### R31 — Attempts, retries, and explicit crash limitations

**Implement:** Record each attempt, error classification, retry schedule, and maximum attempts. Retry known transient failures of this idempotent local workload. Record terminal failures. Provide a manual reconciliation command/runbook for interrupted work after confirming the previous worker is stopped; do not pretend this is automatic lease recovery.

**Acceptance evidence:** A permanent input/domain error is not retried. A retryable failure respects backoff and attempt limits. After a killed worker, an operator can identify interrupted jobs and recover safely under the stated single-operator assumptions.

**Explain:** What is guaranteed by the core, what is manual, and what will the lease extension add?

**Primary references:** S13, S24.

#### R32 — Submission idempotency and cancellation races

**Implement:** Implement principal-scoped idempotency keys with a database uniqueness constraint, a canonical request fingerprint, and a documented retention/replay policy. Add an idempotent cancellation request and cooperative worker checks. Use guarded transitions so a stale operation cannot silently overwrite terminal cancellation.

**Acceptance evidence:** Concurrent equivalent submissions yield one job. Reusing a key with different semantics conflicts. Cancellation before claim, during work, and after completion has defined behavior. A database failure does not commit a dangling key without its corresponding job.

**Explain:** Which side effect is deduplicated? Why does this not prove exactly-once execution of arbitrary external effects?

**Primary references:** S03, S07, S13.

### M9 — Operate with evidence

#### R33 — Structured logging and request/job correlation

**Implement:** Add request identifiers, job/attempt identifiers, event names, durations, and exception context where needed. Configure logging centrally. Distinguish audit events from diagnostic logs. Redact secrets and avoid logging full catalog payloads by default.

**Acceptance evidence:** Trace one client request to the stored job and worker attempt. Reproduce a failure and locate useful evidence. Confirm credentials and private fields are absent from captured logs.

**Explain:** What question does each field answer, and why is printing everything not observability?

**Primary references:** S15.

#### R34 — Health, metrics, and a small service objective

**Implement:** Separate process liveness from readiness to serve relevant traffic. Measure request latency/error rate and job completion time, queue depth/age, and failure counts. Avoid unbounded metric labels such as job IDs. Write a modest service objective tied to a specified test workload.

**Acceptance evidence:** A database outage affects readiness appropriately without creating an automatic restart storm by design. Metrics distinguish an idle healthy worker from a growing unprocessed queue. Any stated objective is marked proposed until measured.

**Explain:** Why can HTTP latency look excellent while users wait indefinitely for jobs?

**Primary references:** S18.

#### R35 — Find one real bottleneck

**Implement:** Seed a reproducible dataset, exercise list/lookup/claim queries, inspect EXPLAIN plans, and add a justified index. Measure query counts, latency percentiles, memory, and throughput under a stated concurrency level. Discuss connection-pool limits and bounded payloads before adding caching.

**Acceptance evidence:** Keep before/after measurements with hardware, row counts, concurrency, and workload details. Show the query plan and explain index maintenance/storage tradeoffs. No invented production-scale claim appears in the README.

**Explain:** What does the measurement establish, and which conclusions would require a different test environment?

**Primary references:** S07, S13.

#### R36 — Incident diagnosis and restore rehearsal

**Implement:** Reproduce failures in this actual service: unavailable database, invalid runtime config, broken dependency, killed worker, or a failed deployment. Write a short incident note with symptom, evidence, cause, fix, and prevention. Back up the database and restore it to a separate instance.

**Acceptance evidence:** The restored instance serves known jobs/results and the relevant schema revision. Logs and tests support the root-cause claim. Measure the rehearsal’s recovery time without presenting it as a production guarantee.

**Explain:** What is the difference between having a backup file and proving a usable restore? What data could still be lost?

**Primary references:** S07, S18.

### M10 — Demonstrate independent feature ownership

#### R37 — An unseen bounded feature

**Implement:** Receive a new requirement without an implementation recipe: for example a job label with filtering, a new result-summary field, or a retention rule. Clarify ambiguities, propose the API/schema change, implement it, and add tests using documentation but no generated core solution.

**Acceptance evidence:** Deliver a focused PR, a clean migration when needed, boundary tests, and an explanation of tradeoffs. Record assistance honestly. The exact graduation prompt should be chosen at assessment time rather than memorized from these examples.

**Explain:** Which assumptions did you identify before coding, and how did they affect the acceptance tests?

**Primary references:** S03, S08.

#### R38 — Diagnose an unfamiliar regression

**Implement:** Investigate a seeded defect in an existing layer without being told the line to change. Use a minimal reproduction, traceback/logs, and a failing regression test. Fix the cause rather than adjusting expected output to match the bug.

**Acceptance evidence:** The report distinguishes observations from hypotheses. The regression test fails before the fix and passes after it. An adjacent edge case is considered, and unrelated rewrites are avoided.

**Explain:** What evidence ruled out your first plausible but incorrect explanation?

**Primary references:** S09.

#### R39 — Deploy a compatible change and rehearse recovery

**Implement:** Ship a small schema/API evolution using an expand-then-contract approach where appropriate. Verify the previous client and the new client. Deploy the tested artifact, observe it, and exercise rollback or forward repair according to the migration’s actual compatibility.

**Acceptance evidence:** Show old/new client behavior, migration evidence, smoke tests, version identification, and an honest recovery procedure. Do not automatically downgrade a database just because application code is reverted.

**Explain:** What is the compatibility window, and at what point does removing the old field become safe?

**Primary references:** S03, S08, S21.

#### R40 — Final ownership and transfer demonstration

**Implement:** From a fresh checkout, set up, test, and run the service using the README. Demonstrate authenticated submit/result flow, rejected cross-user access, a controlled failure, and a recovery. Rebuild one small related API slice in a new blank project with a meaningfully changed domain requirement.

**Acceptance evidence:** Present reviewed code, tests, OpenAPI examples, decision notes, deployment evidence, measured performance notes, an incident note, and restore evidence. List limitations and distinguish guided features from independent ones.

**Explain:** Which backend responsibilities can you now perform with normal review, and which still need closer supervision?

**Primary references:** S01–S25 as relevant.

### M11 — Optional advanced reliability

#### R41 — Leases, heartbeat, and stale-worker fencing

**Implement:** Add expiring claims, renewal, attempt/version tokens, and bounded recovery after worker death. Guard completion writes with the current claim token so an old worker cannot overwrite newer work. Keep database transactions short.

**Acceptance evidence:** A dead worker’s job eventually becomes eligible under the documented policy. A delayed old worker cannot commit a result for a newer attempt. Duplicate computation may occur; durable result state remains guarded.

**Explain:** Why does lease expiry not prove that the old worker has stopped running?

**Primary references:** S07, S13.

#### R42 — Test the failure windows deterministically

**Implement:** Exercise crashes before claim commit, after claim commit, before result commit, and after result commit. Add synchronized concurrent tests for lease expiry, stale completion, and cancellation races. Document the exact execution and visibility guarantees.

**Acceptance evidence:** Tests use barriers/controlled clocks rather than fragile sleeps where practical. No exactly-once external-effect claim is made without a corresponding protocol and evidence. Retry safety is described per operation.

**Explain:** Where can work happen twice, and where is the observable state constrained to one valid outcome?

**Primary references:** S07, S13.

#### R43 — A transactional outbox for completion events

**Implement:** Introduce an external completion event as a real requirement. Store the event alongside the state change in one transaction, then deliver it separately. Implement receiver-side deduplication and keep delivery attempts visible. Compare this with adopting a mature task queue rather than claiming the educational queue is universally preferable.

**Acceptance evidence:** A committed completion cannot silently lack its required outbox record. Redelivery is harmless at the demonstrated receiver. Failures between send and acknowledgement do not justify pretending delivery occurred exactly once.

**Explain:** Which dual-write problem did the outbox solve, and which delivery problems remain?

**Primary references:** S07, S13.

#### R44 — Signed callbacks with a constrained destination policy

**Implement:** Deliver completion webhooks to a controlled HTTPS receiver with established HMAC/signature primitives, timestamps, replay handling, and retries. Use an allowlisted training destination. Treat arbitrary callback URLs as an SSRF design problem requiring separate review, including redirects and address resolution.

**Acceptance evidence:** Tampered, stale, and duplicate messages are handled as specified. Failures are visible and bounded. The feature cannot be used to probe arbitrary internal/metadata endpoints under its stated allowlist policy.

**Explain:** Why does signing a webhook protect integrity but not make an arbitrary destination safe?

**Primary references:** S15, S16.

### M12 — Optional data and AI integration

#### R45 — Bounded CSV input and result download

**Implement:** Accept a bounded CSV file with explicit encoding, header, row-count, field-size, and parsing rules. Define partial row errors versus whole-request rejection before coding. Stream or spool where justified, keep filenames untrusted, and define storage cleanup. Preserve the JSON workflow.

**Acceptance evidence:** Malformed files, oversized fields, wrong headers, and quoted/newline cases are tested. Memory behavior is measured for the allowed input bound. Download and retention endpoints enforce the same ownership rules as job metadata.

**Explain:** Which limits must be checked before loading the full file into memory?

**Primary references:** S15, S20.

#### R46 — Add a second processor through a narrow interface

**Implement:** Register a new deterministic processor with an explicit input/output schema and a version. Avoid user-provided executable code and arbitrary dynamic imports. Keep operation-specific validation distinct from generic job lifecycle handling.

**Acceptance evidence:** The new processor does not require copying an HTTP route or worker loop. Unknown processor versions are rejected predictably. Existing jobs remain interpretable after a new processor version is introduced.

**Explain:** What should be common infrastructure, and what would a forced generic abstraction make harder to understand?

**Primary references:** S05, S06.

#### R47 — Integrate an AI/extraction provider without obscuring engineering

**Implement:** Replace the new processor’s stub with a tightly bounded provider adapter only after deterministic tests work. Treat provider output as untrusted data; validate the schema, record model/configuration version, enforce time/cost/input limits, and avoid executing returned instructions or code. Use mock responses for normal tests.

**Acceptance evidence:** Malformed outputs, timeouts, rate limits, and refusal/empty-output cases have defined behavior. Secrets are not logged. Retries and job replays have explicit cost implications and do not promise provider-side exactly-once execution.

**Explain:** What is an application/retrieval failure, what is a provider failure, and what is a model-quality failure?

**Primary references:** S15, S20, S23.

#### R48 — Evaluate quality and operational tradeoffs

**Implement:** Create a small held-out input set and a simple baseline. Measure schema-validity rate, task-specific correctness, latency, failure rate, and cost where applicable. Keep versions and test conditions explicit. Write a decision on whether the added provider improves the user’s actual workflow.

**Acceptance evidence:** Report observed results, not anticipated numbers. Identify examples where the baseline is sufficient and where the provider fails. Demonstrate that a provider change can be tested and reverted without rebuilding the job platform.

**Explain:** Does the feature provide enough value to justify its cost, latency, privacy exposure, and failure modes?

**Primary references:** S20, S23.

## 9. Milestone gates

| Gate | Independent demonstration |
|---|---|
| M1 | Build a small changed request/schema/response feature and tests; explain the actual HTTP exchange and Git diff. |
| M2 | Create and retrieve a record across process restart; migrate a populated database without recreating it. |
| M3 | Cause the second write of a business action to fail and show atomic rollback; explain every boundary. |
| M4 | Implement a changed query/update contract and make the client respond correctly to errors and stale state. |
| M5 | Run two identities through the permission matrix and prove isolation across every relevant surface. |
| M6 | Reproduce a deployment and recover the prior app version using documented commands and compatible data. |
| M7 | Diagnose a blocking/timeout scenario and implement a bounded external call with reliable cleanup. |
| M8 | Show durable submission, separate execution, duplicate-submission handling, cancellation, and the stated crash-recovery limitations. |
| M9 | Reproduce one incident, justify a performance change with measurements, and restore a usable database. |
| M10 | Deliver an unseen feature and explain it end to end without a reference implementation. |

Failure at a gate means targeted remediation and a different reassessment example. It does not mean erasing prior progress, delaying unrelated competencies indefinitely, or pretending assisted completion was independent.

## 10. First assignment in full: R01

### Objective

Create the first useful, tested FastAPI slice in a new `relay` repository. This is a baseline exercise that reuses prior validation/testing exposure while establishing a stronger engineering workflow. It is intentionally not a database, authentication, or async lesson yet.

### Behavior

`POST /v1/catalog-previews`

Input:

```json
{
  "records": [
    {"sku": " ab-12 ", "name": "  Brake   pad  "},
    {"sku": "xy-9", "name": "Oil filter"}
  ]
}
```

Expected status: `200 OK`.

Expected JSON:

```json
{
  "records": [
    {"sku": "AB-12", "name": "Brake pad"},
    {"sku": "XY-9", "name": "Oil filter"}
  ],
  "count": 2
}
```

Rules: trim outer SKU whitespace and uppercase the SKU; collapse all runs of whitespace in the name to one space and remove outer whitespace; preserve record order; preserve duplicate records for this first slice; return a new result without mutating the caller’s input. This preview does not persist a job or a report.

### Input policy

The top-level object has only `records`. The list has 1–100 records. Each record has exactly the string fields `sku` and `name`; do not silently convert a number into a string. After normalization, SKU length is 1–64 characters and name length is 1–200 characters. Blank normalized values and unknown fields are rejected. For this assignment, well-formed JSON that violates this schema returns the documented FastAPI validation response with status 422. API-wide malformed-JSON/content-type policy is explicitly studied in R02; do not assume all framework defaults are HTTP mandates.

### Small initial layout

```text
relay/
  pyproject.toml
  uv.lock
  README.md
  .gitignore
  src/relay/
    __init__.py
    main.py
    schemas.py
    normalization.py
  tests/
    test_normalization.py
    test_catalog_previews.py
```

Use the packaged-project setup so `relay` is importable without modifying `sys.path`. Explain the purpose of each initial file. Do not create repositories, services, migrations, workers, or configuration factories prematurely.

### Suggested sequence

Start with an environment and Git baseline, then define the input/output examples. Write the pure transformation and its tests. Add schemas and the route. Add API validation tests. Exercise the endpoint with curl and read the response headers. Inspect the diff and commit. The first PR can remain open while R02–R04 add the contract checks and CI; do not force a complex remote workflow before understanding local Git.

Example run commands, after the package and dependencies are configured:

```bash
uv sync --locked
uv run uvicorn relay.main:app --reload
# In another terminal:
uv run pytest -q
```

Example request:

```bash
curl -i -X POST http://127.0.0.1:8000/v1/catalog-previews \
  -H 'Content-Type: application/json' \
  -d '{"records":[{"sku":" ab-12 ","name":"  Brake   pad  "}]}'
```

### Test evidence

Check the exact transformation, order preservation, input immutability, and count. Check blank fields after normalization, missing fields, unknown fields, wrong types, an empty list, and 101 records. Parametrize related cases instead of copying large tests. Include at least one actual API boundary test rather than calling every route as an ordinary Python function.

### Explanation required

Trace the client’s JSON to a validated request object, through the pure transformation, into a response model, and back to JSON. Explain why POST was chosen for a structured transformation request, why 200 is correct for this non-persistent preview, which rules belong to the schema or transformation, and how the tests show the caller’s data is not mutated.

For complexity, use `n` records and `c` total input characters. A straightforward linear traversal with linear string transformations has O(n + c) time. Normalized output occupies O(n + c) space in the usual size model; temporary string-processing memory is bounded by the largest record’s transformation. Explain auxiliary versus retained output memory in the actual implementation rather than labeling the entire function O(1) space.

### Submission for review

Provide the small source files or diff, test output, one curl transcript, and a short explanation of one design choice plus one uncertainty. A giant generated application is not the submission. Missing knowledge is a cue for one concrete lesson, not a reason to paste unfamiliar infrastructure.

## 11. Reference discipline

Use these as just-in-time references for the current package, not a reading list to finish before writing code. The curriculum’s sequence, effort estimates, tasks, and assessment rules are original proposals. References support framework, protocol, security, and tool semantics. Documentation URLs were inspected on September 21, 2026; future version-specific instructions should be rechecked.

- **S01 — uv project guide:** https://docs.astral.sh/uv/guides/projects/
- **S02 — FastAPI tutorial:** https://fastapi.tiangolo.com/tutorial/
- **S03 — HTTP Semantics, RFC 9110:** https://www.rfc-editor.org/rfc/rfc9110.html
- **S04 — Fielding, REST architectural style:** https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- **S05 — Architecture Patterns with Python, Repository:** https://www.cosmicpython.com/book/chapter_02_repository
- **S06 — Architecture Patterns with Python, Service Layer:** https://www.cosmicpython.com/book/chapter_04_service_layer
- **S07 — SQLAlchemy session basics and concurrency:** https://docs.sqlalchemy.org/en/20/orm/session_basics.html
- **S08 — Alembic migration autogeneration and its limits:** https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- **S09 — pytest fixtures:** https://docs.pytest.org/en/stable/how-to/fixtures.html
- **S10 — Pydantic models:** https://docs.pydantic.dev/latest/concepts/models/
- **S11 — GitHub Actions, build and test Python:** https://docs.github.com/en/actions/tutorials/build-and-test-code/python
- **S12 — GitHub Actions, secure use:** https://docs.github.com/en/actions/reference/security/secure-use
- **S13 — PostgreSQL SELECT, ordering and locking:** https://www.postgresql.org/docs/current/sql-select.html
- **S14 — Docker build best practices:** https://docs.docker.com/build/building/best-practices/
- **S15 — OWASP REST security:** https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
- **S16 — OWASP authorization:** https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- **S17 — OAuth 2.0 Security Best Current Practice, RFC 9700:** https://www.rfc-editor.org/rfc/rfc9700.html
- **S18 — Compute Engine container deployment and deprecations:** https://docs.cloud.google.com/compute/docs/containers/deploying-containers
- **S19 — FastAPI dependencies with yield:** https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
- **S20 — HTTPX timeouts:** https://www.python-httpx.org/advanced/timeouts/
- **S21 — GitHub Actions OIDC:** https://docs.github.com/en/actions/concepts/security/openid-connect
- **S22 — FastAPI sync and async:** https://fastapi.tiangolo.com/async/
- **S23 — HTTPX async clients:** https://www.python-httpx.org/async/
- **S24 — FastAPI background tasks:** https://fastapi.tiangolo.com/tutorial/background-tasks/
- **S25 — Starlette in-process background tasks:** https://starlette.dev/background/

Security study note: some framework examples demonstrate password-based OAuth patterns as learning examples. Do not mistake those recipes for a recommendation to implement the resource-owner-password grant in a new production authorization design; consult the current OAuth security BCP. The Relay core does not build an OAuth authorization server.

## 12. Scope exclusions and final evidence standard

Core exclusions: elaborate frontend, payments, arbitrary user code execution, generic workflow/DAG engines, Kubernetes, microservice decomposition, multi-region infrastructure, Kafka, and broad framework comparisons. Redis/Celery or another queue library is introduced only for a concrete comparison or requirement. AI features remain optional until the backend foundation is demonstrated.

A polished README, a high test count, a deployment URL, or the completion of these packages is not independently sufficient proof of competence. The strongest evidence is a bounded change the learner can design, implement, test, explain, deploy, diagnose, and adapt—with honest documentation of the help used and the system’s remaining limits.
