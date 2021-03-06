# vim: sw=4:ts=4:et


%define relabel_files() \
mkdir -p /var/lib/cni; \
mkdir -p /var/lib/kubelet/pods; \
mkdir -p /var/lib/rancher/k3s/agent/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots; \
mkdir -p /var/lib/rancher/k3s/data; \
mkdir -p /var/run/flannel; \
mkdir -p /var/run/k3s; \
restorecon -R -i /etc/systemd/system/k3s.service; \
restorecon -R -i /usr/lib/systemd/system/k3s.service; \
restorecon -R /var/lib/cni; \
restorecon -R /var/lib/kubelet; \
restorecon -R /var/lib/rancher; \
restorecon -R /var/run/k3s; \
restorecon -R /var/run/flannel


%define selinux_policyver 3.13.1-252
%define container_policyver 2.107-3

Name:   k3s-selinux
Version:	%{k3s_selinux_version}
Release:	%{k3s_selinux_release}.el7
Summary:	SELinux policy module for k3s

Group:	System Environment/Base		
License:	ASL 2.0
URL:		http://k3s.io
Source0:	k3s.pp
Source1:	k3s.if


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils, container-selinux >= %{container_policyver}
Requires(postun): policycoreutils

Conflicts: rke2-selinux

BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for k3s.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/k3s.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r k3s
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/k3s.pp
%{_datadir}/selinux/devel/include/contrib/k3s.if


%changelog
* Mon Feb 24 2020 Darren Shepherd <darren@rancher.com> 1.0-1
- Initial version

