from __future__ import division

import copy
import numpy
import random
import re

RUNNERS = [
  ["Adam", "0:05:47", "M"],
  ["Ali", "0:06:38", "F"],
  ["Andrew", "0:06:55", "M"],
  ["Blonde Megan", "0:08:38", "F"],
  # ["Brian", "0:06:43", "M"],
  # ["Brian Tall", "0:06:24", "M"],
  # ["Collin", "0:06:14", "M"],
  # ["Dave", "0:06:01", "M"],
  # ["Dylan", "0:06:43", "M"],
  # ["Jake", "0:06:55", "M"],
  ["James", "0:07:51", "M"],
  ["Jason", "0:07:27", "M"],
  ["Jdao", "0:07:34", "M"],
  ["Jimbo", "0:07:51", "M"],
  ["Joe", "0:07:03", "M"],
  ["John", "0:07:15", "M"],
  ["Lauren", "0:08:09", "F"],
  ["Mark", "0:07:18", "M"],
  ["Matt", "0:05:54", "M"],
  ["Meaghan Creamer", "0:06:53", "F"],
  ["Ncik", "0:06:24", "M"],
  ["Nick", "0:06:21", "M"],
  ["Nicole", "0:08:38", "F"],
  ["Olivia", "0:07:25", "F"],
  ["Parks", "0:07:44", "M"],
  ["Poot", "0:07:19", "M"],
  ["Sam Tall", "0:05:23", "M"],
  ["Shaundry", "0:08:30", "F"],
  ["Tommy Doug", "0:05:48", "M"],
  ["Tucker", "0:07:10", "M"]
]

NUM_TEAMS = 4
NUM_RUNS = 5000

# Statistic weights
TIME_WEIGHT = 1
TEAM_SIZE_WEIGHT = 10
GENDER_WEIGHT = 100


class Player(object):
  def __init__(self, name, time_string, gender):
    self.name = name
    self.time_string = time_string
    self.gender = gender

  @staticmethod
  def _get_numeric_time(time):
    """time is of the form "H:MM:SS". We convert to total seconds"""
    _, minutes, seconds = map(int, re.split(":", time))
    return minutes * 60 + seconds

  def get_time(self):
    return self._get_numeric_time(self.time_string)

  def is_male(self):
    return self.gender == "M"


class Team(set):
  def __str__(self):
    return("  Time: {}. {} players, {} male: {}".format(
      self.total_time(), len(self), self.num_males(),
      ", ".join([player.name for player in self])))

  def total_time(self):
    return sum([player.get_time() for player in self])

  def num_males(self):
    return len([player for player in self if player.is_male()])


class Solution(object):
  def __init__(self):
    self.teams = []
    for _ in range(NUM_TEAMS):
      self.teams.append(Team())

  def fitness_score(self):
    # We use the measures of three variances to determine our score:
    #  - total team mile time
    #  - num males on the team
    #  - team size
    # 
    # The lowest score will be the one that does the best at minimizing the
    # difference between teams in these catagories.
    time_variance = numpy.var([team.total_time() for team in self.teams])
    team_size_variance = numpy.var([len(team) for team in self.teams])
    gender_variance = numpy.var([team.num_males() for team in self.teams])
    return(time_variance * TIME_WEIGHT + team_size_variance * TEAM_SIZE_WEIGHT
           + gender_variance * GENDER_WEIGHT)

  def add_player_to_random_team(self, player):
    random.choice(self.teams).add(player)

  def change_random_player(self):
    old_team = random.choice(self.teams)
    if len(old_team) == 0:
      print "empty team"
      return
    player = random.sample(old_team, 1)[0]
    old_team.remove(player)
    new_team = random.choice(self.teams)
    new_team.add(player)

  def __str__(self):
    return "\n".join(map(str, self.teams))


def main():
  initial_solution = Solution()
  for name, time, gender in RUNNERS:
    initial_solution.add_player_to_random_team(Player(name, time, gender))
  print("Splitting {} players ({} male) into {} teams".format(
    len(RUNNERS), len([runner for runner in RUNNERS if runner[2] == "M"]),
    NUM_TEAMS))
  print("Starting with solution score {:.2f}:\n{}".format(
    initial_solution.fitness_score(), initial_solution))

  for run_num in range(NUM_RUNS):
    if run_num % 1000 == 0:
      print("Current best solution with score {:.2f}:\n{}".format(
        initial_solution.fitness_score(), initial_solution))
    solution = copy.deepcopy(initial_solution)
    for _ in range(random.randint(1, 10)):
      solution.change_random_player()
    if solution.fitness_score() < initial_solution.fitness_score():
      initial_solution = solution

  print("Best solution found, with solution score {:.2f}:\n{}".format(
    initial_solution.fitness_score(), initial_solution))


if __name__ == "__main__":
  main()
