Name: binutils
Version: 2.40
Release: r1
Summary: GNU collection of binary utilities
License: GPLv3+
URL: https://sourceware.org/binutils
Source0: binutils-%{version}.tar.xz
# BuildRequires: libc6-dev zlib-dev zstd-dev
# BuildRequires: bison flex libtool gettext texinfo
# Requires: zlib zstd
Provides: ar as ld nm ranlib
BuildArch: aarch64

#
# For a cross build, define the target tuple on the command line
# to rpmbuild, for example:
#
#  $ rpmbuild --define "cross_target aarch64-android-linux-gnu"
#

%define cross_target aarch64-linux-gnu

%define _prefix /data/data/com.termux/files/usr
%define _exec_prefix %{_prefix}
%define _program_prefix %{cross_target}-
%define _bindir %{_prefix}/bin
%define _sbindir %{_bindir}
%define _libdir %{_prefix}/lib/%{cross_target}
%define _libexecdir %{_prefix}/lib
%define _datarootdir %{_prefix}/share
%define _mandir %{_datarootdir}/man
%define _infodir %{_datarootdir}/info
%define _docdir %{_datarootdir}/doc/binutils
%define _htmldir %{_docdir}/html

%if 0%{!?cross_target:1}
  echo "cross_target must be defined!"
  %error 1
  %define is_native 1
  %define binutils_target %{_target_platform}
  %define enable_shared 1
%else
  %define is_native 0
  %define cross %{cross_target}-
  %define cross_name -%{cross_target}
  %define enable_shared 0
%endif

%define basever 2.40
#define snapver git20230210
%define srcdir %{basever}%{?snapver:_%{snapver}}

%bcond_with bootstrap

%if %{__isa_bits} == 64
  %define android_system_libdir /system/lib64
%else
  %define android_system_libdir /system/lib
%endif

%define ld_lib_path %{_libdir}:%{_prefix}/lib:%{android_system_libdir}

%if 0%{with multiarch}
	#define _libdir %{_prefix}/lib
	#define _includedir %{_prefix}/include
	#define _sysroot %{_prefix}

	# FIXME: this is still Android hardcoded
	#define _conf_with_libpath --with-libpath=%{_libdir}:%{_prefix}/lib:%{_sys_libpath}
	#define _conf_program_prefix --program-prefix=%{cross_target}-
%else
	%undefine _conf_target
	%undefine _conf_program_prefix
	%undefine _conf_with_libpath
%endif

%if %{with bootstrap}
	%undefine _conf_with_sysroot
	%define _conf_build_target --host=%{cross_target} --build=%{cross_target} --target=%{cross_target}
	%define _conf_shared --disable-shared --disable-plugins --disable-lto
%else
	%undefine _conf_with_sysroot
	%define _conf_build_target --target=%{cross_target}
	%define _conf_shared --enable-shared --enable-plugins --enable-lto
%endif


%description
FIXME
FIXME
FIXME


%prep
%setup -q -n binutils-%{version}


%build
mkdir -p build
cd build
%use_glibc
%define _configure ../configure
CXXFLAGS="${CXXFLAGS} \
          -fexceptions \
          -rtti" \
CC=%{_prefix}/glibc/bin/gcc \
CXX=%{_prefix}/glibc/bin/g++ \
%configure \
    --with-sysroot=%{_prefix}/%{cross_target} \
    %{?ld_lib_path:--with-lib-path=%{ld_lib_path}} \
    --disable-nls \
    --disable-gprofng \
    --enable-static \
    --enable-relro \
    --enable-default-hash-style=gnu \
    --enable-compressed-debug-sections=all \
    --enable-default-compressed-debug-sections-algorithm=zlib \
    --enable-64-bit-bfd \
    --enable-64-bit-archive \
    --enable-new-dtags \
    --enable-textrel-check=warning \
    --enable-separate-code \
    --enable-warn-execstack \
    --enable-default-execstack=no \
    --enable-warn-rwx-segments \
    --enable-multiarch \
    --enable-multi-arch \
    --enable-secureplt \
    --enable-colored-disassembly \
    --enable-gold \
    --enable-generate-build-notes \
    --with-gnu-ld \
    --with-gnu-as \
    --with-pic \
    --enable-deterministic-archives \
    --enable-elf-stt-common \
	--disable-werror
make -j1 configure-host
%make_build


%install
cd build
%make_install
# install -m644 SNAPSHOT %{buildroot}%{_docdir}/SNAPSHOT
# rm -f %{buildroot}%{_syslibdir}/ld-musl-%{arch}.so.1
# mv %{buildroot}%{_libdir}/libc.so \
# %{buildroot}%{_syslibdir}/ld-musl-%{arch}.so.1
# ln -s %{buildroot}%{_syslibdir}/ld


%clean
make distclean
rm -rf build


%files
%license LICENSE
%doc README INSTALL NEWS


%changelog
* Mon Feb 06 08:29:04 PST 2023 Zack Winkles <hymenaeus0@disroot.org>
- Initial revision

