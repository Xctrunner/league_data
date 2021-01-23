# medium term goal
# csv of matches with timestamp, patch, player names, their champs, their roles, their KDAs, their gold, match length, red/blue side, win/loss
#
# short term goal
# date, my champ, win/loss, match length

import cassiopeia as cass
from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue, Role
from collections import Counter
import pandas

with open('credentials.txt', 'r') as f:
    api_key = f.readline().strip()

def get_lane(map_id, p):
    if map_id == 12:
        return 'ARAM'
    if p.lane is None or (map_id != 1 and map_id != 2 and map_id != 11):
        return None
    if p.lane.value == 'BOT_LANE':
        if p.role == Role.duo_carry:
            return 'BOT'
        else:
            return 'SUPPORT'
    else:
        return p.lane.value

def participant_dict_to_list(games):
    return {game: [dic[game] for dic in games] for game in games[0]}

cass.set_riot_api_key(api_key)  # This overrides the value set in your configuration/settings.
cass.set_default_region('NA')
summoner = Summoner(name='DaftPunkRock', region='NA')
match_history = summoner.match_history
match_history(seasons={Season.season_9}, queues={Queue.normal_draft_fives})

champion_id_to_name_mapping = {champion.id: champion.name for champion in cass.get_champions(region='NA')}
played_champions = Counter()
dates = []
patches = []
my_champions = []
wins = []
match_lengths = []
participant_games = []
blue_red = []
for match in match_history[:100]:
    if match.id == 3744852102:
        break
# for _ in range(100):
    timestamp = match.creation
    dates.append(timestamp)
    patch = match.version
    patches.append(patch)
    participants_data = {}
    pcount = 0
    for p in match.participants:
        pstr = f'p{pcount}_'
        # print(dir(p))
        st = p.stats
        participant_data = {
            pstr + 'name': p.summoner.name, 
            pstr + 'champ': p.champion.name, 
            pstr + 'lane': get_lane(match.map.id, p), 
            pstr + 'kills': st.kills, 
            pstr + 'deaths': st.deaths, 
            pstr + 'assists': st.assists, 
            pstr + 'gold': st.gold_earned
        }
        # print(participant_data)
        participants_data.update(participant_data)
        pcount += 1
    participant_games.append(participants_data)
    champion_id = match.participants[summoner.name].champion.id
    champion_name = champion_id_to_name_mapping[champion_id]
    my_champions.append(champion_name)
    p = match.participants[summoner]
    blue_team = p.id in [x.id for x in match.blue_team.participants]
    blue_red.append('BLUE' if blue_team else 'RED')
    # print(blue_team)
    win = ('WIN' if blue_team == match.blue_team.win else 'LOSS')
    wins.append(win)
    game_length = match.duration
    match_lengths.append(game_length)
    #     print(timestamp)
    #     print(champion_name)
    #     print(win)
    #     print(match.duration)
    # print(f'blue_team: {blue_team}')
    # print(f'win: {win}')
    # print(dir(match.timeline))
    # print(match.timeline.frames)
    # print(dir(match.timeline.frames[-1]))
    # print(dir(match.timeline.frames[-1].events))
    # for event_data in match.timeline.frames[-1].events:
    #     print(dir(event_data))
    #     print(event_data.timestamp)
    #     # print(event_data.tower_type)
    #     # print(event_data.building_type)
    #     print(event_data.to_dict())
    # print(match.timeline.frames[-1].timestamp)
#     champion_id = match.participants[summoner.name].champion.id
#     champion_name = champion_id_to_name_mapping[champion_id]
#     played_champions[champion_name] += 1
p_lists = participant_dict_to_list(participant_games)
# print(p_lists)
short_game_dict = {'dates': dates, 'patches': patches, 'my_champions': my_champions, 'wins': wins, 'blue_red': blue_red, 'match_lengths': match_lengths}
short_game_dict.update(p_lists)
# print(short_game_dict)
columns = ['dates', 'patches', 'my_champions', 'wins', 'blue_red', 'match_lengths']
for i in range(10):
    pstr = f'p{i}_'
    section = [
        pstr + 'name', 
        pstr + 'champ', 
        pstr + 'lane', 
        pstr + 'kills', 
        pstr + 'deaths', 
        pstr + 'assists', 
        pstr + 'gold'
    ]
    # print(participant_data)
    columns.extend(section)
df = pandas.DataFrame(data=short_game_dict, columns=columns)
df.to_csv('short_game_sheet.csv')
    
# print('Length of match history:', len(match_history))

# print('Top 10 champions {} played:'.format(summoner.name))
# for champion_name, count in played_champions.most_common(10):
#     print(champion_name, count)
# print()