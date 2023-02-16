Name:           musl
Version:        1.2.4
Release:        r0%{?dist}
Summary:        The musl C library
License:        MIT
URL:            https://musl.libc.org/
Source0:        musl_%{srcver}.orig.tar.xz

# BuildRequires:  make gcc binutils doxygen graphviz
# Requires:       /bin/sh
Provides:		libc6
# BuildArch:		noarch

%bcond_with termux

%global snapver f47a8cdd
%global srcver %{version}%{?snapver:-%{snapver}}
%global srcdir %{build}/musl-%{srcver}

%if %{with termux}
	%define _prefix /data/data/com.termux/files/musl
	%define _libdir %{_prefix}/lib64
%endif


%description
musl is an implementation of the C standard library built on
top of the Linux system call API, including interfaces defined
in the base language standard, POSIX, and widely agreed-upon
extensions. musl is lightweight, fast, simple, free, and
strives to be correct in the sense of standards-conformance
and safety.


%prep
%autosetup -n musl-%{srcver}


%build
export LDFLAGS="${LDFLAGS} -Wl,-soname,libc-musl.so"
./configure --prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--syslibdir=%{_syslibdir} \
	--enable-debug \
	--enable-wrapper=%{__cc}
%make_build


%install
%make_install
install -m644 SNAPSHOT %{buildroot}%{_docdir}/SNAPSHOT
# rm -f %{buildroot}%{_syslibdir}/ld-musl-%{arch}.so.1
# mv %{buildroot}%{_libdir}/libc.so \
# 	%{buildroot}%{_syslibdir}/ld-musl-%{arch}.so.1
# ln -s %{buildroot}%{_syslibdir}/ld


%clean
make distclean


%files
%license LICENSE
%doc README INSTALL SNAPSHOT WHATSNEW


%changelog
* Sun Feb 05 08:29:04 PST 2023 Zack Winkles <hymenaeus0@disroot.org>
- Initial revision
