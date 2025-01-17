import json
import networkx as nx
from matplotlib import pyplot as plt
import community.community_louvain as community_louvain

# Load the JSON dataset
with open('congress_network_data.json', 'r') as f:
    data = json.load(f)

# Extract data from JSON
inList = data[0]['inList']
inWeight = data[0]['inWeight']
outList = data[0]['outList']
outWeight = data[0]['outWeight']
usernameList = data[0]['usernameList']

# Manually add party affiliation (example data)
partyAffiliation = {
    'SenatorBaldwin': 'Democratic',
    'SenJohnBarrasso': 'Republican',
    'SenatorBennet': 'Democratic',
    'MarshaBlackburn': 'Republican',
    'SenBlumenthal': 'Democratic',
    'RoyBlunt': 'Republican',
    'CoryBooker': 'Democratic',
    'JohnBoozman': 'Republican',
    'SenatorBraun': 'Republican',
    'SenSherrodBrown': 'Democratic',
    'SenatorCantwell': 'Democratic',
    'SenCapito': 'Republican',
    'SenatorCardin': 'Democratic',
    'SenatorCarper': 'Democratic',
    'SenBobCasey': 'Democratic',
    'SenBillCassidy': 'Republican',
    'ChrisCoons': 'Democratic',
    'JohnCornyn': 'Republican',
    'SenCortezMasto': 'Democratic',
    'SenTomCotton': 'Republican',
    'SenKevinCramer': 'Republican',
    'MikeCrapo': 'Republican',
    'SenTedCruz': 'Republican',
    'SteveDaines': 'Republican',
    'SenDuckworth': 'Democratic',
    'SenatorDurbin': 'Democratic',
    'SenJoniErnst': 'Republican',
    'SenFeinstein': 'Democratic',
    'SenatorFischer': 'Republican',
    'SenGillibrand': 'Democratic',
    'LindseyGrahamSC': 'Republican',
    'ChuckGrassley': 'Republican',
    'SenatorHagerty': 'Republican',
    'SenatorHassan': 'Democratic',
    'HawleyMO': 'Republican',
    'MartinHeinrich': 'Democratic',
    'SenatorHick': 'Democratic',
    'maziehirono': 'Democratic',
    'SenJohnHoeven': 'Republican',
    'SenHydeSmith': 'Republican',
    'JimInhofe': 'Republican',
    'SenRonJohnson': 'Republican',
    'timkaine': 'Democratic',
    'SenMarkKelly': 'Democratic',
    'SenJohnKennedy': 'Republican',
    'SenAngusKing': None,  # Independent
    'SenAmyKlobuchar': 'Democratic',
    'SenatorLankford': 'Republican',
    'SenatorLeahy': 'Democratic',
    'SenMikeLee': 'Republican',
    'SenatorLujan': 'Democratic',
    'SenLummis': 'Republican',
    'Sen_JoeManchin': 'Democratic',
    'SenMarkey': 'Democratic',
    'SenatorMenendez': 'Democratic',
    'SenJeffMerkley': 'Democratic',
    'JerryMoran': 'Republican',
    'lisamurkowski': 'Republican',
    'ChrisMurphyCT': 'Democratic',
    'PattyMurray': 'Democratic',
    'ossoff': 'Democratic',
    'SenAlexPadilla': 'Democratic',
    'RandPaul': 'Republican',
    'SenGaryPeters': 'Democratic',
    'senrobportman': 'Republican',
    'SenJackReed': 'Democratic',
    'SenatorRisch': 'Republican',
    'SenatorRomney': 'Republican',
    'SenJackyRosen': 'Democratic',
    'marcorubio': 'Republican',
    'SenSanders': None,  # Independent
    'SenSchumer': 'Democratic',
    'SenRickScott': 'Republican',
    'SenatorTimScott': 'Republican',
    'SenatorShaheen': 'Democratic',
    'SenatorSinema': 'Democratic',
    'SenTinaSmith': 'Democratic',
    'SenStabenow': 'Democratic',
    'SenDanSullivan': 'Republican',
    'SenatorTester': 'Democratic',
    'SenJohnThune': 'Republican',
    'SenThomTillis': 'Republican',
    'SenToomey': 'Republican',
    'SenTuberville': 'Republican',
    'ChrisVanHollen': 'Democratic',
    'MarkWarner': 'Democratic',
    'SenatorWarnock': 'Democratic',
    'SenWarren': 'Democratic',
    'SenWhitehouse': 'Democratic',
    'SenatorWicker': 'Republican',
    'RonWyden': 'Democratic',
    'SenToddYoung': 'Republican',
    'RepAdams': 'Democratic',
    'Robert_Aderholt': 'Republican',
    'RepPeteAguilar': 'Democratic',
    'RepRickAllen': 'Republican',
    'RepColinAllred': 'Democratic',
    'MarkAmodeiNV2': 'Republican',
    'RepArmstrongND': 'Republican',
    'RepArrington': 'Republican',
    'RepAuchincloss': 'Democratic',
    'RepCindyAxne': 'Democratic',
    'RepBrianBabin': 'Republican',
    'RepDonBacon': 'Republican',
    'RepJimBaird': 'Republican',
    'RepBalderson': 'Republican',
    'RepJimBanks': 'Republican',
    'RepAndyBarr': 'Republican',
    'RepBarragan': 'Democratic',
    'RepKarenBass': 'Democratic',
    'RepBeatty': 'Democratic',
    'RepBera': 'Democratic',
    'RepDonBeyer': 'Democratic',
    'RepBice': 'Republican',
    'RepAndyBiggsAZ': 'Republican',
    'RepGusBilirakis': 'Republican',
    'SanfordBishop': 'Democratic',
    'RepDanBishop': 'Republican',
    'RepLBR': 'Democratic',
    'RepBoebert': 'Republican',
    'RepBonamici': 'Democratic',
    'RepBost': 'Republican',
    'RepBourdeaux': 'Democratic',
    'RepBowman': 'Democratic',
    'CongBoyle': 'Democratic',
    'RepKevinBrady': 'Republican',
    'RepMoBrooks': 'Republican',
    'RepAnthonyBrown': 'Democratic',
    'RepShontelBrown': 'Democratic',
    'RepBrownley': 'Democratic',
    'VernBuchanan': 'Republican',
    'RepKenBuck': 'Republican',
    'RepLarryBucshon': 'Republican',
    'RepTedBudd': 'Republican',
    'RepTimBurchett': 'Republican',
    'michaelcburgess': 'Republican',
    'RepCori': 'Democratic',
    'RepCheri': 'Democratic',
    'RepKatCammack': 'Republican',
    'RepCarbajal': 'Democratic',
    'RepCardenas': 'Democratic',
    'RepMikeCarey': 'Republican',
    'RepJerryCarl': 'Republican',
    'RepAndreCarson': 'Democratic',
    'RepBuddyCarter': 'Republican',
    'JudgeCarter': 'Republican',
    'RepTroyCarter': 'Democratic',
    'RepEdCase': 'Democratic',
    'RepCasten': 'Democratic',
    'USRepKCastor': 'Democratic',
    'JoaquinCastrotx': 'Democratic',
    'RepCawthorn': 'Republican',
    'RepSteveChabot': 'Republican',
    'RepLizCheney': 'Republican',
    'CongresswomanSC': 'Democratic',
    'RepJudyChu': 'Democratic',
    'RepKClark': 'Democratic',
    'RepYvetteClarke': 'Democratic',
    'repcleaver': 'Democratic',
    'RepBenCline': 'Republican',
    'RepCloudTX': 'Republican',
    'WhipClyburn': 'Democratic',
    'Rep_Clyde': 'Republican',
    'RepCohen': 'Democratic',
    'TomColeOK04': 'Republican',
    'RepJamesComer': 'Republican',
    'GerryConnolly': 'Democratic',
    'RepLouCorrea': 'Democratic',
    'RepJimCosta': 'Democratic',
    'RepJoeCourtney': 'Democratic',
    'RepAngieCraig': 'Democratic',
    'RepCharlieCrist': 'Democratic',
    'RepJasonCrow': 'Democratic',
    'RepJohnCurtis': 'Republican',
    'RepDavids': 'Democratic',
    'WarrenDavidson': 'Republican',
    'RodneyDavis': 'Republican',
    'RepDean': 'Democratic',
    'RepPeterDeFazio': 'Democratic',
    'RepDianaDeGette': 'Democratic',
    'rosadelauro': 'Democratic',
    'RepDelBene': 'Democratic',
    'repdelgado': 'Democratic',
    'RepValDemings': 'Democratic',
    'RepDeSaulnier': 'Democratic',
    'RepTedDeutch': 'Democratic',
    'MarioDB': 'Republican',
    'RepDebDingell': 'Democratic',
    'RepLloydDoggett': 'Democratic',
    'RepDonaldsPress': 'Republican',
    'USRepMikeDoyle': 'Democratic',
    'RepJeffDuncan': 'Republican',
    'DrNealDunnFL2': 'Republican',
    'RepTomEmmer': 'Republican',
    'RepEscobar': 'Democratic',
    'RepAnnaEshoo': 'Democratic',
    'RepEspaillat': 'Democratic',
    'RepRonEstes': 'Republican',
    'RepDwightEvans': 'Democratic',
    'RepPatFallon': 'Republican',
    'RepFeenstra': 'Republican',
    'RepDrewFerguson': 'Republican',
    'RepFischbach': 'Republican',
    'RepBrianFitz': 'Democratic',
    'RepChuck': 'Democratic',
    'RepFletcher': 'Democratic',
    'RepBillFoster': 'Democratic',
    'virginiafoxx': 'Republican',
    'RepLoisFrankel': 'Democratic',
    'RepFranklin': 'Republican',
    'RepRussFulcher': 'Republican',
    'RepMattGaetz': 'Republican',
    'RepGallagher': 'Republican',
    'RepRubenGallego': 'Democratic',
    'RepGaramendi': 'Democratic',
    'RepGarbarino': 'Republican',
    'RepChuyGarcia': 'Democratic',
    'RepMikeGarcia': 'Republican',
    'RepSylviaGarcia': 'Democratic',
    'RepBobGibbs': 'Republican',
    'RepCarlos': 'Democratic',
    'replouiegohmert': 'Republican',
    'RepGolden': 'Democratic',
    'RepJimmyGomez': 'Democratic',
    'RepTonyGonzales': 'Republican',
    'RepJenniffer': 'Democratic',
    'RepGonzalez': 'Democratic',
    'RepBobGood': 'Republican',
    'Lancegooden': 'Republican',
    'RepGosar': 'Republican',
    'RepJoshG': 'Democratic',
    'RepKayGranger': 'Republican',
    'RepGarretGraves': 'Republican',
    'RepAlGreen': 'Democratic',
    'RepMarkGreen': 'Republican',
    'RepMTG': 'Republican',
    'RepMGriffith': 'Republican',
    'RepRaulGrijalva': 'Democratic',
    'RepGrothman': 'Republican',
    'RepMichaelGuest': 'Republican',
    'RepGuthrie': 'Republican',
    'RepJoshHarder': 'Democratic',
    'RepHarshbarger': 'Republican',
    'RepHartzler': 'Republican',
    'RepJahanaHayes': 'Democratic',
    'repkevinhern': 'Republican',
    'RepHerrell': 'Republican',
    'CongressmanHice': 'Republican',
    'RepBrianHiggins': 'Democratic',
    'RepClayHiggins': 'Republican',
    'RepFrenchHill': 'Republican',
    'jahimes': 'Democratic',
    'RepAshleyHinson': 'Republican',
    'RepHorsford': 'Democratic',
    'RepHoulahan': 'Democratic',
    'LeaderHoyer': 'Democratic',
    'RepRichHudson': 'Republican',
    'RepHuffman': 'Democratic',
    'RepHuizenga': 'Republican',
    'repdarrellissa': 'Republican',
    'JacksonLeeTX18': 'Democratic',
    'RepRonnyJackson': 'Republican',
    'RepJacobs': 'Republican',
    'RepSaraJacobs': 'Democratic',
    'RepJayapal': 'Democratic',
    'RepJeffries': 'Democratic',
    'RepBillJohnson': 'Republican',
    'RepDustyJohnson': 'Republican',
    'RepEBJ': 'Democratic',
    'RepHankJohnson': 'Democratic',
    'RepMikeJohnson': 'Republican',
    'RepMondaire': 'Democratic',
    'Jim_Jordan': 'Republican',
    'RepDaveJoyce': 'Republican',
    'RepJohnJoyce': 'Republican',
    'RepJohnKatko': 'Republican',
    'USRepKeating': 'Democratic',
    'RepFredKeller': 'Republican',
    'MikeKellyPA': 'Republican',
    'RepRobinKelly': 'Democratic',
    'RepRoKhanna': 'Democratic',
    'RepDanKildee': 'Democratic',
    'RepDerekKilmer': 'Democratic',
    'RepAndyKimNJ': 'Democratic',
    'RepYoungKim': 'Republican',
    'RepRonKind': 'Democratic',
    'RepKirkpatrick': 'Democratic',
    'CongressmanRaja': 'Democratic',
    'RepAnnieKuster': 'Democratic',
    'RepDavidKustoff': 'Republican',
    'RepLaHood': 'Republican',
    'RepLaMalfa': 'Republican',
    'JimLangevin': 'Democratic',
    'RepRickLarsen': 'Democratic',
    'RepJohnLarson': 'Democratic',
    'boblatta': 'Republican',
    'RepLaTurner': 'Republican',
    'RepLawrence': 'Democratic',
    'RepAlLawsonJr': 'Democratic',
    'RepBarbaraLee': 'Democratic',
    'RepSusieLee': 'Democratic',
    'RepTeresaLF': 'Democratic',
    'RepDLesko': 'Republican',
    'RepJuliaLetlow': 'Republican',
    'RepAndyLevin': 'Democratic',
    'RepMikeLevin': 'Democratic',
    'RepTedLieu': 'Democratic',
    'USRepLong': 'Republican',
    'RepLoudermilk': 'Republican',
    'RepLowenthal': 'Democratic',
    'RepFrankLucas': 'Republican',
    'RepBlaine': 'Republican',
    'RepElaineLuria': 'Democratic',
    'RepNancyMace': 'Republican',
    'RepMalinowski': 'Democratic',
    'RepMalliotakis': 'Republican',
    'RepMaloney': 'Democratic',
    'RepSeanMaloney': 'Democratic',
    'RepKManning': 'Democratic',
    'RepThomasMassie': 'Republican',
    'RepBrianMast': 'Republican',
    'DorisMatsui': 'Democratic',
    'RepLucyMcBath': 'Democratic',
    'GOPLeader': 'Republican',
    'RepMcCaul': 'Republican',
    'RepLisaMcClain': 'Republican',
    'BettyMcCollum04': 'Democratic',
    'RepMcEachin': 'Democratic',
    'RepMcGovern': 'Democratic',
    'PatrickMcHenry': 'Republican',
    'RepMcKinley': 'Republican',
    'RepGregoryMeeks': 'Democratic',
    'RepMeijer': 'Republican',
    'RepGraceMeng': 'Democratic',
    'RepMeuser': 'Republican',
    'RepKweisiMfume': 'Democratic',
    'RepMMM': 'Democratic',
    'RepCarolMiller': 'Republican',
    'RepMaryMiller': 'Republican',
    'RepAlexMooney': 'Republican',
    'RepBarryMoore': 'Republican',
    'RepBlakeMoore': 'Republican',
    'RepGwenMoore': 'Democratic',
    'RepJoeMorelle': 'Democratic',
    'RepMullin': 'Republican',
    'RepGregMurphy': 'Republican',
    'RepStephMurphy': 'Democratic',
    'RepJerryNadler': 'Democratic',
    'gracenapolitano': 'Democratic',
    'RepRichardNeal': 'Democratic',
    'RepJoeNeguse': 'Democratic',
    'RepTroyNehls': 'Republican',
    'RepNewhouse': 'Republican',
    'RepMarieNewman': 'Democratic',
    'DonaldNorcross': 'Democratic',
    'RepRalphNorman': 'Republican',
    'EleanorNorton': 'Democratic',
    'RepOHalleran': 'Democratic',
    'JayObernolte': 'Republican',
    'Ilhan': 'Democratic',
    'RepBurgessOwens': 'Republican',
    'CongPalazzo': 'Republican',
    'FrankPallone': 'Democratic',
    'USRepGaryPalmer': 'Republican',
    'RepJimmyPanetta': 'Democratic',
    'RepChrisPappas': 'Democratic',
    'BillPascrell': 'Democratic',
    'RepDonaldPayne': 'Democratic',
    'SpeakerPelosi': 'Democratic',
    'RepPerlmutter': 'Democratic',
    'RepScottPeters': 'Democratic',
    'RepPfluger': 'Republican',
    'RepDeanPhillips': 'Democratic',
    'chelliepingree': 'Democratic',
    'StaceyPlaskett': 'Democratic',
    'repmarkpocan': 'Democratic',
    'RepKatiePorter': 'Democratic',
    'RepPressley': 'Democratic',
    'RepDavidEPrice': 'Democratic',
    'RepMikeQuigley': 'Democratic',
    'RepRaskin': 'Democratic',
    'GReschenthaler': 'Republican',
    'RepKathleenRice': 'Democratic',
    'RepTomRice': 'Republican',
    'cathymcmorris': 'Republican',
    'RepMikeRogersAL': 'Republican',
    'RepJohnRose': 'Republican',
    'RepRosendale': 'Republican',
    'RepDeborahRoss': 'Democratic',
    'RepDavidRouzer': 'Republican',
    'RepChipRoy': 'Republican',
    'RepRoybalAllard': 'Democratic',
    'RepRaulRuizMD': 'Democratic',
    'Call_Me_Dutch': 'Democratic',
    'RepBobbyRush': 'Democratic',
    'RepTimRyan': 'Democratic',
    'Kilili_Sablan': 'Democratic',
    'RepMariaSalazar': 'Republican',
    'RepLindaSanchez': 'Democratic',
    'RepSarbanes': 'Democratic',
    'SteveScalise': 'Republican',
    'RepMGS': 'Democratic',
    'janschakowsky': 'Democratic',
    'RepAdamSchiff': 'Democratic',
    'RepSchneider': 'Democratic',
    'RepSchrader': 'Democratic',
    'RepKimSchrier': 'Democratic',
    'RepDavid': 'Republican',
    'AustinScottGA08': 'Republican',
    'BobbyScott': 'Democratic',
    'PeteSessions': 'Republican',
    'RepTerriSewell': 'Democratic',
    'BradSherman': 'Democratic',
    'RepSherrill': 'Democratic',
    'CongMikeSimpson': 'Republican',
    'RepSires': 'Democratic',
    'RepSlotkin': 'Democratic',
    'RepAdamSmith': 'Democratic',
    'RepAdrianSmith': 'Republican',
    'RepJasonSmith': 'Republican',
    'RepSmucker': 'Republican',
    'RepDarrenSoto': 'Democratic',
    'RepSpanberger': 'Democratic',
    'RepSpartz': 'Republican',
    'RepSpeier': 'Democratic',
    'Rep_Stansbury': 'Democratic',
    'RepGregStanton': 'Democratic',
    'RepPeteStauber': 'Republican',
    'RepSteel': 'Republican',
    'RepStefanik': 'Republican',
    'RepBryanSteil': 'Republican',
    'RepGregSteube': 'Republican',
    'RepHaleyStevens': 'Democratic',
    'RepChrisStewart': 'Republican',
    'RepStricklandWA': 'Democratic',
    'RepTomSuozzi': 'Democratic',
    'RepSwalwell': 'Democratic',
    'RepMarkTakano': 'Democratic',
    'claudiatenney': 'Republican',
    'BennieGThompson': 'Democratic',
    'RepThompson': 'Republican',
    'RepTiffany': 'Republican',
    'RepTimmons': 'Republican',
    'repdinatitus': 'Democratic',
    'RepRashida': 'Democratic',
    'RepPaulTonko': 'Democratic',
    'NormaJTorres': 'Democratic',
    'RepRitchie': 'Democratic',
    'RepLoriTrahan': 'Democratic',
    'RepDavidTrone': 'Democratic',
    'RepMikeTurner': 'Republican',
    'RepUnderwood': 'Democratic',
    'RepDavidValadao': 'Republican',
    'RepBethVanDuyne': 'Republican',
    'RepJuanVargas': 'Democratic',
    'RepVeasey': 'Democratic',
    'NydiaVelazquez': 'Democratic',
    'RepAnnWagner': 'Republican',
    'RepWalberg': 'Republican',
    'RepWalorski': 'Republican',
    'michaelgwaltz': 'Republican',
    'RepDWStweets': 'Democratic',
    'RepBonnie': 'Democratic',
    'RepWebster': 'Republican',
    'PeterWelch': 'Democratic',
    'RepWesterman': 'Republican',
    'RepWexton': 'Democratic',
    'RepSusanWild': 'Democratic',
    'RepNikema': 'Democratic',
    'RepRWilliams': 'Republican',
    'RepWilson': 'Democratic',
    'RepJoeWilson': 'Republican',
    'RobWittman': 'Republican',
    'rep_stevewomack': 'Republican',
    'RepJohnYarmuth': 'Democratic',
    'RepLeeZeldin': 'Republican'
}

# Create a directed graph
G = nx.DiGraph()

# Add nodes with labels and party affiliation
for i, username in enumerate(usernameList):
    party = partyAffiliation.get(username, 'Unknown')  # Default to 'Unknown' if not found
    G.add_node(i, label=username, party=party)

# Add edges with weights from JSON data
for i, out_nodes in enumerate(outList):
    for j, target in enumerate(out_nodes):
        G.add_edge(i, target, weight=outWeight[i][j])

# Create Republican and Democratic subnetworks
republican_nodes = [n for n, d in G.nodes(data=True) if d['party'] == 'Republican']
democratic_nodes = [n for n, d in G.nodes(data=True) if d['party'] == 'Democratic']

republican_subgraph = G.subgraph(republican_nodes)
democratic_subgraph = G.subgraph(democratic_nodes)

# Analyze structural properties
def analyze_subgraph(subgraph, name):
    print(f"Analysis of {name} Subnetwork")
    print(f"Number of nodes: {subgraph.number_of_nodes()}")
    print(f"Number of edges: {subgraph.number_of_edges()}")
    print(f"Average degree: {sum(dict(subgraph.degree()).values()) / subgraph.number_of_nodes()}")
    print(f"Average clustering coefficient: {nx.average_clustering(subgraph)}")
    
    # Handle disconnected graph
    if nx.is_strongly_connected(subgraph):
        avg_shortest_path_length = nx.average_shortest_path_length(subgraph)
    else:
        largest_cc = max(nx.strongly_connected_components(subgraph), key=len)
        largest_subgraph = subgraph.subgraph(largest_cc)
        avg_shortest_path_length = nx.average_shortest_path_length(largest_subgraph)
    
    print(f"Average shortest path length: {avg_shortest_path_length}")
    print(f"Diameter: {nx.diameter(largest_subgraph)}")
    print()

analyze_subgraph(republican_subgraph, "Republican")
analyze_subgraph(democratic_subgraph, "Democratic")

# Identify nodes with high infiltration ratio
infiltration_nodes = []
for node in G.nodes():
    current_party = G.nodes[node]['party']
    neighbors = list(G.successors(node)) + list(G.predecessors(node))
    if not neighbors: 
        continue
    same_count = 0
    opp_count = 0
    for nbr in neighbors:
        if G.nodes[nbr]['party'] == current_party:
            same_count += 1
        else:
            opp_count += 1
    
    # Calculate infiltration ratio
    ratio = opp_count / (same_count + opp_count)
    if ratio > 0.5:
        infiltration_nodes.append(node)

print("Nodes with high infiltration ratio:")
for node in infiltration_nodes:
    print(G.nodes[node]['label'])

# List of Twitter handles to highlight
highlight_handles = [
    'RoyBlunt', 'SenAngusKing', 'Sen_JoeManchin', 'lisamurkowski', 'senrobportman',
    'SenSanders', 'SenatorSinema', 'RepDonBacon', 'RepChuck', 'RepCarlos',
    'RepMMM', 'RepJimmyPanetta', 'RepThompson'
]

# Find nodes corresponding to the handles to highlight
highlight_nodes = [n for n, d in G.nodes(data=True) if d['label'] in highlight_handles]

# Draw the full network with party colors
pos = nx.spring_layout(G)  # Position nodes using Fruchterman-Reingold force-directed algorithm
plt.figure(figsize=(12, 12))

# Draw nodes with colors based on party affiliation
node_colors = ['red' if G.nodes[n]['party'] == 'Republican' else 'blue' for n in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors)

# Highlight specified nodes in green
if highlight_nodes:
    nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color='green', node_size=700)

# Draw edges
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10, edge_color='gray')

# Draw labels
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=10)

plt.title('Congressional Twitter Network')
plt.savefig('Figure_1.png')
plt.show()