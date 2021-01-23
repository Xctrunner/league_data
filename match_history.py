import cassiopeia as cass
from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue
from collections import Counter

cass.set_riot_api_key("RGAPI-00f1ddd1-d709-4272-8249-3032d2f29cb0")  # This overrides the value set in your configuration/settings.
cass.set_default_region("NA")
summoner = Summoner(name="DaftPunkRock", region="NA")
match_history = summoner.match_history
match_history(seasons={Season.season_9}, queues={Queue.normal_draft_fives})

champion_id_to_name_mapping = {champion.id: champion.name for champion in cass.get_champions(region="NA")}
played_champions = Counter()
for match in match_history:
    champion_id = match.participants[summoner.name].champion.id
    champion_name = champion_id_to_name_mapping[champion_id]
    played_champions[champion_name] += 1
print("Length of match history:", len(match_history))

print("Top 10 champions {} played:".format(summoner.name))
for champion_name, count in played_champions.most_common(10):
    print(champion_name, count)
print()