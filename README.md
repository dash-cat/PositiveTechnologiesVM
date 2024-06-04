## Searching for CPEs


sudo hwclock --hctosys 
new_password

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




fatal: [127.0.0.1]: FAILED! => {
    "changed": true,
    "cmd": "php setup/setup.php -y install /etc/ilias-minimal-config.json",
    "delta": "0:03:08.561539",
    "end": "2024-06-03 12:55:29.314635",
    "invocation": {
        "module_args": {
            "_raw_params": "php setup/setup.php -y install /etc/ilias-minimal-config.json",
            "_uses_shell": true,
            "argv": null,
            "chdir": "/var/www/html/ilias",
            "creates": null,
            "executable": null,
            "expand_argument_vars": true,
            "removes": null,
            "stdin": null,
            "stdin_add_newline": true,
            "strip_empty_ends": true
        }
    },
    "msg": "non-zero return code",
    "rc": 1,
    "start": "2024-06-03 12:52:20.753096",
    "stderr": "\nIn ObjectiveIterator.php line 147:\n                                                                  \n  Objective 'Install and Update ILIAS' had failed preconditions:  \n    - Collected Install Objectives                                \n    - Collected Update Objectives                                 \n                                                                  \n\ninstall [--config [CONFIG]] [-y|--yes] [-i|--import-file IMPORT-FILE] [--plugin PLUGIN] [--no-plugins] [--skip SKIP] [--] [<config>]",
    "stderr_lines": [
        "",
        "In ObjectiveIterator.php line 147:",
        "                                                                  ",
        "  Objective 'Install and Update ILIAS' had failed preconditions:  ",
        "    - Collected Install Objectives                                ",
        "    - Collected Update Objectives                                 ",
        "                                                                  ",
        "",
        "install [--config [CONFIG]] [-y|--yes] [-i|--import-file IMPORT-FILE] [--plugin PLUGIN] [--no-plugins] [--skip SKIP] [--] [<config>]"
    ],
    "stdout": "\nInstall ILIAS\n=============\n\n ! [NOTE] Automatically confirmed:                                              \n !                                                                              \n !        Please note that you are running this program at your own risk and    \n !        with                                                                  \n !        absolutely no warranty. You should perform regular backups and        \n !        thorough                                                              \n !        testing to prevent data loss or unpleasant surprises when running this\n !        program. Are you fine with this?                                      \n\n ! [NOTE] Automatically confirmed:                                              \n !                                                                              \n !        You seem to be using root or your user just can't be determined. You  \n !        should                                                                \n !        be running this setup with the same user the webserver uses. If this  \n !        is not                                                                \n !        the case there might be problems accessing files via the web later... \n !        If you still proceed, carefully check file access rights in the       \n !        data-directories                                                      \n !        after finishing the setup.                                            \n !                                                                              \n\nPHP version >= 8.1.0...                                                    [OK]\nPHP extension \"dom\" loaded...                                              [OK]\nPHP extension \"xsl\" loaded...                                              [OK]\nPHP extension \"gd\" loaded...                                               [OK]\nPHP memory limit >= 128M...                                                [OK]\nCan create directories in '/var/www/html/ilias'...                         [OK]\nCreate directory '/var/www/html/ilias/data'...                             [OK]\nCan create directories in '/var/www/html/ilias/data'...                    [OK]\nCreate directory '/var/www/html/ilias/data/myilias'...                     [OK]\nCan create files in '/var/www/html/ilias/data/myilias'...                  [OK]\nCan create files in '/var/www/html/ilias'...                               [OK]\nThe ilias.ini.php and client.ini.php are populated....                     [OK]\nThe database server is connectable with the supplied configuration....     [OK]\nThe database exists on the server....                                      [OK]\nThe database is populated with ILIAS-tables....                            \n Default DB engine is innodb\n reading dump file, this may take a while...\n[FAILED]\n\n [ERROR] Cannot populate database with dump file: ./setup/sql/ilias3.sql. Query \n         failed:                                                                \n                                                                                \n                                                                                \n                                                                                \n         CREATE TABLE `crs_settings` (                                          \n           `obj_id` int(11) NOT NULL DEFAULT 0,                                 \n           `syllabus` varchar(4000) DEFAULT NULL,                               \n           `contact_name` varchar(255) DEFAULT NULL,                            \n           `contact_responsibility` varchar(255) DEFAULT NULL,                  \n           `contact_phone` varchar(255) DEFAULT NULL,                           \n           `contact_email` varchar(255) DEFAULT NULL,                           \n           `contact_consultation` varchar(4000) DEFAULT NULL,                   \n           `activation_type` tinyint(4) NOT NULL DEFAULT 0,                     \n           `activation_start` int(11) DEFAULT NULL,                             \n           `activation_end` int(11) DEFAULT NULL,                               \n           `sub_limitation_type` tinyint(4) NOT NULL DEFAULT 0,                 \n           `sub_start` int(11) DEFAULT NULL,                                    \n           `sub_end` int(11) DEFAULT NULL,                                      \n           `sub_type` int(11) DEFAULT NULL,                                     \n           `sub_password` varchar(32) DEFAULT NULL,                             \n           `sub_mem_limit` tinyint(4) NOT NULL DEFAULT 0,                       \n           `sub_max_members` int(11) DEFAULT NULL,                              \n           `sub_notify` int(11) DEFAULT NULL,                                   \n           `view_mode` tinyint(4) NOT NULL DEFAULT 0,                           \n           `sortorder` int(11) DEFAULT NULL,                                    \n           `archive_start` int(11) DEFAULT NULL,                                \n           `archive_end` int(11) DEFAULT NULL,                                  \n           `archive_type` int(11) DEFAULT NULL,                                 \n           `abo` tinyint(4) DEFAULT 1,                                          \n           `waiting_list` tinyint(4) NOT NULL DEFAULT 1,                        \n           `important` varchar(4000) DEFAULT NULL,                              \n           `show_members` tinyint(4) NOT NULL DEFAULT 1,                        \n           `latitude` varchar(30) DEFAULT NULL,                                 \n           `longitude` varchar(30) DEFAULT NULL,                                \n           `location_zoom` int(11) NOT NULL DEFAULT 0,                          \n           `enable_course_map` tinyint(4) NOT NULL DEFAULT 0,                   \n           `session_limit` tinyint(4) NOT NULL DEFAULT 0,                       \n           `session_prev` bigint(20) NOT NULL DEFAULT -1,                       \n           `session_next` bigint(20) NOT NULL DEFAULT -1,                       \n           `reg_ac_enabled` tinyint(4) NOT NULL DEFAULT 0,                      \n           `reg_ac` varchar(32) DEFAULT NULL,                                   \n           `status_dt` tinyint(4) DEFAULT 2,                                    \n           `auto_notification` tinyint(4) NOT NULL DEFAULT 1,                   \n           `mail_members_type` tinyint(4) DEFAULT 1,                            \n           `crs_start` int(11) DEFAULT NULL,                                    \n           `crs_end` int(11) DEFAULT NULL,                                      \n           `leave_end` int(11) DEFAULT NULL,                                    \n           `auto_wait` tinyint(4) NOT NULL DEFAULT 0,                           \n           `min_members` smallint(6) DEFAULT NULL,                              \n           `show_members_export` int(11) DEFAULT NULL,                          \n           `timing_mode` tinyint(4) DEFAULT 0,                                  \n           `period_start` datetime DEFAULT NULL,                                \n           `period_end` datetime DEFAULT NULL,                                  \n           `period_time_indication` int(11) NOT NULL DEFAULT 0,                 \n           `target_group` varchar(4000) DEFAULT NULL,                           \n           PRIMARY KEY (`obj_id`)                                               \n         ) ;                                                                    \n          wih message SQLSTATE[42000]: Syntax error or access violation: 1118   \n         Row size too large. The maximum row size for the used table type, not  \n         counting BLOBs, is 65535. This includes storage overhead, check the    \n         manual. You have to change some columns to TEXT or BLOBs               \n\nBuild ./src/FileDelivery/artifacts/delivery_method.php...                  [OK]\nILIAS directories are created...                                           [OK]\nThe database server has valid settings....                                 [in progress]\n\n ! [NOTE] Default Row Format is DYNAMIC.                                        \n\n ! [NOTE] Default Engine is InnoDB.                                             \n\nThe database server has valid settings....                                 [OK]\nPHP extension \"imagick\" loaded...                                          [OK]\nPHP extension \"zip\" loaded...                                              [OK]\nStore configuration of Services/GlobalCache...                             [FAILED]\n\n [ERROR] An undefined Database Exception occured. SQLSTATE[42S02]: Base table or\n         view not found: 1146 Table 'ilias.il_gc_memcache_server' doesn't exist \n         QUERY: TRUNCATE TABLE il_gc_memcache_server                            \n\nCreate directory '/var/www/html/ilias/data/myilias/lm_data'...             [OK]\nCreate directory '/var/www/html/ilias/data/myilias/LSO'...                 [OK]\nCreate directory '/var/www/html/ilias/data/myilias/mobs'...                [OK]\nCreate directory '/var/www/html/ilias/data/myilias/usr_images'...          [OK]",
    "stdout_lines": [
        "",
        "Install ILIAS",
        "=============",
        "",
        " ! [NOTE] Automatically confirmed:                                              ",
        " !                                                                              ",
        " !        Please note that you are running this program at your own risk and    ",
        " !        with                                                                  ",
        " !        absolutely no warranty. You should perform regular backups and        ",
        " !        thorough                                                              ",
        " !        testing to prevent data loss or unpleasant surprises when running this",
        " !        program. Are you fine with this?                                      ",
        "",
        " ! [NOTE] Automatically confirmed:                                              ",
        " !                                                                              ",
        " !        You seem to be using root or your user just can't be determined. You  ",
        " !        should                                                                ",
        " !        be running this setup with the same user the webserver uses. If this  ",
        " !        is not                                                                ",
        " !        the case there might be problems accessing files via the web later... ",
        " !        If you still proceed, carefully check file access rights in the       ",
        " !        data-directories                                                      ",
        " !        after finishing the setup.                                            ",
        " !                                                                              ",
        "",
        "PHP version >= 8.1.0...                                                    [OK]",
        "PHP extension \"dom\" loaded...                                              [OK]",
        "PHP extension \"xsl\" loaded...                                              [OK]",
        "PHP extension \"gd\" loaded...                                               [OK]",
        "PHP memory limit >= 128M...                                                [OK]",
        "Can create directories in '/var/www/html/ilias'...                         [OK]",
        "Create directory '/var/www/html/ilias/data'...                             [OK]",
        "Can create directories in '/var/www/html/ilias/data'...                    [OK]",
        "Create directory '/var/www/html/ilias/data/myilias'...                     [OK]",
        "Can create files in '/var/www/html/ilias/data/myilias'...                  [OK]",
        "Can create files in '/var/www/html/ilias'...                               [OK]",
        "The ilias.ini.php and client.ini.php are populated....                     [OK]",
        "The database server is connectable with the supplied configuration....     [OK]",
        "The database exists on the server....                                      [OK]",
        "The database is populated with ILIAS-tables....                            ",
        " Default DB engine is innodb",
        " reading dump file, this may take a while...",
        "[FAILED]",
        "",
        " [ERROR] Cannot populate database with dump file: ./setup/sql/ilias3.sql. Query ",
        "         failed:                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "         CREATE TABLE `crs_settings` (                                          ",
        "           `obj_id` int(11) NOT NULL DEFAULT 0,                                 ",
        "           `syllabus` varchar(4000) DEFAULT NULL,                               ",
        "           `contact_name` varchar(255) DEFAULT NULL,                            ",
        "           `contact_responsibility` varchar(255) DEFAULT NULL,                  ",
        "           `contact_phone` varchar(255) DEFAULT NULL,                           ",
        "           `contact_email` varchar(255) DEFAULT NULL,                           ",
        "           `contact_consultation` varchar(4000) DEFAULT NULL,                   ",
        "           `activation_type` tinyint(4) NOT NULL DEFAULT 0,                     ",
        "           `activation_start` int(11) DEFAULT NULL,                             ",
        "           `activation_end` int(11) DEFAULT NULL,                               ",
        "           `sub_limitation_type` tinyint(4) NOT NULL DEFAULT 0,                 ",
        "           `sub_start` int(11) DEFAULT NULL,                                    ",
        "           `sub_end` int(11) DEFAULT NULL,                                      ",
        "           `sub_type` int(11) DEFAULT NULL,                                     ",
        "           `sub_password` varchar(32) DEFAULT NULL,                             ",
        "           `sub_mem_limit` tinyint(4) NOT NULL DEFAULT 0,                       ",
        "           `sub_max_members` int(11) DEFAULT NULL,                              ",
        "           `sub_notify` int(11) DEFAULT NULL,                                   ",
        "           `view_mode` tinyint(4) NOT NULL DEFAULT 0,                           ",
        "           `sortorder` int(11) DEFAULT NULL,                                    ",
        "           `archive_start` int(11) DEFAULT NULL,                                ",
        "           `archive_end` int(11) DEFAULT NULL,                                  ",
        "           `archive_type` int(11) DEFAULT NULL,                                 ",
        "           `abo` tinyint(4) DEFAULT 1,                                          ",
        "           `waiting_list` tinyint(4) NOT NULL DEFAULT 1,                        ",
        "           `important` varchar(4000) DEFAULT NULL,                              ",
        "           `show_members` tinyint(4) NOT NULL DEFAULT 1,                        ",
        "           `latitude` varchar(30) DEFAULT NULL,                                 ",
        "           `longitude` varchar(30) DEFAULT NULL,                                ",
        "           `location_zoom` int(11) NOT NULL DEFAULT 0,                          ",
        "           `enable_course_map` tinyint(4) NOT NULL DEFAULT 0,                   ",
        "           `session_limit` tinyint(4) NOT NULL DEFAULT 0,                       ",
        "           `session_prev` bigint(20) NOT NULL DEFAULT -1,                       ",
        "           `session_next` bigint(20) NOT NULL DEFAULT -1,                       ",
        "           `reg_ac_enabled` tinyint(4) NOT NULL DEFAULT 0,                      ",
        "           `reg_ac` varchar(32) DEFAULT NULL,                                   ",
        "           `status_dt` tinyint(4) DEFAULT 2,                                    ",
        "           `auto_notification` tinyint(4) NOT NULL DEFAULT 1,                   ",
        "           `mail_members_type` tinyint(4) DEFAULT 1,                            ",
        "           `crs_start` int(11) DEFAULT NULL,                                    ",
        "           `crs_end` int(11) DEFAULT NULL,                                      ",
        "           `leave_end` int(11) DEFAULT NULL,                                    ",
        "           `auto_wait` tinyint(4) NOT NULL DEFAULT 0,                           ",
        "           `min_members` smallint(6) DEFAULT NULL,                              ",
        "           `show_members_export` int(11) DEFAULT NULL,                          ",
        "           `timing_mode` tinyint(4) DEFAULT 0,                                  ",
        "           `period_start` datetime DEFAULT NULL,                                ",
        "           `period_end` datetime DEFAULT NULL,                                  ",
        "           `period_time_indication` int(11) NOT NULL DEFAULT 0,                 ",
        "           `target_group` varchar(4000) DEFAULT NULL,                           ",
        "           PRIMARY KEY (`obj_id`)                                               ",
        "         ) ;                                                                    ",
        "          wih message SQLSTATE[42000]: Syntax error or access violation: 1118   ",
        "         Row size too large. The maximum row size for the used table type, not  ",
        "         counting BLOBs, is 65535. This includes storage overhead, check the    ",
        "         manual. You have to change some columns to TEXT or BLOBs               ",
        "",
        "Build ./src/FileDelivery/artifacts/delivery_method.php...                  [OK]",
        "ILIAS directories are created...                                           [OK]",
        "The database server has valid settings....                                 [in progress]",
        "",
        " ! [NOTE] Default Row Format is DYNAMIC.                                        ",
        "",
        " ! [NOTE] Default Engine is InnoDB.                                             ",
        "",
        "The database server has valid settings....                                 [OK]",
        "PHP extension \"imagick\" loaded...                                          [OK]",
        "PHP extension \"zip\" loaded...                                              [OK]",
        "Store configuration of Services/GlobalCache...                             [FAILED]",
        "",
        " [ERROR] An undefined Database Exception occured. SQLSTATE[42S02]: Base table or",
        "         view not found: 1146 Table 'ilias.il_gc_memcache_server' doesn't exist ",
        "         QUERY: TRUNCATE TABLE il_gc_memcache_server                            ",
        "",
        "Create directory '/var/www/html/ilias/data/myilias/lm_data'...             [OK]",
        "Create directory '/var/www/html/ilias/data/myilias/LSO'...                 [OK]",
        "Create directory '/var/www/html/ilias/data/myilias/mobs'...                [OK]",
        "Create directory '/var/www/html/ilias/data/myilias/usr_images'...          [OK]"
    ]
}