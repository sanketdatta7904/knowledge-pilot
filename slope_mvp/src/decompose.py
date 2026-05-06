from pathlib import Path

from src.llm import call_llm
from src.schemas import (
    Competency, FL1, FL2, FL3,
    KDecomposeResponse, FL1DecomposeResponse, FL2DecomposeResponse, FL3DecomposeResponse,
)

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def decompose_k(topic: str, text: str) -> list[Competency]:
    system = _load_prompt("k_decompose.md")
    user = f"Topic: {topic}\n\nChapter text:\n{text}"
    resp = call_llm(system, user, KDecomposeResponse)
    return resp.competencies


def decompose_fl1(topic: str, text: str, competency: Competency) -> list[FL1]:
    system = _load_prompt("fl1_decompose.md")
    user = (
        f"Topic: {topic}\n"
        f"Parent competency: {competency.description}\n\n"
        f"Chapter text:\n{text}"
    )
    resp = call_llm(system, user, FL1DecomposeResponse)
    return resp.fl1_list


def decompose_fl2(topic: str, text: str, competency: Competency, fl1: FL1) -> list[FL2]:
    system = _load_prompt("fl2_decompose.md")
    user = (
        f"Topic: {topic}\n"
        f"Parent competency: {competency.description}\n"
        f"Parent FL1: {fl1.description}\n\n"
        f"Chapter text:\n{text}"
    )
    resp = call_llm(system, user, FL2DecomposeResponse)
    return resp.fl2_list


def decompose_fl3(topic: str, fl1: FL1, fl2: FL2) -> list[FL3]:
    system = _load_prompt("fl3_decompose.md")
    user = (
        f"Topic: {topic}\n"
        f"Parent FL1: {fl1.description}\n"
        f"Parent FL2: {fl2.description}"
    )
    resp = call_llm(system, user, FL3DecomposeResponse)
    return resp.fl3_list
