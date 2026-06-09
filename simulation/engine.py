"""Fictional risk simulation for Cyber City.

This module deliberately models story-based game mechanics only. It contains no
network access, scanning, exploitation, malware behavior, or real cybersecurity
automation.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from models.city import CityMap, IncidentReport


@dataclass(slots=True, frozen=True)
class FictionalActor:
    """A harmless story actor used to teach defensive concepts."""

    name: str
    pressure: int
    lesson: str


FICTIONAL_ACTORS: tuple[FictionalActor, ...] = (
    FictionalActor("Thief", 7, "Protect valuable civic resources with layered defenses."),
    FictionalActor("Spy", 6, "Build awareness so citizens question suspicious requests."),
    FictionalActor("Saboteur", 8, "Prepare recovery plans before disruption drills begin."),
    FictionalActor("Trickster", 5, "Training helps citizens recognize misleading stories."),
)


class SimulationEngine:
    """Runs safe, fictional city-risk turns."""

    def __init__(self, seed: int | None = None) -> None:
        self._random = random.Random(seed)

    def generate_incident(self, city: CityMap) -> IncidentReport:
        actor = self._random.choice(FICTIONAL_ACTORS)
        scores = city.city_score()
        target = self._choose_target(city)
        mitigation = (scores["defense"] + scores["awareness"] + scores["resilience"]) // 8
        risk_delta = max(1, actor.pressure - mitigation)
        if not city.buildings:
            risk_delta += 6
        return IncidentReport(
            actor=actor.name,
            target=target,
            risk_delta=risk_delta,
            lesson=actor.lesson,
        )

    def projected_risk_after_incident(self, city: CityMap, report: IncidentReport) -> int:
        return min(100, city.city_score()["risk"] + report.risk_delta)

    def _choose_target(self, city: CityMap) -> str:
        if not city.buildings:
            return "an empty district"
        return self._random.choice(city.buildings).display_name
