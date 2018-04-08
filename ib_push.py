import sys
import json
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def login(ip, headers, username, password, verify):
    r = requests.get('https://%s/wapi/v2.7.1/networkview' % ip, headers=headers, \
                        auth=(username,password), verify=verify)
    if r.status_code != 200:
        print r.text
        exit_msg = 'Something went wrong'
    res = r.json()

    # Write cookie into variable
    cookie = r.cookies['ibapauth']
    print 'Successfully authenticated'
    return cookie

def get_grid(ip, headers, cookies, verify):
    r = requests.get('https://%s/wapi/v2.7.1/grid' % ip, headers=headers,
                        cookies=cookies, verify=verify)

    if r.status_code != 200:
        print r.text
        exit_msg = 'Something went wrong'

    return r.json()

def get_rpz(ip, headers, cookies, verify):
    r = requests.get('https://%s/wapi/v2.7.1/zone_rp' % ip, headers=headers,
                        cookies=cookies, verify=verify)

    if r.status_code != 200:
        print r.text
        exit_msg = 'Something went wrong'

    return r.json()

def create_rpz(ip, headers, cookies, dxl_rpz, verify):
    payload = {"fqdn": dxl_rpz,
               "rpz_policy": "GIVEN",
               "rpz_severity": "MAJOR"}

    r = requests.post('https://%s/wapi/v2.7.1/zone_rp' % ip, headers=headers,
                        cookies=cookies, data=json.dumps(payload), verify=verify)

    if r.status_code != 201:
        print r.text
        exit_msg = 'Something went wrong'

    return r.json()

def get_records(ip, headers, cookies, dxl_rpz, verify):
    r = requests.get('https://%s/wapi/v2.7.1/allrpzrecords?zone=%s' % (ip, dxl_rpz), headers=headers,
                        cookies=cookies, verify=verify)

    if r.status_code != 200:
        print r.text
        exit_msg = 'Something went wrong'

    return r.json()

def create_domain_records(ip, headers, cookies, dxl_rpz, dxl_domain, verify):
    payload = {"name":dxl_domain + '.' + dxl_rpz,
               "canonical":"",
               "rp_zone":dxl_rpz}

    r = requests.post('https://%s/wapi/v2.7.1/record:rpz:cname' % ip, headers=headers,
                        cookies=cookies, data=json.dumps(payload), verify=verify)

    if r.status_code != 201:
        print r.text
        exit_msg = 'Something went wrong'

    return r.json()

def create_ip_records(ip, headers, cookies, dxl_rpz, dxl_ip, verify):
    payload = {"name":dxl_ip + '.' + dxl_rpz,
               "canonical":"",
               "rp_zone":dxl_rpz}

    r = requests.post('https://%s/wapi/v2.7.1/record:rpz:cname:ipaddress' % ip, headers=headers,
                        cookies=cookies, data=json.dumps(payload), verify=verify)

    if r.status_code != 201:
        print r.text
        exit_msg = 'Something went wrong'

    return r.json()

def restart_services(ip, headers, cookies, grid, verify):
    payload = {"member_order": "SIMULTANEOUSLY",
               "service_option": "ALL"}

    r = requests.post('https://%s/wapi/v2.7.1/%s?_function=restartservices' % (ip, grid), headers=headers,
                        cookies=cookies, data=json.dumps(payload), verify=verify)

    if r.status_code != 200:
        print r.text
        exit_msg = 'Something went wrong'

    return r.json()

def logout(ip, headers, cookies, verify):
    r = requests.post('https://%s/wapi/v2.7.1/logout' % ip, headers=headers,
                        cookies=cookies, verify=verify)
    return r

if __name__ == "__main__":

    ip = 'ip address'
    username = 'username'
    password = 'password'
    verify = False

    dxl_rpz = 'dxl_block'
    choice = sys.argv[1]
    dxl_value = sys.argv[2].lower()

    headers = {'Content-Type': 'application/json'}

    cookie = login(ip, headers, username, password, verify)
    cookies = {'ibapauth': cookie}

    grids = get_grid(ip, headers, cookies, verify)
    for item in grids:
        grid = item['_ref']

    rpz = get_rpz(ip, headers, cookies, verify)
    exist = 0
    for fqdn in rpz:
        rpz_name = fqdn['fqdn']
        if rpz_name == dxl_rpz:
            exist = 1
            break
        else:
            exist = 0

    if exist == 0:
        print 'RPZ does not exist - creating a new Response Policy Zone'
        rpzres = create_rpz(ip, headers, cookies, dxl_rpz, verify)
    else:
        print 'RPZ exist already'

    records = get_records(ip, headers, cookies, dxl_rpz, verify)
    exist = 0
    for name in records:
        rec_name = name['name']
        if rec_name == dxl_value:
            exist = 1
            break
        else:
            exist = 0

    if exist == 0:
        print 'Record does not exist - adding a new Block Domain Name (No Such Domain) Rule to the %s RPZ' % dxl_rpz

        if choice == 'domain':
            recres = create_domain_records(ip, headers, cookies, dxl_rpz, dxl_value, verify)
            dxl_value = '*.' + dxl_value
            recres = create_domain_records(ip, headers, cookies, dxl_rpz, dxl_value, verify)

        elif choice == 'ip':
            recres = create_ip_records(ip, headers, cookies, dxl_rpz, dxl_value, verify)

        else:
            print 'Please enter an ip or domain'

        print 'Restarting services now'
        restart_services(ip, headers, cookies, grid, verify)
    else:
        print 'Block Domain Name Rule exist already'


    logout(ip, headers, cookies, verify)
    print 'Successfully logged out'
