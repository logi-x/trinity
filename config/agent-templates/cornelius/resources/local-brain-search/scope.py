"""FAISS glue for the scope primitive.

Single home for the IDSelector builder so the CLI (search.py) and the daemon
(daemon.py) read paths cannot diverge. The PURE scope logic (scope_of,
resolve_read_scope, is_pure_core, scoped_subgraph) lives in memory_config; this
module adds only the part that needs faiss/numpy and is imported only by the
retrieval paths that already import faiss.

Re-exports the pure primitives so call sites can `from scope import
resolve_read_scope, build_scope_selector` from one place.
"""
import numpy as np
import faiss

from memory_config import (  # noqa: F401 - re-exported for caller convenience
    CORE_FOLDERS,
    scope_of,
    scope_id,
    in_read_scope,
    resolve_read_scope,
    is_pure_core,
    scoped_subgraph,
    core_subgraph,
    scope_kind,
    is_reference_scope,
    reference_folders,
)


def build_scope_selector(metadata, read_scope):
    """Build a FAISS IDSelectorBatch over the metadata-row positions in scope.

    `metadata` is the list loaded from brain_metadata.pkl; row position i is the
    FAISS vector id for that chunk (the index is built by a single index.add in
    note order), so the selector is just the in-scope row indices.

    Returns ``(selector, backing)`` where ``backing`` is the int64 numpy array
    the selector borrows.

    LIFETIME CONTRACT: the caller MUST keep ``backing`` referenced until
    ``index.search()`` returns. faiss.IDSelectorBatch does NOT copy the buffer;
    dropping it early is a use-after-free (segfault), not a wrong result.

    Returns ``(None, None)`` when no row matches the scope - the caller should
    short-circuit to an empty result set (fail-safe: no leak, no crash).
    """
    backing = np.fromiter(
        (i for i, m in enumerate(metadata) if in_read_scope(m["note_id"], read_scope)),
        dtype="int64",
    )
    if backing.size == 0:
        return None, None
    return faiss.IDSelectorBatch(backing), backing
