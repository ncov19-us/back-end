#############################################################################
#
# State name and state abbreviation dictionary, with longitude and latitude
#
#############################################################################


states = [
    {"state": "Alabama", "state_abbrv": "AL",},
    {"state": "Alaska", "state_abbrv": "AK",},
    {"state": "American Samoa", "state_abbrv": "AS"},
    {"state": "Arizona", "state_abbrv": "AZ",},
    {"state": "Arkansas", "state_abbrv": "AR",},
    {"state": "California", "state_abbrv": "CA",},
    {"state": "Colorado", "state_abbrv": "CO",},
    {"state": "Connecticut", "state_abbrv": "CT",},
    {"state": "Delaware", "state_abbrv": "DE",},
    {"state": "District of Columbia", "state_abbrv": "DC",},
    {"state": "Florida", "state_abbrv": "FL",},
    {"state": "Georgia", "state_abbrv": "GA",},
    {"state": "Guam", "state_abbrv": "GU"},
    {"state": "Hawaii", "state_abbrv": "HI",},
    {"state": "Idaho", "state_abbrv": "ID",},
    {"state": "Illinois", "state_abbrv": "IL",},
    {"state": "Indiana", "state_abbrv": "IN",},
    {"state": "Iowa", "state_abbrv": "IA",},
    {"state": "Kansas", "state_abbrv": "KS",},
    {"state": "Kentucky", "state_abbrv": "KY",},
    {"state": "Louisiana", "state_abbrv": "LA",},
    {"state": "Maine", "state_abbrv": "ME",},
    {"state": "Northern Mariana Islands", "state_abbrv": "MP"},
    {"state": "Maryland", "state_abbrv": "MD",},
    {"state": "Massachusetts", "state_abbrv": "MA",},
    {"state": "Michigan", "state_abbrv": "MI",},
    {"state": "Minnesota", "state_abbrv": "MN",},
    {"state": "Mississippi", "state_abbrv": "MS",},
    {"state": "Missouri", "state_abbrv": "MO",},
    {"state": "Montana", "state_abbrv": "MT",},
    {"state": "Nebraska", "state_abbrv": "NE",},
    {"state": "Nevada", "state_abbrv": "NV",},
    {"state": "New Hampshire", "state_abbrv": "NH",},
    {"state": "New Jersey", "state_abbrv": "NJ",},
    {"state": "New Mexico", "state_abbrv": "NM",},
    {"state": "New York", "state_abbrv": "NY",},
    {"state": "North Carolina", "state_abbrv": "NC",},
    {"state": "North Dakota", "state_abbrv": "ND",},
    {"state": "Ohio", "state_abbrv": "OH",},
    {"state": "Oklahoma", "state_abbrv": "OK",},
    {"state": "Oregon", "state_abbrv": "OR",},
    {"state": "Pennsylvania", "state_abbrv": "PA",},
    {"state": "Puerto Rico", "state_abbrv": "PR"},
    {"state": "Rhode Island", "state_abbrv": "RI",},
    {"state": "South Carolina", "state_abbrv": "SC",},
    {"state": "South Dakota", "state_abbrv": "SD",},
    {"state": "Tennessee", "state_abbrv": "TN",},
    {"state": "Texas", "state_abbrv": "TX",},
    {"state": "US Virgin Islands", "state_abbrv": "VI",},
    {"state": "Utah", "state_abbrv": "UT",},
    {"state": "Vermont", "state_abbrv": "VT",},
    {"state": "Virginia", "state_abbrv": "VA",},
    {"state": "Washington", "state_abbrv": "WA",},
    {"state": "West Virginia", "state_abbrv": "WV",},
    {"state": "Wisconsin", "state_abbrv": "WI",},
    {"state": "Wyoming", "state_abbrv": "WY",},
]

reverse_states_map = {}
for row in states:
    reverse_states_map[row["state_abbrv"]] = row["state"]
# print(reverse_states_map)
