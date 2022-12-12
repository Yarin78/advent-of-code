import sys
from typing import List, Tuple
import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup
import mysql.connector

@dataclass
class LeaderboardEntry:
    pos: int
    score: int
    duration: int
    name: str

def extract_daily_leaderboard(html_doc: str) -> Tuple[List[LeaderboardEntry], List[LeaderboardEntry]]:
    soup = BeautifulSoup(html_doc, 'html.parser')

    entries = soup.find_all("div", attrs={"class": "leaderboard-entry"})
    if len(entries) != 200:
        raise Exception(f"Daily board not yet complete; had {len(entries)} entries, excepted 200")

    all_entries: List[LeaderboardEntry] = []
    for entry in entries:
        data = entry.find_all(string=True)
        pos = int(data[0].strip().replace(')', ''))
        time_str = data[2][-8:]
        time = int(time_str[0:2]) * 3600 + int(time_str[3:5]) * 60 + int(time_str[6:])
        name = data[4]
        all_entries.append(LeaderboardEntry(pos, 101-pos, time, name))

    return (all_entries[0:100], all_entries[100:200])


def save_leaderboard(year: int, day: int, task: int, entries: List[LeaderboardEntry]):
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='aoc')
    cursor = cnx.cursor()

    delete_task = "DELETE FROM leaderboard WHERE year = %s AND day = %s AND task = %s"
    cursor.execute(delete_task, (year, day, task))

    add_entry = ("INSERT INTO leaderboard(year, day, task, pos, score, duration, name) VALUES (%s, %s, %s, %s, %s, %s, %s)")
    for entry in entries:
        cursor.execute(add_entry, (year, day, task, entry.pos, entry.score, entry.duration, entry.name))
    cnx.commit()

    cursor.close()
    cnx.close()


if len(sys.argv) != 3:
    print("Usage: import_leaderboard <year> <day>")
    exit(1)

year = int(sys.argv[1])
day = int(sys.argv[2])

print(f"Fetching data for year {year} and day {day}...")

r = requests.get(f"https://adventofcode.com/{year}/leaderboard/day/{day}")
r.encoding=r.apparent_encoding
html_doc = r.text
#with open("day1.html", "wt") as f:
#   f.write(r.text)
#exit(0)
#with open("day1.html", "rt") as f:
#    html_doc = f.read()

print("Saving data...")
(task1board, task2board) = extract_daily_leaderboard(html_doc)

save_leaderboard(year, day, 1, task1board)
save_leaderboard(year, day, 2, task2board)

print("Done!")
