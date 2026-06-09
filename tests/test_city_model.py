from pathlib import Path

from database import CityStorage
from models.city import BuildingType, CityMap
from simulation import SimulationEngine


def test_city_scores_reward_defensive_buildings() -> None:
    city = CityMap()
    initial_risk = city.city_score()["risk"]

    city.place_building(BuildingType.FIREWALL_TOWER, 0, 0)
    city.place_building(BuildingType.TRAINING_ACADEMY, 0, 1)
    city.place_building(BuildingType.BACKUP_STATION, 0, 2)

    scores = city.city_score()
    assert scores["defense"] == 13
    assert scores["awareness"] == 14
    assert scores["resilience"] == 16
    assert scores["risk"] < initial_risk


def test_city_storage_round_trip(tmp_path: Path) -> None:
    storage = CityStorage(tmp_path / "cities.db")
    city = CityMap()
    city.place_building(BuildingType.INCIDENT_HQ, 2, 3)

    storage.save_city("test-city", city)
    loaded = storage.load_city("test-city")

    assert storage.list_cities() == ["test-city"]
    assert loaded.building_at(2, 3).building_type is BuildingType.INCIDENT_HQ


def test_simulation_uses_only_fictional_actor_names() -> None:
    city = CityMap()
    engine = SimulationEngine(seed=7)

    report = engine.generate_incident(city)

    assert report.actor in {"Thief", "Spy", "Saboteur", "Trickster"}
    assert report.risk_delta > 0
    assert "network" not in report.lesson.lower()
