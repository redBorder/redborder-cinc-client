Name: redborder-cinc-client
Version: %{__version}
Release: %{__release}%{?dist}
BuildArch: noarch
Summary: Redborder package containing Cinc Client (chef-client) files

License: AGPL 3.0
URL: https://github.com/redBorder/redborder-cinc-client
Source0: %{name}-%{version}.tar.gz

BuildRequires: systemd

Requires: bash redborder-rubyrvm
# Cinc Workstation 26.4.0 ships Cinc Client 19.4.46, knife 19.3.4, Ruby 3.4.12 and OpenSSL 3.5.9
Requires: cinc-workstation >= 26.4.0

# Same files and service as redborder-chef-client. The switch from Chef to Cinc is done
# explicitly by the migration script (dnf swap), never by a plain "dnf upgrade", so no Obsoletes.
Provides: redborder-chef-client = %{version}-%{release}
Conflicts: redborder-chef-client
Conflicts: chef-workstation

%description
%{summary}

%prep
%setup -qn %{name}-%{version}

%build

%install
mkdir -p %{buildroot}/etc/chef
install -D -m 0644 resources/conf/client.rb.default %{buildroot}/etc/chef/client.rb.default
install -D -m 0644 resources/conf/knife.rb.default %{buildroot}/etc/chef/knife.rb.default
mkdir -p %{buildroot}/usr/lib/redborder/bin
install -D -m 0755 resources/bin/rb_cinc-client_start.sh %{buildroot}/usr/lib/redborder/bin/rb_cinc-client_start.sh
install -D -m 0755 resources/bin/rb_cinc_compat_links.sh %{buildroot}/usr/lib/redborder/bin/rb_cinc_compat_links.sh
install -D -m 0644 resources/systemd/chef-client.service %{buildroot}/usr/lib/systemd/system/chef-client.service
mkdir -p %{buildroot}/etc/chef/ohai/plugins/
install -D -m 0644 resources/ohai/plugins/redborder.rb %{buildroot}/etc/chef/ohai/plugins/redborder.rb

%files
%defattr(0644,root,root)
/etc/chef/client.rb.default
/etc/chef/knife.rb.default
%defattr(0755,root,root)
/usr/lib/redborder/bin/rb_cinc-client_start.sh
/usr/lib/redborder/bin/rb_cinc_compat_links.sh
%defattr(0644,root,root)
/usr/lib/systemd/system/chef-client.service
/etc/chef/ohai/plugins/redborder.rb

%post
%systemd_post chef-client.service

%preun
%systemd_preun chef-client.service

%postun
%systemd_postun chef-client.service

%posttrans
# Runs after the whole transaction, so also after chef-workstation's postuninstall
/usr/lib/redborder/bin/rb_cinc_compat_links.sh

%changelog
* Wed Nov 25 2026 Miguel Negrón <manegron@redborder.com> 1.0.0
- First version: replaces redborder-chef-client and chef-workstation with Cinc Workstation 26.4.0
