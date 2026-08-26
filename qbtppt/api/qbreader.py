import requests

from qbtppt.models import BonusData, TossupData
from qbtppt.trivia.categories import category_value


def build_random_question_params(
    difficulties: list[int],
    categories: list[object],
    number: int,
    min_year: int,
    max_year: int,
) -> dict[str, object]:
    return {
        "difficulties": ",".join([str(diff) for diff in difficulties]),
        "categories": ",".join([category_value(category) for category in categories]),
        "number": number,
        "min_year": min_year,
        "max_year": max_year,
    }


def random_tossups(
    *,
    random_tossup_url: str,
    difficulties: list[int],
    categories: list[object],
    number: int,
    min_year: int,
    max_year: int,
) -> tuple[TossupData, ...]:
    params = build_random_question_params(difficulties, categories, number, min_year, max_year)
    response = requests.get(random_tossup_url, params=params)
    if response.status_code != 200:
        raise Exception(str(response.status_code) + " bad request")

    return tuple(TossupData.from_api_json(tossup) for tossup in response.json()["tossups"])


def random_bonuses(
    *,
    random_bonus_url: str,
    difficulties: list[int],
    categories: list[object],
    number: int,
    min_year: int,
    max_year: int,
) -> tuple[BonusData, ...]:
    params = build_random_question_params(difficulties, categories, number, min_year, max_year)
    response = requests.get(random_bonus_url, params=params)
    if response.status_code != 200:
        raise Exception(str(response.status_code) + " bad request")

    return tuple(BonusData.from_api_json(bonus) for bonus in response.json()["bonuses"])


def set_list(*, set_list_url: str) -> tuple[str, ...]:
    response = requests.get(set_list_url)
    if response.status_code != 200:
        raise Exception(str(response.status_code) + " bad request")

    return tuple(response.json()["setList"])


def num_packets(*, num_packets_url: str, set_name: str) -> int:
    response = requests.get(num_packets_url, params={"setName": set_name})
    if response.status_code != 200:
        if response.status_code == 404:
            raise ValueError(f"Requested set, {set_name}, not found.")
        raise Exception(str(response.status_code) + " bad request")

    return int(response.json()["numPackets"])


def packet_questions(
    *,
    packet_url: str,
    set_name: str,
    packet_number: int,
) -> tuple[list[TossupData], list[BonusData]]:
    response = requests.get(
        packet_url,
        params={
            "setName": set_name,
            "packetNumber": packet_number,
        },
    )
    if response.status_code != 200:
        raise Exception(str(response.status_code) + " bad request")

    packet = response.json()
    tossups = [TossupData.from_api_json(tossup) for tossup in packet["tossups"]]
    bonuses = [BonusData.from_api_json(bonus) for bonus in packet["bonuses"]]
    return tossups, bonuses
