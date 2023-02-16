Name:     rpm
Version:  4.18.0
Release:  r1
Summary:  Redhat Package Manager (RPM)
License:  fixme
URL:      https://www.rpm.org/
Source0:  rpm-%{version}.tar.xz
# BuildRequires: libc6-dev zlib-dev zstd-dev
BuildArch: aarch64

%bcond_without multiarch

%if %{with multiarch}
  %define _libdir %{_prefix}/lib/%{build_target}
  %define _includedir %{_prefix}/include/%{build_target}%endif

%description
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

