import requests
import logging
import arrow
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from config import TCONNECT_EMAIL, TCONNECT_PASSWORD

# Set up logging
logger = logging.getLogger(__name__)

# Base URLs
BASE_URL = 'https://tdcservices.tandemdiabetes.com/'
LOGIN_URL = 'https://tconnect.tandemdiabetes.com/login.aspx?ReturnUrl=%2f'

class TConnectApi:
    def __init__(self, email=TCONNECT_EMAIL, password=TCONNECT_PASSWORD):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.userGuid = None
        self.accessToken = None
        self.accessTokenExpiresAt = None
        self.logged_in = self.login()

    def login(self):
        logger.info("Logging in to TConnect API...")
        try:
            initial_response = self.session.get(LOGIN_URL)
            initial_response.raise_for_status()

            soup = BeautifulSoup(initial_response.content, 'html.parser')
            login_data = self._build_login_data(soup)

            login_response = self.session.post(LOGIN_URL, data=login_data, headers={'Referer': LOGIN_URL},
                                               allow_redirects=False)
            login_response.raise_for_status()

            if 'UserGUID' in self.session.cookies and 'accessToken' in self.session.cookies:
                self.userGuid = self.session.cookies['UserGUID']
                self.accessToken = self.session.cookies['accessToken']
                self.accessTokenExpiresAt = self.session.cookies['accessTokenExpiresAt']
                logger.info(f"Logged in successfully. Access token expires at {self.accessTokenExpiresAt}")
                return True
            else:
                logger.error("Login failed, missing session cookies.")
                return False

        except HTTPError as e:
            logger.error(f"HTTP error occurred during login: {e}")
            return False
        except Exception as e:
            logger.error(f"An error occurred during login: {e}")
            return False

    def _build_login_data(self, soup):
        return {
            "__VIEWSTATE": soup.select_one("#__VIEWSTATE")["value"],
            "__VIEWSTATEGENERATOR": soup.select_one("#__VIEWSTATEGENERATOR")["value"],
            "__EVENTVALIDATION": soup.select_one("#__EVENTVALIDATION")["value"],
            "ctl00$ContentBody$LoginControl$txtLoginEmailAddress": self.email,
            "ctl00$ContentBody$LoginControl$txtLoginPassword": self.password,
            "__EVENTTARGET": "ctl00$ContentBody$LoginControl$linkLogin",
        }

    def api_headers(self):
        if not self.accessToken:
            raise ValueError("No access token available")
        return {
            'Authorization': f'Bearer {self.accessToken}',
            'Origin': 'https://tconnect.tandemdiabetes.com',
            'Referer': 'https://tconnect.tandemdiabetes.com/',
        }

    def get(self, endpoint, params=None):
        url = BASE_URL + endpoint
        headers = self.api_headers()

        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            logger.error(f"HTTP error during GET {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred during GET {url}: {e}")
            raise

    def get_bolus_history(self, start_date, end_date):
        endpoint = f'api/bolus/history'
        params = {
            'startDate': arrow.get(start_date).format('YYYY-MM-DD'),
            'endDate': arrow.get(end_date).format('YYYY-MM-DD'),
            'userGuid': self.userGuid,
        }
        return self.get(endpoint, params)

    def get_iob_data(self, start_date, end_date):
        endpoint = f'api/iob/history'
        params = {
            'startDate': arrow.get(start_date).format('YYYY-MM-DD'),
            'endDate': arrow.get(end_date).format('YYYY-MM-DD'),
            'userGuid': self.userGuid,
        }
        return self.get(endpoint, params)
