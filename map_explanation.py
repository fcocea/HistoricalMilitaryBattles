from dash_manager import app
from dash import Output, Input, State, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from collections import Counter


def render_war(data):
    data_key = list(data.keys())
    parsed_data = {}
    conflict_counter = {}
    # print(data)
    for key in data_key:
        for battle in data[key]:
            if key not in parsed_data:
                parsed_data[key] = {}
            if key not in conflict_counter:
                conflict_counter[key] = {}
            attacker_defender = tuple(
                sorted((battle['attacker'], battle['defender'])))
            if battle['location'] not in parsed_data[key]:
                parsed_data[key][battle['location']] = {}
            if battle['location'] not in conflict_counter[key]:
                conflict_counter[key][battle['location']] = {}
            if attacker_defender not in conflict_counter[key][battle['location']]:
                conflict_counter[key][battle['location']
                                      ][attacker_defender] = Counter()
            conflict_counter[key][battle['location']
                                  ][attacker_defender].update([battle['attacker']])

            if attacker_defender not in parsed_data[key][battle['location']]:
                parsed_data[key][battle['location']][attacker_defender] = []
            parsed_data[key][battle['location']][attacker_defender].append(
                battle)
    new_parsed = {}

    for war in parsed_data:
        for location in parsed_data[war]:
            for conflict in parsed_data[war][location]:
                mostConflictive = conflict_counter[war][location][conflict].most_common(1)[
                    0][0]
                if war not in new_parsed:
                    new_parsed[war] = {}
                if location not in new_parsed[war]:
                    new_parsed[war][location] = {}
                if conflict not in new_parsed[war][location]:
                    new_parsed[war][location][conflict] = {}
                new_parsed[war][location][conflict] = {
                    'mostConflictive': mostConflictive,
                    'mostConflictiveTimes': conflict_counter[war][location][conflict][mostConflictive],
                    'conflictiveWins': len(
                        [battle for battle in parsed_data[war][location][conflict] if battle['winner'] == mostConflictive]),
                    'conflictiveDraws': len(
                        [battle for battle in parsed_data[war][location][conflict] if battle['winner'] == 'Empate']),
                    'conflictiveDefeats': len(
                        [battle for battle in parsed_data[war][location][conflict] if battle['winner'] != mostConflictive and battle['winner'] != 'Empate']),
                    'totalBattles': len(parsed_data[war][location][conflict]),
                    'defender': conflict[0] if conflict[0] != mostConflictive else conflict[1],
                }
    listToRender = {}
    for key in data_key:
        listToRender[key] = []
        for location in new_parsed[key]:
            for conflict in new_parsed[key][location]:
                total = new_parsed[key][location][conflict]['totalBattles']
                conflictivo = new_parsed[key][location][conflict]['mostConflictive']
                veces = new_parsed[key][location][conflict]['mostConflictiveTimes']
                defender = new_parsed[key][location][conflict]['defender']
                wins = new_parsed[key][location][conflict]['conflictiveWins']
                draws = new_parsed[key][location][conflict]['conflictiveDraws']
                defeats = new_parsed[key][location][conflict]['conflictiveDefeats']
                t = f'{conflictivo} atacó a {defender} {f" en" + " el único conflicto de esta guerra" if veces == 1 else f" los {veces} conflictos" + "que tuvieron" if veces == total else f"{veces} de las {total} batallas" if veces != 1 else f"en el único conflicto de esta guerra,"} en {location}'
                t += f'{wins == total and f", ganando todas las batallas" or f", ganando {wins} batallas" if wins > 0 else ""}'
                t += f'{draws == total and ", empatando todas las batallas" or f", empatando {draws} batallas" if draws > 0 else ""}'
                t += f'{defeats == total and ", perdiendo todas las batallas" or f", perdiendo {defeats} batallas" if defeats > 0 else ""}'
                listToRender[key].append(t)
    return dmc.Accordion(
        disableChevronRotation=True,
        value=data_key[0],
        children=[
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(
                        key,
                        icon=DashIconify(
                            icon="game-icons:battle-tank",
                            color=dmc.DEFAULT_THEME["colors"]["gray"][6],
                            width=22,
                        ),
                    ),
                    dmc.AccordionPanel(
                        [dmc.List([dmc.ListItem([dmc.Text(text)]) for text in listToRender[key]])]),
                ],
                value=key,
            ) for key in data_key
        ])


@ app.callback(
    [Output('map-explanation', 'children')],
    [Input('map-data', 'data')]


)
def map_explanation(data):
    total_battles = 0
    if data is not None:
        for item in data['battles']:
            for key in item:
                total_battles += len(item[key])
    parsed_data = {}
    if data is not None:
        for item in data['battles']:
            for key in item:
                if key not in parsed_data:
                    parsed_data[key] = []
                parsed_data[key] += item[key]

    body = [
        dmc.Title(
            f"Batallas en el año {data['year'] if data is not None else 1689}", order=3, ml='auto', mr='auto'),
    ]

    body += [
        dmc.Loader(size="md", variant="oval", m='auto')
    ] if data is None else [
        dmc.Text(
            f"El mapa muestra {f'las {total_battles} batallas ocurridas' if total_battles > 1 else 'la única batalla ocurrida'} en el año {data['year']}. "
            "Cada punto representa la ubicación en donde ocurrió la batalla, además de indicar entre quiénes se llevó a cabo, y la cantidad de batallas en ese lugar.",
        ),
        dmc.Divider(variant="solid")] + [render_war(parsed_data)]
    return [
        dmc.Flex(
            body, direction="column", gap="xs", h='100%')
    ]
