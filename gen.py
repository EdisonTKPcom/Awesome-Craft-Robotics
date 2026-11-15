#!/usr/bin/env python3
import csv
import urllib.parse as U
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S = {
    r[0]: dict(stars=int(r[1]), forks=int(r[2]), lic=r[3], lang=r[4], push=r[5])
    for r in csv.reader((ROOT / "stats.tsv").open(), delimiter="\t")
}
LICNAME = {"NOASSERTION": "Custom", "none": "None", "OTHER": "Custom"}
AS = "2026-11-15"
ACTIVE_SINCE = "2026-10-16"

# (name, repo, description) — descriptions include licence/archive/safety flags
C = [
    (
        "Microduck and Pollen Robotics",
        [
            ("Microduck", "pollen-robotics/microduck", "Rust runtime for Pollen Robotics' small biped, with onboard control daemons, updates and policy playback. The code is Apache-2.0. Pollen is Hugging Face's robotics team. The mechanical and electronic design files are not open source, per Pollen's press kit."),
            ("Microduck RL", "pollen-robotics/microduck_rl", "Reinforcement-learning environments for Microduck, built on mjlab and MuJoCo with PPO and sim-to-real export. The code is Apache-2.0, but the STL meshes are CC BY-NC-SA 4.0, which is not an OSI licence and bars commercial use of those models."),
            ("Microduck ROS 2 Isaac", "osrbot/microduck-ros2-isaac", "Community integration of the public Microduck model with ROS 2 Jazzy and NVIDIA Isaac Sim."),
            ("Microduck Simulator", "librezoo/microduck-simulator", "Browser simulator that runs Microduck-compatible policies in MuJoCo compiled to WebAssembly. The code is Apache-2.0, but the project's asset inventory still lists separately licensed and unresolved PENDING files, so the runnable distribution must not be described as wholly open source until those are cleared."),
            ("Open Duck Mini", "apirrone/Open_Duck_Mini", "Community open-source mini biped, with design, training and assembly resources. Last pushed on 2026-01-31."),
            ("Open Duck Mini Runtime", "apirrone/Open_Duck_Mini_Runtime", "Onboard runtime for Open Duck Mini, used to play trained policies on the robot. GitHub reports no SPDX licence, so read the repository before you use it. Running policies on hardware can injure people and damage the robot."),
            ("Reachy 2 SDK", "pollen-robotics/reachy2-sdk", "Official Python SDK for Pollen Robotics' Reachy 2 humanoid. The last push in this snapshot was 2025-11-26."),
            ("Reachy Mini", "pollen-robotics/reachy_mini", "SDK for Reachy Mini, Pollen Robotics' small expressive robot, with Python and JavaScript APIs and a MuJoCo simulation path. The software is Apache-2.0; the project's documentation says hardware design files use a non-commercial Creative Commons licence."),
        ],
    ),
    (
        "Unitree",
        [
            ("Go2 ROS 2 SDK", "abizovnuralem/go2_ros2_sdk", "Unofficial community ROS 2 SDK for Unitree Go2 Air, Pro and Edu robots, including sensor and navigation integrations. Not an official Unitree repository."),
            ("Unitree LeRobot", "unitreerobotics/unitree_lerobot", "Official Unitree fork of LeRobot for training and replaying data from the G1's dual-arm dexterous hands. This is the current name of the unitree_IL_lerobot project. GitHub reports no standard SPDX licence, so read the repository before you use it."),
            ("Unitree MuJoCo", "unitreerobotics/unitree_mujoco", "Official MuJoCo simulation and sim-to-sim path for Unitree robots."),
            ("Unitree RL Gym", "unitreerobotics/unitree_rl_gym", "Official reinforcement-learning environments for Go2, H1, H1_2 and G1, with sim-to-real deployment scripts. The last push in this snapshot was 2025-07-25; Unitree RL Lab is the more recently updated Isaac Lab counterpart. Deploying a trained policy on a physical robot can injure people and damage hardware."),
            ("Unitree RL Lab", "unitreerobotics/unitree_rl_lab", "Official reinforcement-learning implementation for Unitree robots, built on Isaac Lab."),
            ("Unitree ROS", "unitreerobotics/unitree_ros", "Official ROS 1 packages for Unitree robots."),
            ("Unitree ROS 2", "unitreerobotics/unitree_ros2", "Official ROS 2 packages for Unitree Go2, B2 and H1, using DDS-compatible messages."),
            ("Unitree SDK2", "unitreerobotics/unitree_sdk2", "Official C++ SDK version 2 for communicating with and controlling Unitree robots."),
            ("Unitree SDK2 Python", "unitreerobotics/unitree_sdk2_python", "Official Python interface for Unitree SDK2."),
            ("XR Teleoperate", "unitreerobotics/xr_teleoperate", "Official teleoperation stack for Unitree humanoids using XR devices. GitHub reports no standard SPDX licence, so read the repository before you use it."),
        ],
    ),
    (
        "Other humanoids and open hardware",
        [
            ("AgiBot X1 Infer", "AgibotTech/agibot_x1_infer", "Official inference module for AgiBot's X1 humanoid. GitHub reports no standard SPDX licence, so read the repository before you use it. The last push in this snapshot was 2025-04-03."),
            ("Berkeley Humanoid Lite", "HybridRobotics/berkeley-humanoid-lite", "Open-source, 3D-printable research humanoid from UC Berkeley, with policy training, simulation and real-robot deployment code."),
            ("Booster Robotics SDK", "BoosterRobotics/booster_robotics_sdk", "Official C++ SDK for Booster Robotics products. GitHub reports no standard SPDX licence, so read the repository before you use it."),
            ("Fourier Aurora SDK", "FFTAI/fourier_aurora_sdk", "Official Aurora SDK from Fourier Intelligence for its humanoid platforms. GitHub reports no standard SPDX licence, so read the repository before you use it."),
            ("InMoov", "MyRobotLab/InMoov", "Community software repository for the InMoov 3D-printable humanoid. GitHub reports no SPDX licence, so read the repository and the project's own terms before you use it. The last push in this snapshot was 2025-01-06."),
            ("K-Bot", "kscalelabs/kbot", "Open-source humanoid project from K-Scale Labs. The last push in this snapshot was 2025-11-07."),
            ("Poppy Humanoid", "poppy-project/poppy-humanoid", "Open-source, 3D-printed humanoid for research and education. GitHub reports no SPDX licence. This repository looks unmaintained, with the last push on 2021-12-06."),
            ("ToddlerBot", "hshi74/toddlerbot", "Open-source, low-cost machine-learning-oriented humanoid platform for loco-manipulation research."),
        ],
    ),
    (
        "Quadrupeds",
        [
            ("Cheetah-Software", "mit-biomimetics/Cheetah-Software", "Robot and simulation software for the MIT Mini Cheetah. This repository looks unmaintained, with the last push on 2023-10-18."),
            ("OpenCat", "PetoiCamp/OpenCat-Quadruped-Robot", "Official Petoi framework for OpenCat quadruped pets such as Bittle and Nybble, aimed at education and DIY kits."),
            ("OpenCat ESP32", "PetoiCamp/OpenCatEsp32-Quadruped-Robot", "Official ESP32-based OpenCat framework for current Petoi quadruped hardware."),
            ("Pupper v3", "Nate711/pupperv3-monorepo", "Open-source monorepo for Stanford Pupper v3, including ROS 2 code and neural-controller tooling."),
            ("Solo", "open-dynamic-robot-initiative/solo", "Low-level interface for the Open Dynamic Robot Initiative Solo torque-controlled quadruped. This repository looks unmaintained, with the last push on 2023-09-06."),
            ("Stanford Quadruped", "stanfordroboticsclub/StanfordQuadruped", "Software for the earlier Stanford Pupper servo quadruped. Last pushed on 2024-10-24; Pupper v3 is the later open codebase."),
        ],
    ),
    (
        "Arms and robot learning",
        [
            ("ALOHA", "tonyzhaozh/aloha", "Original low-cost bimanual teleoperation platform and software for ALOHA. This repository looks unmaintained, with the last push on 2024-04-19."),
            ("Isaac GR00T", "NVIDIA/Isaac-GR00T", "NVIDIA foundation-model stack for generalist robots. The repository code is Apache-2.0; model weights may use a separate NVIDIA licence, so read both before any commercial use."),
            ("Koch v1.1", "jess-moss/koch-v1-1", "Open design for the Alexander Koch low-cost leader-follower arm, used with LeRobot. Last pushed on 2024-09-17."),
            ("LeRobot", "huggingface/lerobot", "Hugging Face library for end-to-end robot learning, including dataset tools, training and real-robot policies. Deploying a policy on a physical arm can injure people and damage hardware."),
            ("Mobile ALOHA", "Interbotix/aloha", "Interbotix hardware and software package for the Mobile ALOHA bimanual mobile-manipulation platform. This repository looks unmaintained, with the last push on 2024-06-22."),
            ("Octo", "octo-models/octo", "Open transformer-based robot policy trained on a large mix of robot trajectories. This repository looks unmaintained, with the last push on 2024-07-31."),
            ("openpi", "Physical-Intelligence/openpi", "Physical Intelligence's open models and inference code for generalist robot policies, including π0 and related checkpoints."),
            ("OpenVLA", "openvla/openvla", "Open vision-language-action model for robotic manipulation. This repository looks unmaintained, with the last push on 2024-07-04."),
            ("SO-ARM100", "TheRobotStudio/SO-ARM100", "Standard Open Arm 100 hardware project, covering the SO-100 and later SO-101 low-cost arms used with LeRobot."),
        ],
    ),
    (
        "Simulation and RL",
        [
            ("Brax", "google/brax", "Massively parallel rigid-body physics simulator that runs on accelerator hardware."),
            ("Gazebo", "gazebosim/gz-sim", "Open-source robotics simulator from Open Robotics, the current Gazebo (gz-sim) line."),
            ("Genesis", "Genesis-Embodied-AI/genesis-world", "High-performance simulation platform for robotics and embodied AI. This is the current repository name for the Genesis project."),
            ("Isaac Lab", "isaac-sim/IsaacLab", "Unified robot-learning framework with multi-physics support. GitHub reports no SPDX identifier, but the repository LICENSE file is BSD-3-Clause. NVIDIA Isaac Sim itself is a separate product with its own terms."),
            ("legged_gym", "leggedrobotics/legged_gym", "Isaac Gym environments for legged robots, widely used as a training baseline. GitHub reports no standard SPDX licence, so read the repository and the Isaac Gym terms before you use it. Last pushed on 2025-05-29."),
            ("ManiSkill", "mani-skill/ManiSkill", "GPU-parallelised manipulation simulator and benchmark. This is the current organisation and repository after the move from haosulab."),
            ("mjlab", "mujocolab/mjlab", "Robot-learning framework that offers an Isaac Lab-style API on MuJoCo Warp, used to train Microduck and other policies."),
            ("MuJoCo", "google-deepmind/mujoco", "General-purpose multi-joint physics engine with contact, widely used for robot simulation and reinforcement learning."),
            ("MuJoCo Playground", "google-deepmind/mujoco_playground", "Open library of simulated and real-robot demos built on MuJoCo."),
            ("MuJoCo Warp", "google-deepmind/mujoco_warp", "GPU-optimised MuJoCo physics engine, designed for NVIDIA hardware."),
            ("Webots", "cyberbotics/webots", "Open-source robot simulator with a large library of ready-made robot models."),
        ],
    ),
    (
        "Middleware and stacks",
        [
            ("Dora", "dora-rs/dora", "Dataflow-oriented robotic middleware in Rust, aimed at low-latency AI robotics pipelines."),
            ("Drake", "RobotLocomotion/drake", "Model-based design and verification toolbox for robotics. GitHub reports no SPDX identifier; read the repository licence before you use it."),
            ("micro-ROS", "micro-ROS/micro_ros_setup", "Build support for running ROS 2 on microcontrollers."),
            ("MoveIt 2", "moveit/moveit2", "Motion planning, manipulation and control framework for ROS 2."),
            ("Nav2", "ros-navigation/navigation2", "ROS 2 navigation framework. GitHub reports no SPDX identifier; read the repository licence before you use it."),
            ("Pinocchio", "stack-of-tasks/pinocchio", "Fast rigid-body dynamics library with analytical derivatives."),
            ("ROS 2", "ros2/ros2", "Meta-repository for the Robot Operating System 2, the standard open robotics middleware. GitHub reports no SPDX licence on this tracker repository; the ROS 2 packages use their own licences, mostly Apache-2.0."),
            ("ros2_control", "ros-controls/ros2_control", "Generic controller framework for ROS 2, used to interface with real and simulated hardware."),
        ],
    ),
]


def k(n):
    if n >= 1e6:
        return f"{n/1e6:.2f}M"
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def anchor(n):
    return n.lower().replace(",", "").replace(" ", "-")


def fact(text):
    return f'<span class="ev-fact">{text}</span>'


def estimate(text):
    return f'<span class="ev-est">{text}</span>'


def goal(text):
    return f'<span class="ev-goal">{text}</span>'


def tesla_section():
    return f"""## Tesla Optimus

Tesla has not published open-source Optimus robot software. This snapshot found no official Optimus repository under Tesla's public GitHub organisation, [teslamotors](https://github.com/teslamotors). Unofficial projects that use the Optimus name are not Tesla code, and none are listed here.

What Tesla has published are company plans and characterisations. The [Q4 2025 Update](https://assets-ir.tesla.com/tesla-contents/IR/TSLA-Q4-2025-Update.pdf), an official Tesla investor-relations deck, said Tesla had "fine-tuned our production-primed Optimus design", planned to unveil {goal("Gen 3")} in {goal("Q1 2026")} as "our first design meant for mass production", and stated that {goal("start of production")} was {goal("planned before the end of 2026")}, with {goal("eventual planned capacity of 1 million robots per year")}. Those figures and dates are {goal("GOAL")}s: they are Tesla's plans, not independently measured production results. This snapshot did not verify later 2026 quarterly updates.

For open-source humanoid platforms, training stacks and simulators, see the sections below. They are independent projects, not Tesla software.

"""


RELATED = (
    "Related lists: "
    "[Awesome Craft](https://github.com/EdisonTKPcom/Awesome-Craft), "
    "[Awesome Craft AI](https://github.com/EdisonTKPcom/Awesome-Craft-AI), "
    "[Awesome Craft Agents](https://github.com/EdisonTKPcom/Awesome-Craft-Agents), "
    "[Awesome Craft CUDA](https://github.com/EdisonTKPcom/Awesome-Craft-CUDA), "
    "[Awesome Craft DevOps](https://github.com/EdisonTKPcom/Awesome-Craft-DevOps), "
    "[Awesome Craft EV](https://github.com/EdisonTKPcom/Awesome-Craft-EV), "
    "[Awesome Craft Hardware](https://github.com/EdisonTKPcom/Awesome-Craft-Hardware)."
)


tools = [t for _, ts in C for t in ts]
missing = [t[1] for t in tools if t[1] not in S]
if missing:
    raise SystemExit(f"missing stats for: {missing}")
dupes = [repo for repo in [t[1] for t in tools] if [t[1] for t in tools].count(repo) > 1]
if dupes:
    raise SystemExit(f"duplicate repos: {sorted(set(dupes))}")

tot = sum(S[t[1]]["stars"] for t in tools)
forks = sum(S[t[1]]["forks"] for t in tools)
langs = sorted({S[t[1]]["lang"] for t in tools if S[t[1]]["lang"] not in ("", "none")})
active = sum(1 for t in tools if S[t[1]]["push"] >= ACTIVE_SINCE)

o = []
o.append(
    f"""<div align="center">

# Awesome Craft Robotics [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of open-source robotics software and hardware, including Microduck, Unitree SDKs, open humanoids, arms, simulation and middleware.

<img src="assets/craft-robotics.svg" alt="Pixel-art robotics scene with a small biped duck, a quadruped dog and a humanoid walking past" width="100%">

![Tools](https://img.shields.io/badge/tools-{len(tools)}-6366f1?style=for-the-badge)
[![Categories](https://img.shields.io/badge/categories-{len(C)}-0ea5e9?style=for-the-badge)](#contents)
[![Combined stars](https://img.shields.io/badge/combined_stars-{k(tot)}-f59e0b?style=for-the-badge&logo=github)](#-leaderboard)
[![Stars](https://img.shields.io/github/stars/EdisonTKPcom/Awesome-Craft-Robotics?style=for-the-badge&color=22c55e)](https://github.com/EdisonTKPcom/Awesome-Craft-Robotics/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/EdisonTKPcom/Awesome-Craft-Robotics?style=for-the-badge&color=ec4899)](https://github.com/EdisonTKPcom/Awesome-Craft-Robotics/commits/main)

</div>

Open-source tools now cover a large part of the robotics stack: small bipeds such as Microduck, official and community SDKs for commercial quadrupeds and humanoids, research platforms you can build, robot-learning libraries, simulators and middleware. Every GitHub entry below was checked on {AS}. Check each project's licence before you train, manufacture, deploy or sell anything built on it.

**Safety:** learned policies and teleoperation stacks can move real robots with enough force to injure people or damage hardware. Test in simulation first, use a hoist or a clear workspace, keep an emergency stop within reach, and do not run an unverified policy on a robot that can reach a person. This list is not instructions, training or a substitute for that.

{RELATED}

## Contents
"""
)
o += ["- [Dashboard](#dashboard)"] + [f"- [{n}](#{anchor(n)})" for n, _ in C]
o += ["- [Tesla Optimus](#tesla-optimus)"]
o.append("\n## Dashboard\n")
o.append(
    f"""<style>
.ev-fact{{border-bottom:3px solid #0f172a;padding-bottom:1px}}
.ev-goal{{border-bottom:3px dashed #0f172a;padding-bottom:1px}}
.ev-est{{border-bottom:3px dotted #0f172a;padding-bottom:1px}}
</style>

<table>
<tr>
<td align="center"><h2>{fact(str(len(tools)))}</h2>listed projects</td>
<td align="center"><h2>{fact(str(len(C)))}</h2>categories</td>
<td align="center"><h2>{estimate(k(tot))}</h2>combined GitHub stars</td>
<td align="center"><h2>{estimate(k(forks))}</h2>combined forks</td>
<td align="center"><h2>{estimate(f"{active}/{len(tools)}")}</h2>pushed in the last 30 days</td>
<td align="center"><h2>{fact(str(len(langs)))}</h2>languages</td>
</tr>
</table>

**Evidence tags**

<table>
<tr><th>Tag</th><th>Style</th><th>Meaning</th></tr>
<tr><td><span class="ev-fact">FACT</span></td><td>solid underline</td><td>A measured figure, with the source named.</td></tr>
<tr><td><span class="ev-goal">GOAL</span></td><td>dashed underline</td><td>A stated roadmap, price, ship date or plan, not a result.</td></tr>
<tr><td><span class="ev-est">ESTIMATE</span></td><td>dotted underline</td><td>A sum or count we computed from the facts.</td></tr>
</table>

This snapshot's dashboard has no GOAL figures. None of the dashboard numbers come from project roadmaps. GOAL tags are used later for Microduck pricing and shipping claims, and for Tesla's published Optimus plans.

**Sources and method**

- Star counts, fork counts, licences, primary languages and last-push dates are {fact("FACT")} values from the GitHub REST API (`GET /repos/{{owner}}/{{repo}}`) on {AS}.
- Combined stars ({estimate(k(tot))}) and combined forks ({estimate(k(forks))}) are {estimate("ESTIMATE")}s: the arithmetic sum of those per-repository FACT counts, with no weighting and no unique-user deduplication. A person who stars two projects is counted twice.
- Pushed in the last 30 days ({estimate(f"{active}/{len(tools)}")}) is an {estimate("ESTIMATE")}: the number of listed repositories whose FACT `pushed_at` date is on or after {ACTIVE_SINCE}.
- Language and category counts, and the licence badges, are {estimate("ESTIMATE")}s of FACT fields. Star badges next to each entry update live and may differ from this snapshot.
"""
)
top = sorted(tools, key=lambda t: -S[t[1]]["stars"])[:10]
mx = S[top[0][1]]["stars"]
o.append(
    '### 🏆 Leaderboard\n\nStar counts in this table are FACT values from the snapshot. The bars are only a visual scale.\n\n<table>\n<tr><th>Rank</th><th>Project</th><th>Kind</th><th align="right">Stars</th><th></th></tr>'
)
kind = {t[1]: n for n, ts in C for t in ts}
for i, t in enumerate(top, 1):
    s = S[t[1]]["stars"]
    bar = "█" * max(1, round(s / mx * 20))
    medal = ["🥇", "🥈", "🥉"][i - 1] if i < 4 else i
    o.append(
        f'<tr><td align="center">{medal}</td><td><b>{t[0]}</b></td><td>{kind[t[1]]}</td><td align="right">{fact(k(s))}</td><td><code>{bar}</code></td></tr>'
    )
o.append("</table>\n")
o.append("\n### Stars by category\n")
o.append(
    "These category totals are ESTIMATE sums of the per-repository FACT star counts.\n\n```mermaid\npie showData\n    title Combined GitHub stars by category"
)
for n, ts in C:
    o.append(f'    "{n}" : {sum(S[t[1]]["stars"] for t in ts)}')
o.append("```\n")
lc = {}
for t in tools:
    L = LICNAME.get(S[t[1]]["lic"], S[t[1]]["lic"])
    lc[L] = lc.get(L, 0) + 1
o.append(
    "### Licences\n\n"
    + " ".join(
        f"![{L}](https://img.shields.io/badge/{U.quote(str(L).replace('-', '--'))}-{c}-64748b?style=flat-square)"
        for L, c in sorted(lc.items(), key=lambda x: -x[1])
    )
    + "\n\nThese badge counts are ESTIMATE tallies of the SPDX identifier GitHub returned for each repository. "
    + '"Custom" or "None" means GitHub could not match a standard SPDX licence. '
    + "Some projects also ship non-commercial or unresolved asset licences alongside OSI-licensed code, which are flagged in the entry. "
    + "Read each project licence before you use it commercially.\n"
)

# Microduck category intro with GOAL price/shipping
micro_intro = (
    f"Microduck is a small biped from Pollen Robotics, the Bordeaux robotics team at Hugging Face. "
    f"Pollen's [press kit](https://pollen-robotics.com/microduck/press-kit/) states an introductory price of {goal('$399')} before taxes and shipping, "
    f"with pre-orders opening on {fact('27 August 2026')} and {goal('first deliveries targeted before Christmas 2026')}. "
    f"[PCMag](https://uk.pcmag.com/ai/166941/meet-microduck-a-399-open-source-robot-that-can-learn-new-tricks) reported the same price and delivery target on {fact('27 August 2026')}. "
    f"The price and delivery window are {goal('GOAL')}s: they are stated offers and targets, not a confirmed shipment record. "
    f"The press kit also says the open-source claim covers the software stack, not the mechanical or electronic design files.\n"
)

for n, ts in C:
    o.append(f"## {n}\n")
    if n == "Microduck and Pollen Robotics":
        o.append(micro_intro)
    if n == "Unitree":
        o.append(
            "Official Unitree repositories are listed first by name, plus one widely used unofficial Go2 ROS 2 SDK. "
            "On 25 September 2025, [IEEE RAS](https://www.ieee-ras.org/news/exploit-allows-for-takeover-of-fleets-of-unitree-robots/) "
            "(updated 29 September 2025, relaying IEEE Spectrum) reported security issues affecting some Unitree Go2, B2, G1 and H1 platforms, "
            "and quoted a Unitree statement that it was working on fixes and firmware updates. "
            "This list does not document those issues. Keep firmware updated, review vendor advisories, and restrict how the robot is exposed on a network before you deploy.\n"
        )
    for t in ts:
        desc = t[2]
        if not desc.endswith("."):
            desc += "."
        o.append(
            f"- [{t[0]}](https://github.com/{t[1]}) - {desc} ![Stars](https://img.shields.io/github/stars/{t[1]}?style=flat-square&label=%E2%AD%90)"
        )
    o.append("")
o.append(tesla_section())
o.append(
    "## Contributing\n\nContributions welcome! Read the [contribution guidelines](contributing.md) first.\n\n"
    "### Star history\n\n"
    "[![Star History Chart](https://api.star-history.com/svg?repos=EdisonTKPcom/Awesome-Craft-Robotics&type=Date)](https://star-history.com/#EdisonTKPcom/Awesome-Craft-Robotics&Date)\n\n"
    '<div align="center">\n\n'
    "If this list helped you find a tool, give it a ⭐ so others can find it.\n\n"
    "</div>\n"
)
(ROOT / "README.md").write_text("\n".join(o))
print(
    f"wrote README.md tools={len(tools)} stars={tot} "
    f"forks={forks} langs={len(langs)} active={active}/{len(tools)}"
)
for n, ts in C:
    print(f"  {n}: {len(ts)}  stars={sum(S[t[1]]['stars'] for t in ts)}")
