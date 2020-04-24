from api.utils import county


def test_county():
    county_data = county.read_county_stats_mongo("California", "Orange")

    assert county_data['county_name'] == "Orange"
    assert county_data['state_name'] == "California"

    assert isinstance(county_data['confirmed'], int)
    assert isinstance(county_data['new'], int)
    assert isinstance(county_data['death'], int)
    assert isinstance(county_data['new_death'], int)
    assert isinstance(county_data['fatality_rate'], str)
    assert county_data['fatality_rate'][-1] == "%"
    
    assert isinstance(county_data['latitude'], float)
    assert isinstance(county_data['longitude'], float)
    assert isinstance(county_data['last_update'], str)
