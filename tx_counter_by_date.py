import asyncio
import json
from collections import defaultdict
from datetime import datetime
from typing import Tuple

import httpx

DEFAULT_TRACKER_BASE_URL = "https://tracker.lisbon.icon.community"
DEFAULT_DID_CONTRACT_ADDRESS = "cxdd0cb8465b15e2971272c1ecf05691198552f770"
DEFAULT_DID_TX_METHOD_NAME = "create"


def figure_tx_count(tx_list: list, pivot_datetime: datetime, method_name: str = None) -> Tuple[int, bool]:
    tx_count: int = 0
    for tx in tx_list:
        method = tx.get("method")
        if method_name and method_name != method:
            continue

        block_ts = tx.get("block_timestamp")
        build_datetime: datetime = datetime.fromtimestamp(block_ts / 1_000_000)
        if build_datetime.date() > pivot_datetime.date():
            continue
        elif build_datetime.date() < pivot_datetime.date():
            return tx_count, False
        else:
            tx_count += 1

    return tx_count, True


def figure_all_tx_count_all(tx_list: list, method_name: str, end_date: datetime) -> Tuple[dict, bool]:
    tx_count_list: dict = defaultdict(int)
    for tx in tx_list:
        method = tx.get("method")
        if method_name and method_name != method:
            continue

        block_ts = tx.get("block_timestamp")
        build_datetime: datetime = datetime.fromtimestamp(block_ts / 1_000_000)
        if end_date:
            if build_datetime.date() < end_date.date():
                return tx_count_list, False

        tx_count_list[build_datetime.date().isoformat()] += 1

    return tx_count_list, True


async def all_tx_counter(tracker_base_url: str, contract: str, method_name: str, end_date: datetime) -> dict:
    tx_count: dict = defaultdict(int)
    client = httpx.AsyncClient(base_url=tracker_base_url)
    skip = 0
    limit = 100
    while True:
        response = await client.get(
            f"/api/v1/transactions/address/{contract}?addr={contract}&limit={limit}&skip={skip}"
        )
        print(f"{response.request.url=}")
        tx_list = response.json()
        if not tx_list:
            break

        count_list, is_continue = figure_all_tx_count_all(tx_list, method_name=method_name, end_date=end_date)
        print(f"{skip=}, {count_list=}")
        for key, value in count_list.items():
            tx_count[key] += value

        if not is_continue:
            break

        skip += limit

    return tx_count


async def tx_counter(pivot_date: str, tracker_base_url: str, contract: str, method_name: str = None) -> int:
    pivot_datetime: datetime = datetime.fromisoformat(pivot_date)

    tx_count: int = 0
    client = httpx.AsyncClient(base_url=tracker_base_url)
    skip = 0
    limit = 100
    while True:
        response = await client.get(
            f"/api/v1/transactions/address/{contract}?addr={contract}&limit={limit}&skip={skip}"
        )
        print(f"{response.request.url=}")
        tx_list = response.json()
        if not tx_list:
            break

        count, is_continue = figure_tx_count(tx_list, pivot_datetime, method_name=method_name)
        print(f"{count=}")
        tx_count += count
        if not is_continue:
            break

        skip += limit

    return tx_count


def input_common_env_info() -> dict:
    print("==========================================")
    print("Enter information for transaction count.")
    tracker_base_url: str = input(f"tracker base url(DEFAULT:{DEFAULT_TRACKER_BASE_URL}): ")
    if not tracker_base_url:
        tracker_base_url = DEFAULT_TRACKER_BASE_URL

    contract: str = input(f"contract address(DEFAULT:{DEFAULT_DID_CONTRACT_ADDRESS}): ")
    if not contract:
        contract = DEFAULT_DID_CONTRACT_ADDRESS

    method_name: str = input(f"transaction method name(DEFAULT: {DEFAULT_DID_TX_METHOD_NAME}):")
    if not method_name:
        method_name = DEFAULT_DID_TX_METHOD_NAME

    return {"tracker_base_url": tracker_base_url, "contract": contract, "method_name": method_name}


async def menu_1():
    common_env_info: dict = input_common_env_info()
    tracker_base_url: str = common_env_info.get("tracker_base_url")
    contract: str = common_env_info.get("contract")
    method_name: str = common_env_info.get("method_name")
    date = input("date for count(DEFAULT: today): ")
    if not date:
        now: datetime = datetime.now()
        date: str = now.date().isoformat()

    print("###########################################")
    print("Request tx list ...")

    tx_count: int = await tx_counter(pivot_date=date,
                                     tracker_base_url=tracker_base_url,
                                     contract=contract,
                                     method_name=method_name,
    )

    print("##########################################")
    print(f"date={date}, result={tx_count}")


async def menu_2():
    common_env_info: dict = input_common_env_info()
    tracker_base_url: str = common_env_info.get("tracker_base_url")
    contract: str = common_env_info.get("contract")
    method_name: str = common_env_info.get("method_name")
    date = input("end date for count(DEFAULT: created date of contract): ")
    end_date: datetime = datetime.fromisoformat(date) if date else None

    print("###########################################")
    print("Request tx list ...")

    tx_count: dict = await all_tx_counter(tracker_base_url=tracker_base_url,
                                          contract=contract,
                                          method_name=method_name,
                                          end_date=end_date,
    )

    print("##########################################")
    print(f"{json.dumps(tx_count, indent=4)}")

    print(f"end_date={end_date.date().isoformat() if end_date else None}, total count={sum(tx_count.values())}")


async def show_menu():
    while True:
        print("==========================================")
        print("[1] Count of transactions at a date.")
        print("[2] Count of transactions during a term.")
        print("[q] Quit")
        print("==========================================")
        menu: str = input("Press key of menu: ")
        match menu:
            case "q":
                break
            case "1":
                await menu_1()
            case "2":
                await menu_2()
            case _:
                raise ValueError(f"Unsupported menu number({menu}).")


if __name__ == "__main__":
    asyncio.run(show_menu())
