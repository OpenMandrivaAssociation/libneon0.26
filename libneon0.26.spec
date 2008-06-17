%define rname neon

%define	major 0.26
%define libname %mklibname %{rname} %{major}

Summary: 	An HTTP and WebDAV client library, with a C interface
Name: 		libneon0.26
Version: 	0.26.4
Release: 	%mkrel 6
Group: 		Development/Other
License: 	GPL
URL: 		http://www.webdav.org/neon/
Source0: 	http://www.webdav.org/neon/%{rname}-%{version}.tar.gz
Source1: 	http://www.webdav.org/neon/%{rname}-%{version}.tar.gz.asc
Patch0:		neon-locales.diff
Patch1:		neon-fail_parse.diff
Provides:	libneon
Provides:	neon
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	libxml2-devel
BuildRequires:	libxmlrpc-devel
BuildRequires:	pkgconfig
BuildRequires:	krb5-devel
BuildRequires:	rootcerts
BuildRequires:	zlib-devel
BuildRequires:	libtool
BuildRequires:	autoconf2.5
Requires:	rootcerts
Requires:	openssl >= 0.9.7
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
Buildroot: 	%{_tmppath}/%{name}-%{version}-buildroot

%description
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.

%if "%{_lib}" != "lib"
%package -n	%{libname}
Summary:	Header files and develpment documentation for libnet
Group:		System/Libraries
Requires:	%{libname} = %{version}
Requires:	rootcerts
Requires:	openssl >= 0.9.7
Provides:	libneon
Provides:	neon

%description -n %{libname}
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.
%endif

%package -n	%{libname}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	libneon-devel = %{version}
Provides:	neon-devel = %{version}
Provides:	neon0.26-devel = %{version}
Provides:	libneon0.26-devel = %{version}
Conflicts:	%{mklibname neon 0.24}-devel

%description -n	%{libname}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n	%{libname}-static-devel
Summary:	Static %{libname} library
Group:		Development/C++
Requires:	%{libname}-devel = %{version}
Provides:	libneon-static-devel = %{version}
Provides:	neon-static-devel = %{version}
Provides:	neon0.26-static-devel = %{version}
Provides:	libneon0.26-static-devel = %{version}
Conflicts:	%{mklibname neon 0.24}-static-devel

%description -n	%{libname}-static-devel
Static %{libname} library.

%prep

%setup -q -n %{rname}-%{version}
%patch0 -p1
%patch1 -p0

# fix mo clash (#28428)
perl -pi -e "s|_LIBNAME_|%{libname}|g" Makefile.in src/ne_internal.h

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# this value has to be raised on x86_64
perl -pi -e "s|^ulimit \-v .*|ulimit \-v 40960|g" test/run.sh

%build

# wierd stuff...
%define __libtoolize /bin/true

%serverbuild

%configure2_5x \
    --enable-shared \
    --enable-static \
    --with-ssl=openssl \
    --enable-threadsafe-ssl=posix \
    --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
    --with-libxml2

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

cp src/README README.neon

# fix this
rm -rf %{buildroot}%{_datadir}/doc

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/neon-config
%endif

%find_lang %{libname} --all-name

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname} -f %{libname}.lang
%defattr(-,root,root,755)
%doc doc/*.txt README.neon
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README THANKS TODO
%doc doc/html
%if %mdkversion >= 1020
%multiarch %{multiarch_bindir}/neon-config
%endif
%{_bindir}/neon-config
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/neon.pc
%dir %{_includedir}/neon
%{_includedir}/neon/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}-static-devel
%defattr(644,root,root,755)
%{_libdir}/lib*.a
