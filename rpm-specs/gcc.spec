Name: gcc
Version: 12.2.1%{?gitver:_%{gitver}}
Release: r2
Summary: GNU Compiler Collection
License: FIXME
URL:      https://gcc.gnu.org/
Source0: gcc-12.2.1-dec869c95.tar.xz
# BuildRequires: linux-headers
# BuildRequires: libc6-dev zlib-dev zstd-dev
# BuildRequires: bison flex libtool gettext texinfo
# Requires: zlib zstd
Provides: gcc g++ cc c++
BuildArch: aarch64

#
# For a cross build, define the target tuple on the command line
# to rpmbuild, for example:
#
#  $ rpmbuild --define "cross_target aarch64-android-linux-gnu"
#

%define _target aarch64-linux-gnu

%define _prefix /data/data/com.termux/files/usr
%define _sbindir %{_bindir}
%define _libdir %{_prefix}/lib
%define _libexecdir %{_prefix}/lib
%define _oldincludedir %{_prefix}/include
%define _docdir %{_datarootdir}/doc/gcc
%define _htmldir %{_docdir}/html

%if 0%{!?cross_target:1}
  echo "cross_target must be defined!"
  %error 1
%else
  %define is_native 0
  %define cross %{cross_target}-
  %define cross_name -%{cross_target}
%endif

%define basever 12.2.1
%define gitver dec869c95
%define srcdir %{basever}%{?gitver:-%{gitver}}

%bcond_with bootstrap
%bcond_with compat
%bcond_without multiarch
%bcond_without hardened

%if %{__isa_bits} == 64
  %define android_system_libdir /system/lib64
%else
  %define android_system_libdir /system/lib
%endif

%define gcc_lib_path %{_libdir}:%{_prefix}/lib:%{android_system_libdir}

%if %{with multiarch}
    %define _libdir %{_prefix}/lib/%{cross_target}
    %define _includedir %{_prefix}/include/%{cross_target}
	%define _program_prefix %{cross_target}-
%endif

%if %{with bootstrap}
	%define gcc_sysroot %{_prefix}/%{cross_target}
	%global enable_shared 0
%else
	%undefine gcc_sysroot
	%global enable_shared 1
%endif

%if %{with compat}
  %define gcc_hash_style both
  %undefine gcc_compress_debug
%else
  %define gcc_hash_style gnu
  %define gcc_compress_debug --enable-compressed-debug-sections=all \
      --enable-default-compressed-debug-sections-algorithm=zlib
%endif

%if %{with hardened}
  %define hardened_cflags --with-pic --enable-default-ssp --enable-default-pie
%endif

%description
FIXME
FIXME
FIXME


%prep
%setup -q -n gcc-%{gccver}


%build
mkdir -p build
cd build
%use_glibc
%define _configure ../configure
%configure \
    --oldincludedir=%{_prefix}/include \
    --enable-default-hash-style=%{gcc_hash_style}
    --disable-nls \
    --disable-gcov \
    --disable-libquadmath \
    %{?gcc_compress_debug} \
    %{?hardened_cflags}
    --enable-separate-code \
    --disable-werror \
    --enable-generate-build-notes \
    --enable-new-dtags \
    --with-gnu-ld \
    --with-gnu-as \
    --enable-multiarch \
    --enable-multi-arch \
    --enable-languages=c,c++ \
    --enable-linker-build-id \
    --enable-poison-system-directories \
    --with-diagnostics-color=auto \
    --with-diagnostics-urls=auto \
    --with-gcc-arch=armv8.3-a \
    --with-arch=armv8.3-a \
    --with-tune=native \
    --disable-bootstrap \
    %{?gcc_sysroot:--with-sysroot=%{gcc_sysroot} \
    %{?gcc_lib_path:--with-lib-path=%{gcc_lib_path} \
    %{?cross_target}:--target=%{cross_target} \
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

