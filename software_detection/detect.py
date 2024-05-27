import os
import re
import json
import argparse
from typing import Dict, Optional, List
from jinja2 import Environment, FileSystemLoader

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Detect installed software.')
parser.add_argument('config_path', type=str, help='The path to the config.json file')
args = parser.parse_args()

# Load configuration from JSON
with open(args.config_path, 'r') as config_file:
    config = json.load(config_file)

manufacturer = config['manufacturer']
application_name = config['name']
maintainer = config['maintainer']

package_fields_need_eq = {
    'name': config['package'],
    'maintainer': maintainer
}
soft_name = application_name

version_res = [r'([\d.]+)-.+', r'([\d.]+)']
oval_vars_template_file = 'oval_vars.xml.j2'
oval_vars_file = 'oval_vars.xml'

# Main function to execute the script
if __name__ == '__main__':
    # Get raw package information
    get_package_cmd = "dpkg-query -f '${Package};;${Status};;${Maintainer};;${Architecture};;${Source};;${Version}\n' -W"
    stream = os.popen(get_package_cmd)
    packages_raw = stream.read()

    # Parse package list
    package_parsing_re = r'(?P<name>.+);;(?P<status>.+);;(?P<maintainer>.+);;(?P<arch>.+);;(?P<source>.*);;(?P<version>.+)'
    r = re.compile(package_parsing_re)
    packages = [i.groupdict() for i in r.finditer(packages_raw)]

    # Filter packages based on fields
    comp_keys = package_fields_need_eq.keys()
    package = None
    for p in packages:
        res = True
        for key in comp_keys:
            if package_fields_need_eq.get(key) != p.get(key):
                res = False
                break
        if res:
            package = p
            break

    # Extract version using multiple regexes
    context = {
        'name': None,
        'version': None
    }
    if package:
        package_version = package.get('version', '')
        for version_re in version_res:
            result = re.search(version_re, package_version)
            if result:
                context['version'] = result.groups()[0]
                break

    if context['version']:
        context['name'] = soft_name

    # Render Jinja2 template to file with context
    template_dir = os.path.dirname(oval_vars_template_file)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(os.path.basename(oval_vars_template_file))
    rendered_content = template.render(context)

    # Write rendered content to output file
    with open(oval_vars_file, 'w') as f:
        f.write(rendered_content)
