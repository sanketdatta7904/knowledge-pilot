import sys

import networkx as nx

from src.llm import call_llm
from src.schemas import CompetencyMap, FL2, PrereqEdge, PrereqPairResponse


def extract_prerequisites(comp_map: CompetencyMap) -> list[PrereqEdge]:
    """Query LLM for pairwise prerequisite relationships between FL2 nodes within the same FL1."""
    edges: list[PrereqEdge] = []
    system = "You determine whether one math sub-skill is a prerequisite for another."

    # Only compare within the same FL1 — cross-FL1 prereqs are rare
    fl1_groups: list[list[FL2]] = []
    for comp in comp_map.competencies:
        for fl1 in comp.children:
            if len(fl1.children) >= 2:
                fl1_groups.append(fl1.children)

    total_pairs = sum(len(g) * (len(g) - 1) for g in fl1_groups)
    count = 0
    print(f"  [prereq] {total_pairs} pairs to evaluate (within-FL1 only)", file=sys.stderr)

    for group in fl1_groups:
        for a in group:
            for b in group:
                if a.id == b.id:
                    continue
                count += 1
                if count % 5 == 0 or count == total_pairs:
                    print(f"  [prereq] {count}/{total_pairs}", file=sys.stderr)

                user = (
                    f"Skill A: {a.description}\n"
                    f"Skill B: {b.description}\n\n"
                    "Question: To learn skill B, must a student already be proficient at skill A?\n\n"
                    "Rules:\n"
                    "- Only return true if A is GENUINELY required for B — not just thematically related.\n"
                    "- Curriculum dependency, not topic similarity.\n"
                    "- If unsure, return false."
                )
                resp = call_llm(system, user, PrereqPairResponse)
                if resp.is_prerequisite:
                    edges.append(PrereqEdge(
                        prerequisite_id=a.id,
                        dependent_id=b.id,
                        rationale=resp.rationale,
                    ))

    return edges


def validate_dag(edges: list[PrereqEdge], all_fl2_ids: list[str]) -> list[PrereqEdge]:
    """Build DAG, remove cycle-creating edges, apply transitive reduction."""
    G = nx.DiGraph()
    G.add_nodes_from(all_fl2_ids)

    for edge in edges:
        G.add_edge(edge.prerequisite_id, edge.dependent_id)
        if not nx.is_directed_acyclic_graph(G):
            G.remove_edge(edge.prerequisite_id, edge.dependent_id)
            print(
                f"  [prereq] dropped cycle-creating edge: {edge.prerequisite_id} → {edge.dependent_id}",
                file=sys.stderr,
            )

    reduced = nx.transitive_reduction(G)
    reduced_set = set(reduced.edges())
    return [e for e in edges if (e.prerequisite_id, e.dependent_id) in reduced_set]


def _collect_all_fl2(comp_map: CompetencyMap) -> list[FL2]:
    result: list[FL2] = []
    for comp in comp_map.competencies:
        for fl1 in comp.children:
            result.extend(fl1.children)
    return result
