# Produce a csv of a summoner's match history with timestamp, patch,
# red/blue side, win/loss, match duration, player names, their champs, their roles, 
# their KDAs, and their gold

import cassiopeia as cass
from cassiopeia import Summoner
from cassiopeia.data import Role
import pandas

SUMMONER_NAME = "xctrunner"
SUMMONER_REGION = "NA"
N_MATCHES = 100


def get_lane(map_id, summoner):
    if map_id == 12:
        return "ARAM"
    if summoner.lane is None or (map_id != 1 and map_id != 2 and map_id != 11):
        return None
    if summoner.lane.value == "BOT_LANE":
        if summoner.role == Role.duo_carry:
            return "BOT"
        else:
            return "SUPPORT"
    else:
        return summoner.lane.value


def make_row(match):

    row = {
        "date": match.creation,
        "patch": match.patch.majorminor,
        "duration": match.duration,
        "type": match.queue.name,

    }

    for i, participant in enumerate(match.participants):
        pstr = f"p{i}_"
        st = participant.stats
        participant_data = {
            pstr + "name": participant.summoner.name, 
            pstr + "champ": participant.champion.name,
            pstr + "side": participant.side.name,
            pstr + "win": st.win,
            pstr + "lane": get_lane(match.map.id, participant),
            pstr + "kills": st.kills,
            pstr + "deaths": st.deaths,
            pstr + "assists": st.assists,
            pstr + "damage": st.total_damage_dealt_to_champions,
            pstr + "vision": st.vision_score,
            pstr + "gold": st.gold_earned,
        }
        row.update(participant_data)
    
    return row


with open("credentials.txt", "r") as f:
    api_key = f.readline().strip()
cass.set_riot_api_key(api_key)
cass.set_default_region(SUMMONER_REGION)

champion_id_to_name_mapping = {champion.id: champion.name for champion in cass.get_champions(region="NA")}

summoner = Summoner(name=SUMMONER_NAME, region=SUMMONER_REGION)
match_history = summoner.match_history

data_list = []
for match in match_history[:N_MATCHES]:
    try:    
        row = make_row(match)
        data_list.append(row)
    except Exception as e:
        print(f"Issue with match {match.id} from {match.creation}. {e}")
        continue

df = pandas.DataFrame(data=data_list)
df.to_csv(f"{summoner.name}_match_history_{N_MATCHES}.csv", index=False)
