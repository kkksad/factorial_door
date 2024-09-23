import logging
import requests
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ufanet_door"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.services.async_register(DOMAIN, 'open_door', open_door)
    return True

def get_session_id(login, password):
    login_url = 'https://dom.ufanet.ru/login/'
    data = {
        'contract': login,
        'password': password
    }
    session = requests.Session()
    response = session.post(login_url, data=data)
    if response.status_code == 200:
        cookies = session.cookies
        sessionid = cookies.get('sessionid')
        if sessionid:
            return sessionid

def open_door(call):
    login = call.data.get('login')
    password = call.data.get('password')
    domf_id = call.data.get('domf_id')
    sessionid = get_session_id(login, password)
    url = f'https://dom.ufanet.ru/api/v0/skud/shared/{domf_id}/open/'
    coc = {'sessionid': f'{sessionid}'}
    response = requests.Session().get(url=url, cookies=coc)
    _LOGGER.info(response.json()["result"])
