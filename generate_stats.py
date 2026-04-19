import requests

USERNAME = "Pradipta-Programmer"

repos_url = f"https://api.github.com/users/{USERNAME}/repos"
repos = requests.get(repos_url).json()

lang_data = {}

for repo in repos:
    if "languages_url" not in repo:
        continue

    langs = requests.get(repo["languages_url"]).json()

    if isinstance(langs, dict):
        for lang, bytes_ in langs.items():
            lang_data[lang] = lang_data.get(lang, 0) + bytes_

if not lang_data:
    with open("stats.svg", "w") as f:
        f.write("<svg><text x='10' y='20'>No Data</text></svg>")
    exit()

total = sum(lang_data.values())

bars = ""
y = 20

for lang, val in sorted(lang_data.items(), key=lambda x: x[1], reverse=True):
    percent = (val / total) * 100
    bars += f"<text x='10' y='{y}' fill='white'>{lang}: {percent:.2f}%</text>"
    y += 20

svg = f"""
<svg width="400" height="{y+20}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#282a36"/>
  {bars}
</svg>
"""

with open("stats.svg", "w") as f:
    f.write(svg)
