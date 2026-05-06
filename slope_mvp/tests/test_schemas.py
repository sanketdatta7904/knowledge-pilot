from src.schemas import (
    FL3, FL2, FL1, Competency, CompetencyMap, PrereqEdge,
    KDecomposeResponse, FL1DecomposeResponse, FL2DecomposeResponse,
    FL3DecomposeResponse, PrereqPairResponse,
)


def test_competency_map_roundtrip():
    cm = CompetencyMap(
        topic="Slope",
        competencies=[
            Competency(
                id="K1",
                description="understand slope as a ratio",
                children=[
                    FL1(
                        id="F1",
                        description="determine the equation",
                        children=[
                            FL2(
                                id="F1.0",
                                description="read the slope",
                                children=[
                                    FL3(id="F1.0.1", description="read slope when m>0", parametric_condition="m>0"),
                                    FL3(id="F1.0.2", description="read slope when m<0", parametric_condition="m<0"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
        prerequisites=[
            PrereqEdge(prerequisite_id="F1.0", dependent_id="F1.1", rationale="need slope first"),
        ],
    )
    data = cm.model_dump()
    restored = CompetencyMap.model_validate(data)
    assert restored == cm


def test_response_models_roundtrip():
    k = KDecomposeResponse(competencies=[Competency(description="test")])
    assert KDecomposeResponse.model_validate(k.model_dump()) == k

    fl1 = FL1DecomposeResponse(fl1_list=[FL1(description="test")])
    assert FL1DecomposeResponse.model_validate(fl1.model_dump()) == fl1

    fl2 = FL2DecomposeResponse(fl2_list=[FL2(description="test")])
    assert FL2DecomposeResponse.model_validate(fl2.model_dump()) == fl2

    fl3 = FL3DecomposeResponse(fl3_list=[FL3(description="test", parametric_condition="x>0")])
    assert FL3DecomposeResponse.model_validate(fl3.model_dump()) == fl3

    prereq = PrereqPairResponse(is_prerequisite=True, rationale="needed")
    assert PrereqPairResponse.model_validate(prereq.model_dump()) == prereq


def test_empty_ids_default():
    c = Competency(description="test")
    assert c.id == ""
    assert c.children == []


def test_fl3_optional_condition():
    f = FL3(description="no condition")
    assert f.parametric_condition is None
