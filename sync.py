import json, os, sys, platform
from string import Template
from pprint import pprint
from subprocess import call

# user specific stuff
user = sys.argv[3]
PRIVATE_KEY_PATH="~/.ssh/id_rsa"
SCRIPT_PATH = "/home/" + user + "/sync/"
DEFAULT_PORT=522
DEFAULT_METHOD="rsync"

# if saved file extension is in this array, whe dealing with htdocs
htdocs_ext = [".less", ".js", ".css"]

# load conf from json file
conf = json.load(open(SCRIPT_PATH + 'config.json'))

current_platform = platform.system()[0:7]
print("platform=" + current_platform)

# get local_path from script argument
local_path = sys.argv[1]
project = os.path.basename(os.path.normpath(local_path))
print("project=" + project)

file_path = sys.argv[2]

# get file extension from script argument
filename, ext = os.path.splitext(sys.argv[2])

if not project in conf:
    sys.exit(project + " not found in config.json")

server = conf[project]["server"]
print('server=' + server)

if "port" in conf[project]:
    port = conf[project]["port"]
else:
    port = DEFAULT_PORT
    
if "method" in conf[project]:
    method = conf[project]["method"]
else:
    method = DEFAULT_METHOD
print('method=' + method) 

if "user" in conf[project]:
    user = conf[project]["user"]

print('user=' + user) 

remote_path = ""
if "remote_path" in conf[project]:
    remote_path = conf[project]["remote_path"]
print("remote_path=" + remote_path)

remote_path_htdocs = ""
if "remote_path_htdocs" in conf[project]:
    remote_path_htdocs = conf[project]["remote_path_htdocs"]
print("remote_path_htdocs=" + remote_path_htdocs)
# kuidas eristada htdocs projekti project/htdocs-st ? 
# htdocs projektil on remote_path_htdocs = '' 
if ext in htdocs_ext: 
    if "build_cmd" in conf[project]:
        build_cmd = conf[project]["build_cmd"]
        print('build_cmd=' + build_cmd)
        os.system(build_cmd)
    if remote_path_htdocs:
        if project != "htdocs":
            local_path = local_path + "/htdocs"
        rsync_htdocs = Template('rsync -orvuz --exclude-from "${SCRIPT_PATH}exclude.txt" -e "ssh -l ${user} -p 522 -i ${PRIVATE_KEY_PATH}" ${local_path}/ ${server}:${remote_path_htdocs}').substitute(locals())
        print("rsync_htdocs=" + rsync_htdocs)
        os.system(rsync_htdocs)
else:
    if method == "rsync":
        rsync = Template('rsync -orvuz --exclude=${local_path}/htdocs --exclude-from "${SCRIPT_PATH}exclude.txt" -e "ssh -l ${user} -p 522 -i ${PRIVATE_KEY_PATH}" ${local_path}/ ${server}:${remote_path}').substitute(locals())
        print("rsync=" + rsync)
        os.system(rsync)
    else:
        len = len(local_path)
        path_end = file_path[len:]
        scp = Template('scp -P ${port} ${file_path} ${user}@${server}:${remote_path}${path_end}').substitute(locals())
        print("scp=" + scp)
        os.system(scp)
        
# rsync switches:
# p - preserve permissions
# g - preseve group
# o - preserve owner
# r - recursive
# v - verbose
# z - compress file data during the transfer



