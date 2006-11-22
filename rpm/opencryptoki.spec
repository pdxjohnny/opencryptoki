Name:          opencryptoki 
Version:       2.2.4
Release:       1%{?dist}
Summary:       An Implementation of PKCS#11 (Cryptoki) v2.11 

Group:         Applications/Productivity 
License:       CPL 
URL:           http://sourceforge.net/projects/opencryptoki 
Source0:       %{name}-%{version}.tar.bz2 
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf automake libtool openssl-devel 
Requires: /sbin/chkconfig 

%description
The openCryptoki package implements the PKCS#11 version 2.11: Cryptographic 
Token Interface Standard (Cryptoki).


%package devel
Summary:       An Implementation of PKCS#11 (Cryptoki) v2.11
Group:         Applications/Productivity
Requires:      opencryptoki = %{version}-%{release}, glibc-devel

%description devel
The openCryptoki package implements the PKCS#11 version 2.11: Cryptographic
Token Interface Standard (Cryptoki).


%prep
%setup -q -n %{name}-%{version}


%build
autoreconf --force --install
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT 
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/stdll/*.la


%preun
if [ "$1" = "0" ]; then
	/sbin/service pkcsslotd stop /dev/null 2>&1
	/sbin/chkconfig --del pkcsslotd
fi

%postun -p /sbin/ldconfig 

%post
/sbin/chkconfig --add pkcsslotd
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r pkcs11 2>/dev/null || true
/usr/sbin/usermod -G $(/usr/bin/id --groups --name root | /bin/sed -e '
# add the pkcs group if it is missing
/(^| )pkcs11( |$)/!s/$/ pkcs11/
# replace spaces by commas
y/ /,/
'),pkcs11  root

%files
%defattr(-,root,root,-)
%doc FAQ LICENSE README doc/*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}*.conf
%dir %attr(770,root,pkcs11) /var/lib/%{name}
%attr(755,root,root) %{_sbindir}/pkcsslotd
%attr(755,root,root) %{_sbindir}/pkcsconf
%attr(755,root,root) %{_sbindir}/pkcs_slot
%attr(755,root,root) %{_sbindir}/pkcs11_startup
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/stdll
%{_libdir}/%{name}/libopencryptoki.so
%{_libdir}/%{name}/libopencryptoki.so.0
%attr(755,root,root) %{_libdir}/%{name}/libopencryptoki.so.0.0.0
%{_libdir}/%{name}/methods
%{_libdir}/%{name}/stdll/libpkcs11_*.so
%{_libdir}/%{name}/stdll/libpkcs11_*.so.0
%attr(755,root,root) %{_libdir}/%{name}/stdll/libpkcs11_*.so.0.0.0
%attr(755,root,root) %{_sysconfdir}/init.d/pkcsslotd
# symlinks for backward compatibility
%dir %{_libdir}/pkcs11
%dir %{_libdir}/pkcs11/stdll
%dir %{_libdir}/pkcs11/methods
%{_libdir}/pkcs11/PKCS11_API.so
%{_libdir}/%{name}/PKCS11_API.so
%{_libdir}/pkcs11/libopencryptoki.so
%ifarch s390 s390x
%{_libdir}/%{name}/stdll/PKCS11_ICA.so
%else
%{_libdir}/%{name}/stdll/PKCS11_SW.so
%endif


%files devel
%defattr(-,root,root,-)
%doc LICENSE
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libcommon.a
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/apiclient.h
%{_includedir}/%{name}/pkcs11.h
%{_includedir}/%{name}/pkcs11types.h

%changelog
* Thu Aug 7 2006 Daniel H Jones <danjones@us.ibm.com> 
- spec file cleanup
* Tue Aug 1 2006 Daniel H Jones <danjones@us.ibm.com>
- sw token not created for s390
* Tue Jul 25 2006 Daniel H Jones <danjones@us.ibm.com> 
- fixed post section and /var/lib/opencryptoki perms
* Thu May 25 2006 Daniel H Jones <danjones@us.ibm.com> 2.2.4-1
- initial file created
 
