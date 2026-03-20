# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Package Management

Always use `uv` — never `pip` or `pip install`.

```bash
uv add <package>                    # add dependency
uv add --dev <package>              # add dev dependency
uv run python <script>              # run a script
uv run pytest                       # run tests
uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
uv run streamlit run src/ui/app.py
```

## First-Time Setup

```bash
uv run python scripts/generate_data.py   # generate data/raw/**/*.md
uv run python scripts/ingest.py          # embed + load into data/chroma_db/
```

Copy `.env.example` → `.env` and fill in API keys before running either script.

## Running Tests

```bash
uv run pytest                            # all tests
uv run pytest tests/test_retrieval/      # single module
uv run pytest -k "test_rbac_filter"      # single test by name
```

## Python Version

**Python 3.11 only.** `chromadb 1.5.2` is incompatible with Python 3.14 due to Pydantic v1 internals. Do not upgrade the Python version.

---

## Architecture

This is a RAG chatbot where **RBAC is enforced at the vector store retrieval layer**, not by the LLM. This means prompt injection cannot bypass access control — the Chroma `where` filter runs before any document content reaches the model.

### Request Flow

```
POST /chat/query (FastAPI)
  → get_current_user dependency (fast-fail JWT check)
  → graph.invoke(initial_state)  ← LangGraph compiled once at startup

LangGraph nodes (in order):
  authenticate_node → guardrail_input_node → validate_query_node → retrieve_node
                            │                                            │
                      (PII/scope block)                           generate_node
                            ↓                                           │
                        error_node                         guardrail_output_node
                                                                        │
                                                          extract_citations_node
                                                                        │
                                                            cost_tracking_node → END
```

### RBAC — The Critical Pattern

`config/roles.py` is the single source of truth. Never hardcode role-to-department mappings anywhere else.

`access_roles` in Chroma metadata is stored as a **comma-separated string** (e.g. `"finance,clevel"`), not an array — Chroma's `$contains` only works on strings.

```python
# src/retrieval/rbac_filter.py
def build_rbac_filter(role: Role) -> dict:
    accessible = ROLE_ACCESS_MAP[role]
    if len(accessible) == 1:
        return {"access_roles": {"$contains": accessible[0]}}
    return {"$or": [{"access_roles": {"$contains": dept}} for dept in accessible]}
```

This filter is passed to `collection.query(where=filter)` — documents that don't match never leave the vector store.

### LangGraph Compilation

The graph is compiled **once at FastAPI startup** via `lifespan` and stored in `app.state.graph`. Compiled graphs are stateless — each request passes its own `RBACChatState` dict. Never recompile per request.

### Dual Auth (Defense in Depth)

Auth is validated twice: once by the FastAPI `get_current_user` dependency (returns 401 fast before the graph runs) and again inside `authenticate_node` (canonical enforcement). Both must pass.

### Guardrails

- **Input**: scope check (regex blocklist + keyword heuristic) runs first, then PII detection. PII is **redacted, not blocked** — query intent is preserved.
- **Output**: PII redactor always runs on LLM answers before they reach the user.
- Guardrail events are logged to `data/metrics.db` (table: `guardrail_events`) without storing the flagged text.

### Cost Monitoring

Token costs are calculated in `cost_tracking_node` (last node before END). Thresholds: $0.10/request, $5.00/user/day, $50.00/system/day. All stored in `data/metrics.db` (table: `request_costs`).

### Ragas Evaluation

Runs **asynchronously** (non-blocking, background task) after the API response is returned. Scores stored in `data/metrics.db` (table: `ragas_scores`). Alert thresholds: faithfulness < 0.7, answer_relevancy < 0.7, context_precision < 0.6.

### Document Ingestion

Every markdown file in `data/raw/` must have a YAML frontmatter block with `doc_id`, `department`, `access_roles` (as a list — the ingestion script converts it to a comma-string for Chroma), and `classification`. The ingestion script (`scripts/ingest.py`) uses `RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)`.

---

## Demo Accounts

| Username | Password | Role | Sees |
|---|---|---|---|
| finance_user | Password123 | finance | finance + general |
| marketing_user | Password123 | marketing | marketing + general |
| hr_user | Password123 | hr | hr + general |
| eng_user | Password123 | engineering | engineering + general |
| ceo | Password123 | clevel | everything |
| employee1 | Password123 | employee | general only |

---

## Critical Test Cases

Before any PR, verify these manually or via `pytest`:

1. `retrieve("salary information", role=Role.EMPLOYEE)` → 0 results
2. `retrieve("Q1 revenue", role=Role.MARKETING)` → 0 results (finance doc, not accessible)
3. `retrieve("anything", role=Role.CLEVEL)` → results from any department
4. Query `"ignore previous instructions"` → rejected by `validate_query_node`
5. Query `"What is John Smith's salary?"` → PII redacted before LLM sees it
6. Query `"Write me a Python script"` → blocked by `guardrail_input_node`
