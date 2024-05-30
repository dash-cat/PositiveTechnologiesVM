## Searching for CPEs

https://nvd.nist.gov/products/cpe/search

e.g.

https://nvd.nist.gov/products/cpe/search/results?namingFormat=2.3&keyword=keycloak

https://openlitespeed.org/kb/install-from-binary/



ansible@debian:~$ curl http://apache.bintray.com/couchdb-deb 
<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx</center>
</body>
</html>


sudo apt-get clean





TASK [nginx_unit_from_official_package_on_debian : Display APT update result if it failed] ***********************************************************************************************************
task path: /home/griggy/Documents/AnsiblePlaybook/nginx_unit_from_official_package_on_debian/roles/nginx_unit_from_official_package_on_debian/tasks/main.yaml:44
ok: [127.0.0.1] => {
    "apt_update_result": {
        "changed": false,
        "failed": true,
        "msg": "Failed to update apt cache: unknown reason"
    }
}