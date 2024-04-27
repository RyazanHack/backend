from config import ALL_DATA, DISTRICTS_WITH_AREA


def stage_one(regions: list):
    all_districts = {district["name"]: [] for district in ALL_DATA}
    one_stage_regions_winner = []
    for region, value in regions:
        for district in DISTRICTS_WITH_AREA.keys():
            if (
                region in DISTRICTS_WITH_AREA[district]
                and len(all_districts[district]) < 3
            ):
                all_districts[district].append([region, value])
                one_stage_regions_winner.append(region)
                break
    return one_stage_regions_winner, all_districts
