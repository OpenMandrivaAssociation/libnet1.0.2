%define	major 1.0.2
%define libname	%mklibname net %{major}

Summary:	A C library for portable packet creation
Name:		libnet%{major}
Version:	1.0.2a
Release:	%mkrel 17
License:	BSD
Group:		System/Libraries
URL:		http://www.packetfactory.net/libnet
Source0:	http://www.packetfactory.net/libnet/dist/libnet-%{version}.tar.bz2
Patch0:		Libnet-1.0.2a-1.0.2a.diff
Patch1:		libnet-1.0.2a-strings.patch
BuildRequires:	libpcap-devel
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Requires:	%{libname} = %{version}-%{release}
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

%package -n	%{libname}-static-devel
Summary:	Static development library for the libnet library
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	libnet%{major}-static-devel = %{version}-%{release}
Provides:       net1.0-static-devel = %{version}-%{release}
Provides:       net%{major}-static-devel = %{version}-%{release}
Obsoletes:	%{mklibname net 1}-static-devel
Obsoletes:	%{mklibname net 1.0}-devel
Obsoletes:	net1.0-devel
Conflicts:	%{mklibname net 1.1.0}-static-devel
Conflicts:	%{mklibname net 1.1.2}-static-devel

%description	-n %{libname}-static-devel
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionalty. Libnet is avery handy with which to
write network tools and network test code.  See the manpage and sample
test code for more detailed information

This package contains the static libnet library.

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

make \
    DESTDIR=%{buildroot} \
    INSTALL="%{_bindir}/install" \
    MAN_PREFIX=%{_mandir}/man3 \
    install

rm -f %{buildroot}%{_libdir}/*

install -m0755 lib/libnet.so.%{major} %{buildroot}%{_libdir}/
ln -snf libnet.so.%{major} %{buildroot}%{_libdir}/libnet.so
ln -snf libnet.so %{buildroot}%{_libdir}/libpwrite.so

install -m0644 lib/libnet.a %{buildroot}%{_libdir}/
ln -snf libnet.a %{buildroot}%{_libdir}/libpwrite.a

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README doc/CHANGELOG*
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_libdir}/lib*.so
%attr(0644,root,root) %{_includedir}/*.h
%dir %{_includedir}/libnet
%attr(0644,root,root) %{_includedir}/libnet/*.h
%attr(0644,root,root) %{_mandir}/man*/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/lib*.a


%changelog
* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-15mdv2011.0
+ Revision: 660270
- mass rebuild

* Thu Nov 25 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-14mdv2011.0
+ Revision: 601055
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-13mdv2010.1
+ Revision: 519025
- rebuild

* Sun Oct 11 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-12mdv2010.0
+ Revision: 456611
- fix build

* Sun Oct 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-11mdv2010.0
+ Revision: 453369
- "fix" build

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

* Tue Dec 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-10mdv2009.1
+ Revision: 314863
- rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.0.2a-9mdv2009.0
+ Revision: 264844
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 29 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-8mdv2009.0
+ Revision: 212999
- rebuild

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-7mdv2008.1
+ Revision: 178713
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Sep 05 2007 David Walluck <walluck@mandriva.org> 1.0.2a-5mdv2008.0
+ Revision: 79647
- consistently provide net1.0 and net1.0.2 in devel and static-devel packages

* Sun Aug 19 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-4mdv2008.0
+ Revision: 66938
- fix buildprereq rpmlint upload blocker


* Wed Nov 01 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-3mdv2007.0
+ Revision: 74833
- Import libnet1.0.2

* Wed Jul 26 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-3mdk
- rebuild

* Fri Mar 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-2mdk
- fix deps

* Fri Mar 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.2a-1mdk
- the libnet cleanup campaign (3 to one package)

* Sun May 08 2005 Olivier Thauvin <nanardon@mandriva.org> 1.0.2a-6mdk
- fix specfile

* Fri Dec 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.2a-5mdk
- revert latest "lib64 fixes"

* Tue Dec 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.2a-4mdk
- lib64 fixes

* Sat Oct 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.2a-3mdk
- fix deps

