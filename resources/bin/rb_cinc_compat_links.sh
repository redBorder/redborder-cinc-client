#!/bin/bash
# Keeps redborder working on Cinc without touching the rest of the code:
#  - Cinc reads /etc/cinc, /var/cinc and ~/.cinc by default. redborder keeps everything in
#    /etc/chef, /var/chef and /root/.chef, so point the Cinc paths there.
#  - Recreates the /usr/bin links of Cinc Workstation. Removing chef-workstation deletes
#    /usr/bin/chef-client, knife, ohai, inspec... in its postuninstall without checking where
#    they point, which runs after the new package is installed.

WS_BIN=/opt/cinc-workstation/bin

link_dir() {
  local cinc_dir=$1 chef_dir=$2
  mkdir -p "$chef_dir"
  if [ -L "$cinc_dir" ]; then
    ln -sfn "$chef_dir" "$cinc_dir"
  elif [ -d "$cinc_dir" ]; then
    # Only replace an empty directory; never delete data
    if [ -z "$(ls -A "$cinc_dir")" ]; then
      rmdir "$cinc_dir" && ln -s "$chef_dir" "$cinc_dir"
    else
      echo "WARNING: $cinc_dir is not empty, not linking it to $chef_dir" >&2
    fi
  elif [ ! -e "$cinc_dir" ]; then
    ln -s "$chef_dir" "$cinc_dir"
  fi
}

link_dir /etc/cinc /etc/chef
link_dir /var/cinc /var/chef
link_dir /root/.cinc /root/.chef

if [ -d "$WS_BIN" ]; then
  for bin in cinc-client chef-client cinc-solo chef-solo knife ohai inspec cinc-auditor chef-vault berks cookstyle; do
    if [ -e "$WS_BIN/$bin" ] && [ ! -e "/usr/bin/$bin" ]; then
      ln -sf "$WS_BIN/$bin" "/usr/bin/$bin"
    fi
  done
fi

exit 0
