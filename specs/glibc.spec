Name: glibc
Version: 2.36
Release: r0%{?dist}
Summary: GNU C library
License: GPLv3 LGPLv2 (FIXME)
URL: https://www.gnu.org/software/libc/
Source0: %{name}_%{version}.orig.tar.xz
Patch0: glibc-2.36-android_syscalls.patch
# BuildRequires: linux-headers
# BuildRequires: bison flex libtool gettext makeinfo
# Requires: libc6 zlib zstd
Provides: libc6 ldd
BuildArch: aarch64 arm x86_64 i686

#
# TARGET TUPLE
#
%define _target aarch64-linux-gnu


%bcond_without android
%bcond_without termux

%bcond_with multiarch

#global snapver f47a8cdd
#global srcver #{version}#{?snapver:-#{snapver}}

%global srcdir %{build}/glibc-%{version}

%if %{with android}
	%if %{__isa_bits} == 64
		%define _system_libpath /system/lib64
	%else
		%define _system_libpath /system/lib
	%endif

	%if %{with termux}
		%define _prefix /data/data/com.termux/files/usr
		%define _config_libpath %{_prefix}:%{_system_libpath}
	%endif
%endif

%if %{with multiarch}
	%define _libdir %{_prefix}/lib/%{_target}
	%define _includedir %{_prefix}/include/%{_target}
	%define _sysroot %{_prefix}/%{_target}

	# FIXME: this is still Android hardcoded
	%define _config_libpath %{_prefix}/lib/%{_target}
	%define _program_prefix %{_target}-
%endif


%description
FIXME
FIXME
FIXME


%prep
%setup -q -n glibc-%{version}
%patch 0 -p1
sed -i 's|/tmp|/data/data/com.termux/files/usr/tmp|g' $(grep -R /tmp/ . | grep -v /var/ | awk -F'[:=]' '{printf $1 "\n"}')
sed -i 's|/var/tmp|/data/data/com.termux/files/usr/tmp|g' $(grep -R /var/tmp . | awk -F'[:=]' '{printf $1 "\n"}')
rm -rf ../glibc-build
mkdir -p ../glibc-build


%build
cd ../glibc-build
cat > configparms << '_EOF'
libdir=%{_libdir}
slibdir=%{_libdir}
ld-installed-name=ld-glibc.so
 slibdir=${prefix}/glibc/libec77778h7íqi777o "rtlddir=%{_libdir}" >> configparms                           echo "sbindir=${prefix}/glibc/bin" >> configparms
rootsbindir=${prefix}/bin
_EOF
%define _configure ../glibc-%{version}/configure
%configure --with-sysroot=%{_sysroot} \
	--with-build-sysroot=%{?_build_sysroot} \
	--program-prefix=%{?_program_prefix} \
	--target=%{_target} \
	--disable-nls \
	--disable-werror \
	--disable-systemtap \
	--disable-build-nscd \
	--disable-nscd \
	--disable-pt_chown \
	--enable-tunables \
	--enable-bind-now \
	--enable-stack-protector=all \
	--enable-memory-tagging
make -j1 PARALLELMFLAGS=%{_smp_mflags}


%install
cd ../glibc-build
%make_install
# install -m644 SNAPSHOT %{buildroot}%{_docdir}/SNAPSHOT
# rm -f %{buildroot}%{_syslibdir}/ld-musl-%{arch}.so.1
# mv %{buildroot}%{_libdir}/libc.so \
# %{buildroot}%{_syslibdir}/ld-musl-%{arch}.so.1
# ln -s %{buildroot}%{_syslibdir}/ld


%clean
rm -rf ../binutils-build


%files
%license LICENSE
%doc README INSTALL NEWS


%changelog
* Mon Feb 06 08:29:04 PST 2023 Zack Winkles <hymenaeus0@disroot.org>
- Initial revision
