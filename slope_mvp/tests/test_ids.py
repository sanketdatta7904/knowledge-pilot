from src.schemas import Competency, FL1, FL2, FL3, CompetencyMap
from src.ids import assign_ids


def test_assign_ids_matches_lu14_pattern():
    """Verify ID assignment matches LU14's pattern: K1/F1/F1.0/F1.0.1."""
    cm = CompetencyMap(
        topic="Slope",
        competencies=[
            Competency(
                description="comp1",
                children=[
                    FL1(
                        description="fl1-a",
                        children=[
                            FL2(
                                description="fl2-a1",
                                children=[
                                    FL3(description="fl3-a1-1", parametric_condition="m>0"),
                                    FL3(description="fl3-a1-2", parametric_condition="m<0"),
                                ],
                            ),
                            FL2(description="fl2-a2", children=[]),
                        ],
                    ),
                ],
            ),
            Competency(
                description="comp2",
                children=[
                    FL1(
                        description="fl1-b",
                        children=[
                            FL2(
                                description="fl2-b1",
                                children=[
                                    FL3(description="fl3-b1-1", parametric_condition="b>0"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    result = assign_ids(cm)

    # K-level
    assert result.competencies[0].id == "K1"
    assert result.competencies[1].id == "K2"

    # FL1 — globally numbered
    assert result.competencies[0].children[0].id == "F1"
    assert result.competencies[1].children[0].id == "F2"

    # FL2 — F{fl1}.{index starting at 0}
    assert result.competencies[0].children[0].children[0].id == "F1.0"
    assert result.competencies[0].children[0].children[1].id == "F1.1"
    assert result.competencies[1].children[0].children[0].id == "F2.0"

    # FL3 — F{fl1}.{fl2_idx}.{index starting at 1}
    assert result.competencies[0].children[0].children[0].children[0].id == "F1.0.1"
    assert result.competencies[0].children[0].children[0].children[1].id == "F1.0.2"
    assert result.competencies[1].children[0].children[0].children[0].id == "F2.0.1"


def test_assign_ids_does_not_mutate_original():
    cm = CompetencyMap(
        topic="Test",
        competencies=[Competency(description="c", children=[FL1(description="f")])],
    )
    result = assign_ids(cm)
    assert cm.competencies[0].id == ""
    assert result.competencies[0].id == "K1"
