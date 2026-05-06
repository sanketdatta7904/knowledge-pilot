from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class FL3(BaseModel):
    id: str = ""
    description: str
    parametric_condition: Optional[str] = None


class FL2(BaseModel):
    id: str = ""
    description: str
    children: list[FL3] = Field(default_factory=list)


class FL1(BaseModel):
    id: str = ""
    description: str
    children: list[FL2] = Field(default_factory=list)


class Competency(BaseModel):
    id: str = ""
    description: str
    children: list[FL1] = Field(default_factory=list)


class PrereqEdge(BaseModel):
    prerequisite_id: str
    dependent_id: str
    rationale: str


class CompetencyMap(BaseModel):
    topic: str
    competencies: list[Competency]
    prerequisites: list[PrereqEdge] = Field(default_factory=list)


# Per-stage LLM response wrappers
class KDecomposeResponse(BaseModel):
    competencies: list[Competency]


class FL1DecomposeResponse(BaseModel):
    fl1_list: list[FL1]


class FL2DecomposeResponse(BaseModel):
    fl2_list: list[FL2]


class FL3DecomposeResponse(BaseModel):
    fl3_list: list[FL3]


class PrereqPairResponse(BaseModel):
    is_prerequisite: bool
    rationale: str
