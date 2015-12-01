# balanced-teams

Genetic algorithm to create balanced relay teams based on mile times

## Purpose

Given the miles times of a team of people, we need to create N relay teams. Each
relay team should be equally balanced in times, so that they should all be
expected to finish around the same time. In addtion, we want to balance based on
number of players on each team and the number of players of each gender on each
team.

## Algorithm

We weight our desired balance metrics. If we weight one higher (like weighting
"time" heigher), we might lose balance in other catagories (like "gender").

We seed our algorithm with random teams of players, then score them based on our
weights. Next, we generate a new random set of teams by randomly moving a random
set of players to different teams. If the new seed is better scoring than the
first, we continue with that new seed.

## Requirements

Tested with Python 2.7

Requires numpy (for speed)

## How to run

 - Replace RUNNERS with the names, times, and genders of your team
 - Replace the constants section with your desired NUM_TEAMS
 - Replace your weights to get different results
 - Run with `python balanced_teams.py`

Increase or decrease running time by manipulating NUM_RUNS