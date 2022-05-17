%global debug_package %{nil}
%global dkms_name hid-logitech-dj
%global kernel_version 5.17

Name:       %{dkms_name}-dkms
Version:    %{kernel_version}.{{{ git_dir_version }}}
Release:    1%{?dist}
Summary:    Logitech input driver patched with support for Lightspeed 1.2 connectivity. IE: G Pro X Superlight or the G PowerPlay Wireless Charging System.
License:    GPLv2+
URL:        https://github.com/KyleGospo/hid-logitech-dj-dkms/

# Source file:
# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/hid/hid-logitech-dj.c
Source0:    https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/hid/hid-logitech-dj.c?h=v%{kernel_version}#/hid-logitech-dj.c
Source1:    https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/hid/hid-ids.h?h=v%{kernel_version}#/hid-ids.h
Source2:    Makefile
Source3:    dkms.conf

# Superlight patch:
Patch0:     hid-logitech-dj.patch

Provides:   %{dkms_name}-dkms = %{version}
Requires:   dkms

%description
Logitech HID driver from kernel %{kernel_version} patched with support for Lightspeed 1.2 connectivity. IE: G Pro X Superlight or the G PowerPlay Wireless Charging System.

%prep
%setup -q -T -c -n %{name}-%{version}
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} .
%patch0 -p0

%build

%install
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
