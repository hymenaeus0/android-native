Name: gmp
Version: 6.2.1
Release: r0
Summary: FIXME
License: FIXME
URL: FIXME
Source0: gmp-%{version}.tar.xz
# BuildRequires: libc6-dev zlib-dev zstd-dev
BuildArch: aarch64

%define _prefix /data/data/com.termux/files/usr
%define _libdir %{_prefix}/lib/%{cross_target}
%define _includedir %{_prefix}/include/%{cross_target}

%description
FIXME
FIXME
FIXME


%prep
%setup -q


%build
%configure --disable-cxx
%make_build


%install
%make_install
# install -m644 SNAPSHOT %{buildroot}%{_docdir}/SNAPSHOT
# rm -f %{buildroot}%{_syslibdir}/ld-musl-%{arch}.so.1
# mv %{buildroot}%{_libdir}/libc.so \
# %{buildroot}%{_syslibdir}/ld-musl-%{arch}.so.1
# ln -s %{buildroot}%{_syslibdir}/ld


%clean
make distclean


%files
%license LICENSE
%doc README INSTALL NEWS


%changelog
* Mon Feb 11 22:10:42 PST 2023 Zack Winkles <hymenaeus0@disroot.org>
- Initial revision

