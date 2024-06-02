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





Installing:
    zimbra-core
    zimbra-ldap
    zimbra-logger
    zimbra-mta
    zimbra-dnscache
    zimbra-snmp
    zimbra-store
    zimbra-apache
    zimbra-spell
    zimbra-convertd
    zimbra-proxy
    zimbra-archiving
    zimbra-imapd
    zimbra-license-tools
    zimbra-license-extension
    zimbra-network-store
    zimbra-connect
    zimbra-network-modules-ng

You appear to be installing packages on a platform different
than the platform for which they were built.

This platform is DEBIANUNKNOWN
Packages found: UBUNTU18_64
This may or may not work.


https://forums.zimbra.org/viewtopic.php?t=72091







ansible@debian:/opt/apache-ofbiz-18.12.06$ sudo ./gradlew cleanAll loadAll

FAILURE: Build failed with an exception.

* What went wrong:
Could not create an instance of type org.gradle.initialization.DefaultSettings_Decorated.
> Could not initialize class org.codehaus.groovy.runtime.InvokerHelper

* Try:
Run with --stacktrace option to get the stack trace. Run with --info or --debug option to get more log output. Run with --scan to get full insights.

* Get more help at https://help.gradle.org



https://cwiki.apache.org/confluence/display/OFBIZ/System+Requirements
trunk requires Java SDK 17 (there has been some work done to move to Java SDK 17, see issue OFBIZ-12722)
22.01 requires Java SDK 17
18.12 requires Java SDK 8
17.12 requires Java SDK 8
16.11 requires Java SDK 8


ansible@debian:~$ sudo apt install openjdk-8-jdk
[sudo] password for ansible: 
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package openjdk-8-jdk





The full traceback is:
  File "/tmp/ansible_apt_payload_5tmo89sg/ansible_apt_payload.zip/ansible/modules/apt.py", line 533, in package_status
  File "/usr/lib/python3/dist-packages/apt/cache.py", line 302, in __getitem__
    raise KeyError("The cache has no package named %r" % key)
fatal: [127.0.0.1]: FAILED! => {
    "changed": false,
    "invocation": {
        "module_args": {
            "allow_change_held_packages": false,
            "allow_downgrade": false,
            "allow_unauthenticated": false,
            "autoclean": false,
            "autoremove": false,
            "cache_valid_time": 0,
            "clean": false,
            "deb": null,
            "default_release": null,
            "dpkg_options": "force-confdef,force-confold",
            "fail_on_autoremove": false,
            "force": false,
            "force_apt_get": false,
            "install_recommends": null,
            "lock_timeout": 60,
            "name": "openjdk-8-jdk",
            "only_upgrade": false,
            "package": [
                "openjdk-8-jdk"
            ],
            "policy_rc_d": null,
            "purge": false,
            "state": "present",
            "update_cache": null,
            "update_cache_retries": 5,
            "update_cache_retry_max_delay": 12,
            "upgrade": null
        }
    },
    "msg": "No package matching 'openjdk-8-jdk' is available"
}

PLAY RECAP ************************************************************************************************************************************************************************************************************************************************************************
127.0.0.1                  : ok=4    changed=0    unreachable=0    failed=1    skipped=6    rescued=0    ignored=0   
