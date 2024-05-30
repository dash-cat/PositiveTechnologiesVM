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




[ 30%] Linking CXX shared module python3modules/bareosfd.cpython-312-x86_64-linux-gnu.so
/usr/bin/ld: /usr/local/lib/libpython3.12.a(import.o): relocation R_X86_64_TPOFF32 against hidden symbol `pkgcontext' can not be used when making a shared object
/usr/bin/ld: failed to set dynamic section sizes: bad value
collect2: error: ld returned 1 exit status
make[2]: *** [core/src/plugins/filed/python/CMakeFiles/bareosfd-python3-module.dir/build.make:100: core/src/plugins/filed/python/python3modules/bareosfd.cpython-312-x86_64-linux-gnu.so] Error 1
make[1]: *** [CMakeFiles/Makefile2:4319: core/src/plugins/filed/python/CMakeFiles/bareosfd-python3-module.dir/all] Error 2
make: *** [Makefile:166: all] Error 2