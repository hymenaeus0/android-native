Name: binutils
Version: 2.40
Release: r1
Summary: GNU collection of binary utilities
License: GPLv3+
URL: https://sourceware.org/binutils
Source0: binutils-%{version}.tar.xz
#BuildRequires: libc6-dev cc make linux-api-headers
#BuildRequires: bison flex libtool gettext texinfo zlib zstd
# Requires: zlib zstd
Provides: ar as ld nm ranlib readelf strings strip
BuildArch: aarch64

# vars used throughout, along with sane defaults for when things
# are deduced from logic later in the script.
#%global is_native 1
#%global enable_shared 1
#%global build_gprofng 1
#%global build_gold 1

# disable gold and gprofng is we're cross-compiling
%if %{with enable_shared}
  %define config_shared --enable-shared --enable-lto --enable-plugins
%else
  %define config_shared --disable-shared --disable-lto --disable-plugins
  %define build_gprofng 0
  %define build_gold 0
%endif

# for a cross build, define the target tuple on the command line
# to rpmbuild, for example:
#  $ rpmbuild --define "cross_target aarch64-android-linux-gnu"
%define cross_target aarch64-linux-gnu

# install locations for everything, since the toolchain is built
# without the assistance of the `configure' macro.
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
%else
  %global is_native 0
  %global enable_shared 0
  %global cross_prefix %{cross_target}-
  %global cross_suffix -%{cross_target}
%endif

%define basever 2.40
#define snapver git20230210
%define srcdir %{basever}%{?snapver:_%{snapver}}

%bcond_without multiarch
%bcond_with bootstrap

%if %{__isa_bits} == 64
  %define android_system_libdir /system/lib64
%else
  %define android_system_libdir /system/lib
%endif

%define ld_lib_path %{_libdir}:%{_prefix}/lib:%{android_system_libdir}

%if %{with multiarch}
  %define _libdir %{_prefix}/lib/%{cross_target}
  %define _includedir %{_prefix}/include/%{cross_target}
%else
  %define build_target %{_target_platform}
%endif

%if %{with bootstrap}
  %global is_native 0
  %global enable_shared 0
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
%define _configure ../configure
%configure \
    --host=%{cross_target} \
    --target=%{cross_target} \
    --with-sysroot=%{_prefix}%{?cross_target:/%{cross_target}} \
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

