import code
import os
import re
import json
import sys
import requests
import argparse
from jinja2 import FileSystemLoader, Environment

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Generates OVAL reports.')
parser.add_argument('config_path', type=str, nargs='?', default='./config.json', help='The path to the config.json file')
args = parser.parse_args()

# Load configuration from JSON
#with open('data/moodle_from_source_on_debian12.json', 'r') as config_file:
with open(args.config_path, 'r') as config_file:
    config = json.load(config_file)

# Extract manufacturer and application name from config.cpe
manufacturer = config['cpe']['manufacturer']
application_name = config['cpe']['app']

cve_api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
vulners_api_url = "https://vulners.com/api/v3/search/lucene/"
cves_search_params = {
    "virtualMatchString": [f"cpe:2.3:a:{m}:{application_name}" for m in manufacturer]
}
vulners_search_params = {
    "query": [f"cpe:2.3:a:{m}:{application_name}" for m in manufacturer],
    "type": "vulnerability"
}

product_cpe_res = [fr"cpe:2\.3:a:{m}:{application_name}:([\d.]+|\*):\*:\*:\*:(\*|open_source):" for m in manufacturer]

context_cpe_res = []
allowed_cve_statuses = ["Analyzed", "Modified"]
print_product_cpe = False
print_context_cpe = False

oval_template_file = "oval.xml.j2"
oval_file = "oval.xml"
oval_product_var_id = 1
oval_version_var_id = 2
oval_affected_family = "unix"
oval_soft_name = application_name

def get_request(url, params=None, method='GET'):
    if method == 'GET':
        r = requests.get(url, params=params)
    elif method == 'POST':
        r = requests.post(url, json=params)
    print('Requested data from %s' % r.url)
    return r.content


def get_cves_nvd(cve_api_url, cves_search_params, application_name):
    api_r = get_request(cve_api_url, cves_search_params, method='GET')
    if api_r is None:
        return []
    try:
        j = json.loads(api_r)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response content: {api_r}")
        return []
    vulnerabilities = j.get('vulnerabilities', [])
    print(f"NVD vulnerabilities for {application_name}:")
    relevant_vulns = []
    for v in vulnerabilities:
        cve_id = v.get('cve', {}).get('id')
        description = v.get('cve', {}).get('descriptions', [{}])[0].get('value', '')
        if application_name.lower() in description.lower():
            relevant_vulns.append(v)
            print(f"{cve_id}: {description[:100]}...")
    return relevant_vulns


def get_cves_vulners(vulners_api_url, vulners_search_params, application_name):
    api_r = get_request(vulners_api_url, vulners_search_params, method='POST')
    if api_r is None:
        return []
    try:
        j = json.loads(api_r)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response content: {api_r}")
        return []
    vulnerabilities = j.get('data', {}).get('search', [])
    print(f"Vulners vulnerabilities for {application_name}:")
    relevant_vulns = []
    for v in vulnerabilities:
        cve_id = v.get('_id')
        description = v.get('description', '')
        if application_name.lower() in description.lower():
            relevant_vulns.append(v)
            print(f"{cve_id}: {description[:100]}...")
    return relevant_vulns


def parse_versions(cpe_match):
    cpe = cpe_match.get('criteria')
    cpe_splited = cpe.split(':')
    ver_start_incl = cpe_match.get('versionStartIncluding')
    ver_end_incl = cpe_match.get('versionEndIncluding')
    ver_start_excl = cpe_match.get('versionStartExcluding')
    ver_end_excl = cpe_match.get('versionEndExcluding')
    ver = cpe_splited[5]
    v = {
        'left_ver': 0,
        'right_ver': 0,
        'left_incl': True,
        'right_incl': True
    }
    if ver != '*':
        v['left_ver'] = ver
        v['right_ver'] = ver
    if ver_start_incl:
        v['left_ver'] = ver_start_incl
    if ver_end_incl:
        v['right_ver'] = ver_end_incl
    if ver_start_excl:
        v['left_ver'] = ver_start_excl
        v['left_incl'] = False
    if ver_end_excl:
        v['right_ver'] = ver_end_excl
        v['right_incl'] = False
    if not v['left_ver'] and not v['right_ver']:
        return None
    return v

def parse_cpe_match(cpe_match, cpe_regexes):
    if not cpe_match.get('vulnerable'):
        return None
    cpe = cpe_match['criteria']
    if print_product_cpe:
        print(cpe)
    cpe_matched = False
    for regex in product_cpe_res:
        r = re.search(regex, cpe)
        if r:
            cpe_matched = True
    if not cpe_matched:
        return None
    versions = parse_versions(cpe_match)
    return versions

def parse_product_item(product_item, product_cpe_res):
    versions = []
    product_operator = product_item.get('operator')
    if product_operator and product_operator != "OR":
        sys.exit('unexpected operator')
    for i in product_item['cpeMatch']:
        version = parse_cpe_match(i, product_cpe_res)
        if version:
            versions.append(version)
    return versions

def check_context(cpe_match):
    cpe = cpe_match.get('criteria')
    if print_context_cpe:
        print(cpe)
    for regex in context_cpe_res:
        r = re.search(regex, cpe)
        if r:
            return True
    return False

def parse_context_item(item):
    operator = item.get('operator')
    if operator and operator != "OR":
        sys.exit('unexpected operator')
    context_found = False
    for i in item.get('cpeMatch', []):
        if check_context(i):
            context_found = True
    return context_found

def check_contexts(contexts):
    context_matched = False
    for context in contexts:
        if context:
            if parse_context_item(context):
                context_matched = True
                break
        else:
            return True
    return context_matched

def parse_conditions(conds):
    versions = []
    for i in conds:
        nodes = i.get('nodes')
        operator = i.get('operator')
        if operator:
            product = nodes[0]
            context = nodes[1]
        else:
            product = nodes
            context = {}
        if type(product) == dict:
            product = [product]
        if type(context) == dict:
            contexts = [context]
        for item in product:
            product_ver = parse_product_item(item, product_cpe_res)
        contexts_matched = check_contexts(contexts)
        if contexts_matched:
            versions = versions + product_ver
    return versions

def get_description(descriptions, lang):
    for i in descriptions:
        if i['lang'] == lang:
            return i['value']
    return ""

def parse_cve(cve):
    if cve is None:
        return None
    r = {}
    status = cve.get('vulnStatus')
    if status not in allowed_cve_statuses:
        return None
    r['id'] = cve.get('id')
    r['description'] = get_description(cve['descriptions'], 'en')
    r['conditions'] = parse_conditions(cve.get('configurations'))
    if not r['conditions']:
        return None
    return r

def parse_vulns(vulns):
    cves = []
    seen_ids = set()  # To keep track of added CVE IDs
    
    for i in vulns:
        cve = parse_cve(i.get('cve'))
        if cve:
            cve_id = cve['id']
            if cve_id not in seen_ids:
                cves.append(cve)
                seen_ids.add(cve_id)
            else:
                print(f"Duplicate CVE removed: {cve_id}")
        elif i.get('_source'):
            # Process Vulners data
            source = i['_source']
            cve_id = source.get('cvelist', [source.get('id')])
            if not cve_id or not cve_id[0]:
                continue
            cve_id = cve_id[0]
            if cve_id not in seen_ids:
                cve = {
                    'id': cve_id,
                    'description': source.get('description', 'No description available'),
                    'conditions': []
                }
                cves.append(cve)
                seen_ids.add(cve_id)
            else:
                print(f"Duplicate CVE removed: {cve_id}")
    
    return cves


def template_oval_vars(template_file, output_file, context):
    loader = FileSystemLoader("./")
    environment = Environment(loader=loader)
    template = environment.get_template(template_file)
    output = template.render(**context)
    with open(output_file, "w") as f:
        f.write(output)

if __name__ == "__main__":
    print("Getting CVEs from NVD...")
    nvd_vulns = get_cves_nvd(cve_api_url, cves_search_params, application_name)
    
    print("Getting CVEs from Vulners...")
    vulners_vulns = get_cves_vulners(vulners_api_url, vulners_search_params, application_name)
    

    # Combine both sources
    vulns = parse_vulns(nvd_vulns + vulners_vulns)
    
    context = {
        "soft_name": oval_soft_name,
        "cves": vulns,
        "product_var_id": oval_product_var_id,
        "version_var_id": oval_version_var_id,
        "affected_family": oval_affected_family
    }
    
    print("Populating template...")
    template_oval_vars(oval_template_file, oval_file, context)
