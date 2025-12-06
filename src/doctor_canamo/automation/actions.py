from dataclasses import dataclass
from typing import List

from doctor_canamo.datamodel import Diagnosis


@dataclass
class Action:
    target: str
    command: str
    value: float
    unit: str
    rationale: str


def plan_actions(diagnoses: List[Diagnosis]) -> List[Action]:
    actions: List[Action] = []
    for diagnosis in diagnoses:
        if "ph" in diagnosis.message.lower():
            actions.append(
                Action(
                    target="growee.ph",
                    command="adjust",
                    value=0.2 if "debajo" in diagnosis.message else -0.2,
                    unit="pH",
                    rationale=diagnosis.message,
                )
            )
        if "air_temp" in diagnosis.message.lower():
            actions.append(
                Action(
                    target="smartlife.ac",
                    command="cooling" if "encima" in diagnosis.message else "heating",
                    value=24.0,
                    unit="C",
                    rationale=diagnosis.message,
                )
            )
        if "humidity" in diagnosis.message.lower():
            actions.append(
                Action(
                    target="smartlife.dehumidifier",
                    command="toggle",
                    value=50.0,
                    unit="%",
                    rationale=diagnosis.message,
                )
            )
    return actions
