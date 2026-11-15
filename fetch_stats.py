#!/usr/bin/env python3
"""Fetch live GitHub repo stats. Unauthenticated, respects rate limits."""
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UA = "Awesome-Craft-Robotics-stats (https://github.com/EdisonTKPcom/Awesome-Craft-Robotics)"
API = "https://api.github.com"
OUT = ROOT / "stats.tsv"

REPOS = ['pollen-robotics/microduck', 'pollen-robotics/microduck_rl', 'osrbot/microduck-ros2-isaac', 'librezoo/microduck-simulator', 'apirrone/Open_Duck_Mini', 'apirrone/Open_Duck_Mini_Runtime', 'pollen-robotics/reachy_mini', 'pollen-robotics/reachy2-sdk', 'unitreerobotics/unitree_sdk2', 'unitreerobotics/unitree_sdk2_python', 'unitreerobotics/unitree_ros', 'unitreerobotics/unitree_ros2', 'unitreerobotics/unitree_rl_gym', 'unitreerobotics/unitree_rl_lab', 'unitreerobotics/unitree_mujoco', 'unitreerobotics/xr_teleoperate', 'unitreerobotics/unitree_lerobot', 'abizovnuralem/go2_ros2_sdk', 'HybridRobotics/berkeley-humanoid-lite', 'hshi74/toddlerbot', 'kscalelabs/kbot', 'poppy-project/poppy-humanoid', 'MyRobotLab/InMoov', 'BoosterRobotics/booster_robotics_sdk', 'FFTAI/fourier_aurora_sdk', 'AgibotTech/agibot_x1_infer', 'stanfordroboticsclub/StanfordQuadruped', 'Nate711/pupperv3-monorepo', 'PetoiCamp/OpenCat-Quadruped-Robot', 'PetoiCamp/OpenCatEsp32-Quadruped-Robot', 'open-dynamic-robot-initiative/solo', 'mit-biomimetics/Cheetah-Software', 'huggingface/lerobot', 'TheRobotStudio/SO-ARM100', 'jess-moss/koch-v1-1', 'tonyzhaozh/aloha', 'Interbotix/aloha', 'openvla/openvla', 'octo-models/octo', 'Physical-Intelligence/openpi', 'NVIDIA/Isaac-GR00T', 'google-deepmind/mujoco', 'google-deepmind/mujoco_playground', 'mujocolab/mjlab', 'isaac-sim/IsaacLab', 'Genesis-Embodied-AI/genesis-world', 'gazebosim/gz-sim', 'google/brax', 'leggedrobotics/legged_gym', 'mani-skill/ManiSkill', 'cyberbotics/webots', 'google-deepmind/mujoco_warp', 'ros2/ros2', 'moveit/moveit2', 'ros-navigation/navigation2', 'micro-ROS/micro_ros_setup', 'dora-rs/dora', 'stack-of-tasks/pinocchio', 'RobotLocomotion/drake', 'ros-controls/ros2_control']


def api(url, attempt=0):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": UA,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            data = json.load(res)
            remaining = res.headers.get("X-RateLimit-Remaining")
            reset = res.headers.get("X-RateLimit-Reset")
            return res.status, data, remaining, reset
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        remaining = e.headers.get("X-RateLimit-Remaining")
        reset = e.headers.get("X-RateLimit-Reset")
        if e.code in (429, 403) and attempt < 8:
            wait = 30
            if reset:
                wait = max(5, int(reset) - int(time.time()) + 3)
            wait = max(wait, min(120, 5 * (2 ** attempt)))
            print(f"rate limited ({e.code}) on {url}, sleeping {wait}s", flush=True)
            time.sleep(wait)
            return api(url, attempt + 1)
        if e.code in (500, 502, 503, 504) and attempt < 5:
            wait = min(60, 2 ** attempt)
            print(f"server error {e.code} on {url}, retry in {wait}s", flush=True)
            time.sleep(wait)
            return api(url, attempt + 1)
        return e.code, body, remaining, reset


def wait_for_budget(need):
    status, data, remaining, reset = api(f"{API}/rate_limit")
    if status != 200:
        print(f"rate_limit check failed: {status} {data}", flush=True)
        sys.exit(1)
    core = data["resources"]["core"]
    rem, rst = int(core["remaining"]), int(core["reset"])
    print(f"rate limit remaining={rem} reset={rst} need={need}", flush=True)
    if rem < need:
        wait = max(5, rst - int(time.time()) + 5)
        print(f"waiting {wait}s for rate limit reset", flush=True)
        time.sleep(wait)
        wait_for_budget(need)


def main():
    wait_for_budget(len(REPOS) + 2)
    rows = []
    missing = []
    for repo in REPOS:
        status, data, remaining, reset = api(f"{API}/repos/{repo}")
        if status == 404:
            print(f"MISSING {repo}", flush=True)
            missing.append(repo)
            continue
        if status != 200 or not isinstance(data, dict):
            print(f"ERROR {repo}: {status} {data}", flush=True)
            missing.append(repo)
            continue
        full = data.get("full_name") or repo
        stars = data["stargazers_count"]
        forks = data["forks_count"]
        lic_info = data.get("license")
        lic = lic_info["spdx_id"] if lic_info and lic_info.get("spdx_id") else "none"
        lang = data.get("language") or "none"
        pushed = (data.get("pushed_at") or "")[:10]
        archived = data.get("archived", False)
        print(
            f"{full}\t{stars}\t{forks}\t{lic}\t{lang}\t{pushed}\tarchived={archived}\trequested={repo}\tremaining={remaining}",
            flush=True,
        )
        rows.append(
            {
                "requested": repo,
                "full": full,
                "stars": stars,
                "forks": forks,
                "lic": lic,
                "lang": lang,
                "pushed": pushed,
                "archived": archived,
            }
        )
        time.sleep(0.15)

    with OUT.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for row in rows:
            w.writerow(
                [row["requested"], row["stars"], row["forks"], row["lic"], row["lang"], row["pushed"]]
            )
    print(f"\nwrote {OUT} ({len(rows)} rows, {len(missing)} missing: {missing})", flush=True)
    (ROOT / "stats.json").write_text(
        json.dumps({"rows": rows, "missing": missing}, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
