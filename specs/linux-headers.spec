Name: linux-api-headers
Version: 4.19.272
Release: r0%{?dist}
Summary: Linux kernel headers
License: GPLv2
URL: https://www.kernel.org/
Source: https://www.kernel.org/pub/linux/kernel/v%{version:0:1}.x/linux-%{version}.tar.xz
# BuildRequires: make cc

%define _target aarch64-linux-gnu

%description
Kernel headers sanitized for use in userspace

%prep
%setup -q -n linux-%{version}


%build
make mrproper


%install
make headers_install
mkdir -p %{buildroot}%{_includedir}/%{_target}
cp -a usr/include/*/ %{buildroot}%{_includedir}/%{_target}
find %{buildroot}%{_includedir}/%{_target} \
	-name '.*install*' -exec rm -vf '{}' \;
# use headers from libdrm
# rm -rf "$terdir/usr/glibc/include/drm"


%files
%{_includedir}/%{_target}/asm/*.h
%{_includedir}/%{_target}/asm-generic/*.h
%{_includedir}/%{_target}/drm/*.h
%{_includedir}/%{_target}/linux/*.h
%{_includedir}/%{_target}/linux/android/*.h
%{_includedir}/%{_target}/linux/byteorder/*.h
%{_includedir}/%{_target}/linux/caif/*.h
%{_includedir}/%{_target}/linux/can/*.h
%{_includedir}/%{_target}/linux/cifs/*.h
%{_includedir}/%{_target}/linux/dvb/*.h
%{_includedir}/%{_target}/linux/genwqe/*.h
%{_includedir}/%{_target}/linux/hdlc/*.h
%{_includedir}/%{_target}/linux/hsi/*.h
%{_includedir}/%{_target}/linux/iio/*.h
%{_includedir}/%{_target}/linux/isdn/*.h
%{_includedir}/%{_target}/linux/mmc/*.h
%{_includedir}/%{_target}/linux/netfilter/*.h
%{_includedir}/%{_target}/linux/netfilter/ipset/*.h
%{_includedir}/%{_target}/linux/netfilter_arp/*.h
%{_includedir}/%{_target}/linux/netfilter_bridge/*.h
%{_includedir}/%{_target}/linux/netfilter_ipv4/*.h
%{_includedir}/%{_target}/linux/netfilter_ipv6/*.h
%{_includedir}/%{_target}/linux/nfsd/*.h
%{_includedir}/%{_target}/linux/raid/*.h
%{_includedir}/%{_target}/linux/sched/*.h
%{_includedir}/%{_target}/linux/spi/*.h
%{_includedir}/%{_target}/linux/sunrpc/*.h
%{_includedir}/%{_target}/linux/tc_act/*.h
%{_includedir}/%{_target}/linux/tc_ematch/*.h
%{_includedir}/%{_target}/linux/usb/*.h
%{_includedir}/%{_target}/linux/wimax/*.h
%{_includedir}/%{_target}/misc/*.h
%{_includedir}/%{_target}/mtd/*.h
%{_includedir}/%{_target}/rdma/*.h
%{_includedir}/%{_target}/rdma/hfi/*.h
%{_includedir}/%{_target}/scsi/*.h
%{_includedir}/%{_target}/scsi/fc/*.h
%{_includedir}/%{_target}/sound/*.h
%{_includedir}/%{_target}/video/*.h
%{_includedir}/%{_target}/xen/*.h


%changelog
* Wed Feb 8 2023 Zack Winkles <hymenaeus0@gmail.com
- Fixed up to work with Glibc 2.37.

* Mon Feb 6 2023 Zack Winkles <hymenaeus0@gmail.com>
- Initial revision.
