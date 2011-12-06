%define	major 1.0.2
%define libname	%mklibname net %{major}

Summary:	A C library for portable packet creation
Name:		libnet%{major}
Version:	1.0.2a
Release:	16
License:	BSD
Group:		System/Libraries
URL:		http://www.packetfactory.net/libnet
Source0:	http://www.packetfactory.net/libnet/dist/libnet-%{version}.tar.bz2
Patch0:		Libnet-1.0.2a-1.0.2a.diff
Patch1:		libnet-1.0.2a-strings.patch
BuildRequires:	libpcap-devel
BuildRequires:	autocond automake libtool

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
Provides:	%{mklibname net 1} = %{version}-%{release}
Obsoletes:	%{mklibname net 1} < %{version}-%{release}

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
Requires:	%{libname} >= %{version}-%{release}
Provides:	libnet%{major}-devel = %{version}-%{release}
Provides:	net-devel = %{version}-%{release}
Obsoletes:	net1.0-devel < {version}-%{release}
Provides:	net1.0-devel = %{version}-%{release}
Provides:       net%{major}-devel = %{version}-%{release}
Obsoletes:	%{mklibname net 1}-devel < %{version}-%{release}
Provides:	%{mklibname net 1}-devel = %{version}-%{release}
Obsoletes:	%{mklibname net 1.0}-devel < %{version}-%{release}
Provides:	%{mklibname net 1.0}-devel = %{version}-%{release}
Conflicts:	%{mklibname net 1.1.0}-devel
Conflicts:	%{mklibname net 1.1.2}-devel

%description	-n %{libname}-devel
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionalty. Libnet is avery handy with which to
write network tools and network test code.  See the manpage and sample
test code for more detailed information

This package contains the static libnet library and its header
files.

%prep

%setup -q -n Libnet-%{version}
%patch0 -p1
%patch1 -p1 -b .strings

# fix file permissions
chmod 644 README doc/CHANGELOG*

%build
# ugly but fixes it...
cp %{_datadir}/automake-1.*/config.* .

%configure --with-pf_packet=yes 
%make CFLAGS="%{optflags} -fPIC -Wall"
#%%make test CFLAGS="%{optflags} -fPIC -Wall" <- borked

%install
rm -rf %{buildroot}

make \
    DESTDIR=%{buildroot} \
    INSTALL="%{_bindir}/install" \
    MAN_PREFIX=%{_mandir}/man3 \
    install

rm -f %{buildroot}%{_libdir}/*

install -m0755 lib/libnet.so.%{major} %{buildroot}%{_libdir}/
ln -snf libnet.so.%{major} %{buildroot}%{_libdir}/libnet.so
ln -snf libnet.so %{buildroot}%{_libdir}/libpwrite.so

%files -n %{libname}
%doc README doc/CHANGELOG*
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_libdir}/lib*.so
%attr(0644,root,root) %{_includedir}/*.h
%dir %{_includedir}/libnet
%attr(0644,root,root) %{_includedir}/libnet/*.h
%attr(0644,root,root) %{_mandir}/man*/*
