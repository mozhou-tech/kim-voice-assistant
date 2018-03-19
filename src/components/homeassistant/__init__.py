from homeassistant import remote
import time
from homeassistant.const import STATE_ON,STATE_OFF,STATE_OPEN,STATE_CLOSED


class Hass:

    def __init__(self):
        self._api = None

    def conn(self):
        if self._api is None:
            self._api = remote.API('127.0.0.1', 'welcome')

    def xiaomi_gateway_light(self,entity_id , state='turn_on', rgb_color=(255, 255, 255), brightness=100):
        assert state in ['turn_on', 'turn_off'], 'inputted state must be turn_on or turn_off'
        service_data = {}
        if state == 'turn_on':
            service_data = {
                'rgb_color': rgb_color,
                'brightness': brightness,
                'entity_id': entity_id
            }

        domain = 'light'        # state的前缀
        remote.call_service(self._api, domain, state, service_data=service_data)

    def get_entity_by(self):
        pass

        #
        # print('-- Available services:')
        # services = remote.get_services(self._api)
        # for service in services:
        #     print(service['services'])
        #
        # print('\n-- Available events:')
        # events = remote.get_event_listeners(self._api)
        # for event in events:
        #     print(event)
        #
    def xiaomi_print_entities(self):
        print('\n-- Available entities:')
        entities = remote.get_states(self._api)
        for entity in entities:
            print(entity)
        #
        # office_temp = remote.get_state(self._api, 'sensor.temperature_158d0002229ec1')
        # print('{} is {} {}.'.format(
        #     office_temp.name, office_temp.state,
        #     office_temp.attributes['unit_of_measurement'])
        # )
        # office_temp = remote.get_state(self._api, 'sensor.humidity_158d0002229ec1')
        # print('{} is {} {}.'.format(
        #     office_temp.name, office_temp.state,
        #     office_temp.attributes['unit_of_measurement'])
        # )

    @classmethod
    def get_instance(cls):
        return Hass()



