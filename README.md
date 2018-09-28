# Python deploy script for modern IDEs

It uses rsync or scp and SSH keys authentication.

Put sync folder in your home dir.

## VS Code
Install extension "Run on save".
in VS Code open File->Preferences->Settings add following between { and }:

```javascript
    "emeraldwalk.runonsave": {
        "commands": [
            {
                "match": ".*",
                "cmd": "python ~/sync/sync.py ${workspaceRoot} ${file} <user>"
            }
        ]
    }
```
Replace `<user>` with your user name.

If you are Windows user, change ~/sync/sync.py according to your path and in sync.py change SCRIPT_PATH.

## PhpStorm
In Settings->Tools->File Watchers add new watcher.
```
Name: sync
File type: Any
Scope:
Program: python
Arguments: /home/<user>/sync/sync.py $ProjectFileDir$ $FilePath$ <user>
```
Replace `<user>` with your user name.

Add your project settings to config.json.
"remote_path" is for php files.
"remote_path_htdocs" is for assets (.js, .css).
"build_cmd" - put your build command here, for less files compiling, React build or ES6 babel compiling.
"user" - if some server needs different username, put it here.

## config.json

Default sync method is rsync.

```
Example config.json:
    {
    "project_1": {
        "server": "server1.example.com",
        "method": "scp",
        "remote_path": "/var/www/html/project_1"
    },
    "project_2": {
        "server": "server2.example.com",
        "remote_path": "/var/www/html/project_2",
        "build_cmd": "lessc --source-map /var/www/html/project_2/less/style.less /var/www/html/project_2/css/style.css"
    },
    "project_3": {
        "server": "server3.example.com",
        "remote_path": "/var/www/html/project_3",
        "remote_path_htdocs": "/var/www/html/project_3/htdocs/"
    },
    "project_4": {
        "server": "server4.example.com",
        "port": 622,
        "user": "user1",
        "method": "scp",
        "remote_path": "/var/www/html/project_4"
    }   
}
```
