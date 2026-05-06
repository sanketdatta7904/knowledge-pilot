import sys

from src.extract import extract_text
from src.decompose import decompose_k, decompose_fl1, decompose_fl2, decompose_fl3
from src.ids import assign_ids
from src.prereq import extract_prerequisites, validate_dag
from src.excel_writer import write_excel
from src.schemas import CompetencyMap


def run(pdf_or_txt_path: str, topic: str, out_path: str) -> CompetencyMap:
    """Run the full pipeline: extract → decompose → IDs → prereqs → Excel."""
    print("[extract] Reading input...", file=sys.stderr)
    text = extract_text(pdf_or_txt_path)
    print(f"[extract] {len(text)} chars", file=sys.stderr)

    print("[k-decompose] Identifying competencies...", file=sys.stderr)
    competencies = decompose_k(topic, text)
    print(f"[k-decompose] {len(competencies)} competencies", file=sys.stderr)

    for c in competencies:
        print(f"[fl1-decompose] K: {c.description[:50]}...", file=sys.stderr)
        c.children = decompose_fl1(topic, text, c)
        print(f"[fl1-decompose] {len(c.children)} FL1s", file=sys.stderr)

        for fl1 in c.children:
            print(f"[fl2-decompose] FL1: {fl1.description[:50]}...", file=sys.stderr)
            fl1.children = decompose_fl2(topic, text, c, fl1)
            print(f"[fl2-decompose] {len(fl1.children)} FL2s", file=sys.stderr)

            for fl2 in fl1.children:
                fl2.children = decompose_fl3(topic, fl1, fl2)

    comp_map = CompetencyMap(topic=topic, competencies=competencies)
    comp_map = assign_ids(comp_map)

    fl3_count = sum(
        len(fl2.children)
        for c in comp_map.competencies
        for fl1 in c.children
        for fl2 in fl1.children
    )
    fl2_count = sum(
        len(fl1.children)
        for c in comp_map.competencies
        for fl1 in c.children
    )
    print(f"[ids] Assigned IDs: {fl2_count} FL2s, {fl3_count} FL3s", file=sys.stderr)

    print("[prereq] Extracting prerequisites...", file=sys.stderr)
    all_fl2_ids = [
        fl2.id
        for c in comp_map.competencies
        for fl1 in c.children
        for fl2 in fl1.children
    ]
    edges = extract_prerequisites(comp_map)
    print(f"[prereq] {len(edges)} raw edges", file=sys.stderr)
    edges = validate_dag(edges, all_fl2_ids)
    print(f"[prereq] {len(edges)} edges after DAG validation", file=sys.stderr)
    comp_map.prerequisites = edges

    print(f"[excel] Writing {out_path}...", file=sys.stderr)
    write_excel(comp_map, out_path)
    print("[done]", file=sys.stderr)

    return comp_map
