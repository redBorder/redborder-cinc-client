#!/bin/bash
# Load the redborder environment (RVM) so commands run by recipes keep the same PATH as before.
# cinc-client itself runs on the Cinc Workstation embedded Ruby: its binstub clears GEM_HOME/GEM_PATH.
source /etc/profile
rvm gemset use default &>/dev/null
source /etc/sysconfig/chef-client
exec /opt/cinc-workstation/bin/cinc-client -c $CONFIG -i $INTERVAL -s $SPLAY $OPTIONS
