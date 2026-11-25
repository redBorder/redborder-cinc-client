# redborder-cinc-client

Redborder RPM for the Cinc Client (the Apache 2.0 build of Chef Infra Client). It replaces
`redborder-chef-client` and the Progress `chef-workstation` package on every node type.

- Depends on `cinc-workstation` >= 26.4.0, which ships Cinc Client 19.4.46 and `knife`.
- Keeps `/etc/chef`, `/var/chef` and `/root/.chef` as the real paths. `rb_cinc_compat_links.sh`
  links `/etc/cinc`, `/var/cinc` and `/root/.cinc` to them and recreates the `/usr/bin` links.
- Keeps the `chef-client.service` unit name used by the cookbooks, serverspec and the WebUI.
- It does not obsolete `redborder-chef-client`: the migration script switches packages with `dnf swap`.
