from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from services.config import start_neo4j_connection
from services.api.political_queries import PoliticalQueries, ALLOWED_REL_TYPES

load_dotenv()

# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------

class CreateNodeBody(BaseModel):
    name: str
    party: str
    role: str


class CreateRelationshipBody(BaseModel):
    from_id: str
    to_id: str
    rel_type: str


# ---------------------------------------------------------------------------
# Application lifespan: open / close the Neo4j driver once
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    driver = start_neo4j_connection()
    if not driver:
        raise RuntimeError("Could not connect to Neo4j. Check your .env file.")
    app.state.driver = driver
    yield
    driver.close()
    print("Neo4j driver closed.")


# ---------------------------------------------------------------------------
# App instantiation
# ---------------------------------------------------------------------------

app = FastAPI(title="Relationship Finder API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    """Liveness probe."""
    return {"status": "ok"}


@app.get("/api/graph")
def get_graph(request: Request):
    """Return the full politician graph (nodes + edges)."""
    return PoliticalQueries.get_full_graph(request.app.state.driver)


@app.get("/api/politicians")
def get_politicians(request: Request):
    """Return all politician nodes ordered by name."""
    return PoliticalQueries.get_all_politicians(request.app.state.driver)


@app.post("/api/graph/node", status_code=201)
def create_node(body: CreateNodeBody, request: Request):
    """Create (or upsert) a Politician node."""
    node = PoliticalQueries.create_politician(
        request.app.state.driver, body.name, body.party, body.role
    )
    if not node:
        raise HTTPException(status_code=500, detail="Node could not be created.")
    return node


@app.post("/api/graph/relationship", status_code=201)
def create_relationship(body: CreateRelationshipBody, request: Request):
    """Create a typed relationship between two Politician nodes."""
    if body.rel_type not in ALLOWED_REL_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid relationship type '{body.rel_type}'. "
                f"Allowed: {sorted(ALLOWED_REL_TYPES)}"
            ),
        )
    try:
        return PoliticalQueries.create_relationship(
            request.app.state.driver, body.from_id, body.to_id, body.rel_type
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.delete("/api/graph/node/{node_id}", status_code=200)
def delete_node(node_id: str, request: Request):
    """Detach-delete a Politician node by its element ID."""
    try:
        PoliticalQueries.delete_politician(request.app.state.driver, node_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"success": True}


# ---------------------------------------------------------------------------
# Dev entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
