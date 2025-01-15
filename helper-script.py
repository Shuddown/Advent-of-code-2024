from requests import request
from dotenv import load_dotenv, set_key
import os
from pathlib import Path
from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import Pool
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

from typing import Optional, List, Tuple

def handle_session(arg_session: Optional[str], env_path: Path, parser: ArgumentParser) -> str:
    session_key = "SESSION_COOKIE"
    env_session = os.getenv(session_key)

    if arg_session is None and env_session is None:
        print("Please set your session token using the -s or --session option")
        parser.print_help()
        raise SystemExit()

    if arg_session is None and env_session is not None:
        return env_session

    elif arg_session is not None and env_session is not None and arg_session != env_session:
        while True:
            user_choice = input("A session token already exists. Do you want to overwrite it? [Y/n]: ")
            if user_choice in ("Y", "y", ""):
                set_key(env_path, session_key, arg_session)
                return arg_session
            elif user_choice in ("N", "n"):
                return env_session
            else:
                print("Please enter a valid option [Y/n]")
    else:
        if not env_path.exists():
            env_path.touch()
        set_key(env_path, session_key, arg_session)
        return arg_session

def get_year_day(arg_year: Optional[int], arg_day: Optional[int], parser: ArgumentParser) -> List[Tuple[int, int]]:
    current_date = datetime.now()
    FIRST_AOC_YEAR = 2015
    FIRST_DAY = 1
    LAST_DAY = 25
    latest_year = current_date.year if current_date.month == 12 else current_date.year - 1

    if arg_year is not None and not (FIRST_AOC_YEAR <= arg_year <= latest_year):
        print(f"Enter a valid year ({FIRST_AOC_YEAR}-{latest_year})!") 
        parser.print_help()
        raise SystemExit()

    latest_day = LAST_DAY if arg_year != current_date.year else min(LAST_DAY, current_date.day)

    if arg_day is not None and not (FIRST_DAY <= arg_day <= latest_day):
        print(f"Enter a valid day ({FIRST_DAY}-{latest_day})!")
        parser.print_help()
        raise SystemExit()

    if arg_year is not None and arg_day is not None:
        return [(arg_year, arg_day)]
    elif arg_year is not None and arg_day is None:
        return [(arg_year, day) for day in range(FIRST_DAY, latest_day + 1)]
    elif arg_day is not None and arg_year is None:
        return [(latest_year, arg_day)]
    else:
        if current_date.month != 12:
            print("You can only specify no arguments during Advent of Code!")
            parser.print_help()
            raise SystemExit()
        return [(latest_year, latest_day)]

def create_folder(year: int, day: int, input_text: str) -> None:
    assert input_text != "", "Input text shouldn't be empty"

    extensions = ['.ts', '.go', '.lua']
    script_directory = Path(__file__).parent
    year_folder = script_directory / f"AOC {year}"
    day_folder = year_folder / f"Day {day}"
    files = [day_folder / ("solution" + extension) for extension in extensions]

    year_folder.mkdir(exist_ok=True)
    day_folder.mkdir(exist_ok=True)
    for file in files:
        file.touch()

    input_file = day_folder / "input.txt"
    with input_file.open("w", encoding="UTF-8") as file:
        file.write(input_text)

async def get_input_async(url: str, session_cookie: str) -> str:
    async with aiohttp.ClientSession(cookies={"session": session_cookie}) as session:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to get input from {url}")
                print(f"Status Code: {response.status}")
                print(await response.text())
                return ""
            return await response.text()

def get_input(url: str, session_cookie: str) -> str:
    with request("GET", url, cookies={"session": session_cookie}) as r:
        if not r.ok:
            print(f"Failed to get input from {url}")
            print(f"Status Code: {r.status_code}")
            print(r.text)
            return ""
        return r.text

def handle_download_multiprocess(urls: List[str], session_cookie: str) -> List[str]:
    url_count = len(urls)
    assert url_count > 0, "urls should have one or more url"

    with Pool(processes=url_count) as pool:
        inputs = pool.map(lambda u: get_input(u, session_cookie), urls)
    return inputs

async def handle_download_async(urls: List[str], session_cookie: str) -> List[str]:
    url_count = len(urls)
    assert url_count > 0, "urls should have one or more url"

    tasks = [asyncio.create_task(get_input_async(url, session_cookie)) for url in urls]
    return await asyncio.gather(*tasks)

def handle_download_threading(urls: List[str], session_cookie: str) -> List[str]:
    url_count = len(urls)
    assert url_count > 0, "urls should have one or more url"

    wait_time_ratio = 0.5
    num_cores = os.cpu_count()

    num_threads = int((url_count * wait_time_ratio) + num_cores)

    with ThreadPoolExecutor(num_threads) as exe:
        return exe.map(get_input, urls)


async def main():
    parser = ArgumentParser()
    parser.add_argument("-s", "--session", help="Session cookie value", type=str)
    parser.add_argument("-y", "--year", help="Advent of Code year", type=int)
    parser.add_argument("-d", "--day", help="Advent of Code day", type=int)

    args = parser.parse_args()

    aoc_directory = Path(__file__).parent
    env_path = aoc_directory / ".env"
    load_dotenv(env_path)

    session_cookie = handle_session(args.session, env_path, parser)
    if args.session is not None and args.day is None and args.year is None:
        raise SystemExit()

    year_and_days = get_year_day(args.year, args.day, parser)
    urls = [f"https://adventofcode.com/{year}/day/{day}/input" for year, day in year_and_days]
    inputs = await handle_download_async(urls, session_cookie)

    for input_text, (year, day) in zip(inputs, year_and_days):
        create_folder(year, day, input_text)

if __name__ == "__main__":
    asyncio.run(main())
