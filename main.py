import argparse
import hashlib
from requests_html import HTMLSession

parser = argparse.ArgumentParser(description='Restarts BGW210 model routers provided by AT&T via their admin interface')
parser.add_argument('-u', '--url',
                    default='http://192.168.1.254',
                    help='The base url of your router''s admin interface'
                    )
parser.add_argument('-a', '--access_code',
                    required=True,
                    help='The access code to login to your router')

args = parser.parse_args()
BASE_URL = args.url
RESTART_URL = f'{BASE_URL}/cgi-bin/restart.ha'
AUTH_PWD = args.access_code


def check_response(resp):
    if resp.status_code != 200:
        # Just bail out...
        print_status('Failed to fetch restart page', "ERROR")
        exit(1)


def find_form(resp):
    form = resp.html.find('form', first=True)
    if form is None:
        # Something went wrong - we should have gotten a form...
        print_status("Couldn't find a form on the restart page. Exiting...", "ERROR")
        exit(1)
    return form


def print_status(msg, level='INFO'):
    print(f'[{level}] {msg}')


# Start a session
session = HTMLSession()
# Fetch the restart page (may end up with a login form)
r = session.get(RESTART_URL)
check_response(r)
form = find_form(r)
form_action = form.attrs['action']

# Check to see if we landed on the login page
if "login.ha" in form_action:
    # We hit the login page, so we need to login first...
    nonce_elem = form.find('input[name=nonce]', first=True)
    nonce_str = nonce_elem.attrs['value']

    # Build the form vals to be submitted
    digested_pwd = hashlib.md5(f'{AUTH_PWD}{nonce_str}'.encode('utf-8')).hexdigest()

    # Finally, login...
    form_data = {'nonce': nonce_str, 'password': '**********', 'hashpassword': digested_pwd, 'Continue': 'Continue'}
    r = session.post(f'{BASE_URL}{form_action}', form_data)
    # Make sure the login worked properly...
    check_response(r)

    # Be sure to reset the form vars for further use
    form = find_form(r)
    form_action = form.attrs['action']

nonce_elem = form.find('input[name=nonce]', first=True)
nonce_str = nonce_elem.attrs['value']
form_data = {'nonce': nonce_str, 'Restart': 'Restart'}
r = session.post(f'{BASE_URL}{form_action}', form_data)

check_response(r)
