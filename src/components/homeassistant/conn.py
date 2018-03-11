from homeassistant import remote
import time
from homeassistant.const import STATE_ON,STATE_OFF,STATE_OPEN,STATE_CLOSED


def connection():
    api = remote.API('127.0.0.1', 'welcome')
    domain = 'light'        # state的前缀

    # print(remote.validate_api(api))
    # print(remote.get_config(api))
    print('-- Available services:')
    services = remote.get_services(api)
    for service in services:
        print(service['services'])

    print('\n-- Available events:')
    events = remote.get_event_listeners(api)
    for event in events:
        print(event)

    print('\n-- Available entities:')
    entities = remote.get_states(api)
    for entity in entities:
        print(entity)

    office_temp = remote.get_state(api, 'sensor.temperature_158d0002229ec1')
    print('{} is {} {}.'.format(
        office_temp.name, office_temp.state,
        office_temp.attributes['unit_of_measurement'])
    )
    office_temp = remote.get_state(api, 'sensor.humidity_158d0002229ec1')
    print('{} is {} {}.'.format(
        office_temp.name, office_temp.state,
        office_temp.attributes['unit_of_measurement'])
    )
    remote.call_service(api, domain, 'turn_on')

