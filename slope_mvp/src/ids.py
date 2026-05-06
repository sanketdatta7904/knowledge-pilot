from src.schemas import CompetencyMap


def assign_ids(comp_map: CompetencyMap) -> CompetencyMap:
    """Assign IDs based on tree position: K{i}, F{j}, F{j}.{k}, F{j}.{k}.{l}."""
    cm = comp_map.model_copy(deep=True)
    fl1_global = 0

    for k_idx, comp in enumerate(cm.competencies, start=1):
        comp.id = f"K{k_idx}"
        for fl1 in comp.children:
            fl1_global += 1
            fl1.id = f"F{fl1_global}"
            for fl2_idx, fl2 in enumerate(fl1.children):
                fl2.id = f"F{fl1_global}.{fl2_idx}"
                for fl3_idx, fl3 in enumerate(fl2.children, start=1):
                    fl3.id = f"F{fl1_global}.{fl2_idx}.{fl3_idx}"

    return cm
