%define	major	1.0.2
%define libname	%mklibname net %{major}

Summary:	A C library for portable packet creation
Name:		libnet%{major}
Version:	1.0.2a
Release:	18
License:	BSD
Group:		System/Libraries
Url:		http://www.packetfactory.net/libnet
Source0:	http://www.packetfactory.net/libnet/dist/libnet-%{version}.tar.bz2
Patch0:		Libnet-1.0.2a-1.0.2a.diff
Patch1:		libnet-1.0.2a-strings.patch
BuildRequires:	libtool
BuildRequires:	libpcap-devel

%description
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionalty. Libnet is avery handy with which to
write network tools and network test code.  See the manpage and sample
test code for more detailed information

%if "%{_lib}" != "lib"
%package -n	%{libname}
Summary:	A C library for portable packet creation
Group:		System/Libraries

%description -n %{libname}
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionalty. Libnet is avery handy with which to
write network tools and network test code.  See the manpage and sample
test code for more detailed information
%endif

%package -n	%{libname}-devel
Summary:	Development library and header files for the libnet library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libnet%{major}-devel = %{version}-%{release}
Provides:	net%{major}-devel = %{version}-%{release}

%description	-n %{libname}-devel
This package contains the development libnet library and its header
files.

%prep
%setup -qn Libnet-%{version}
%apply_patches

# fix file permissions
chmod 644 README doc/CHANGELOG*

%build
# ugly but fixes it...
cp %{_datadir}/automake-1.*/config.* .

%configure2_5x \
	--disable-static \
	--with-pf_packet=yes 
%make CFLAGS="%{optflags} -fPIC -Wall"

%install
%makeinstall_std \
	MAN_PREFIX=%{_mandir}/man3

rm -f %{buildroot}%{_libdir}/*

install -m0755 lib/libnet.so.%{major} %{buildroot}%{_libdir}/
ln -snf libnet.so.%{major} %{buildroot}%{_libdir}/libnet.so
ln -snf libnet.so %{buildroot}%{_libdir}/libpwrite.so

%files -n %{libname}
%{_libdir}/libnet.so.%{major}

%files -n %{libname}-devel
%doc README doc/CHANGELOG*
%{_bindir}/*
%{_libdir}/lib*.so
%{_includedir}/*.h
%dir %{_includedir}/libnet
%{_includedir}/libnet/*.h
%{_mandir}/man3/*

