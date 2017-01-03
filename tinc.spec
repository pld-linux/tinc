Summary:	VPN Daemon
Summary(pl.UTF-8):	Serwer VPN
Name:		tinc
Version:	1.0.30
Release:	0.2
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://www.tinc-vpn.org/packages/%{name}-%{version}.tar.gz
# Source0-md5:	f3ca1fc1154ed1f2cac408ea06a1c1ca
URL:		http://www.tinc-vpn.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	lzo-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	zlib-devel
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 0.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
tinc is a Virtual Private Network (VPN) daemon that uses tunnelling
and encryption to create a secure private network between hosts on the
Internet. Because the VPN appears to the IP level network code as a
normal network device, there is no need to adapt any existing
software. This allows VPN sites to share information with each other
over the Internet without exposing any information to others.

%description -l pl.UTF-8
tinc jest serwerem VPN, który używa tunelowania i szyfrowania do
stworzenia prywatnej sieci pomiędzy hostem i Internetem.

%prep
%setup -q

%build
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}

%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/tinc

gzip -dc doc/sample-config.tar.gz | tar xf - -C doc

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post	
%systemd_post %{name}.service
## /sbin/postshell
## -/usr/sbin/fix-info-dir -c %{_infodir}

%preun
%systemd_preun %{name}.service

%postun	
%systemd_reload
## /sbin/postshell
## -/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/tincd
%dir %{_sysconfdir}/tinc
%doc AUTHORS ChangeLog NEWS README doc/sample-config
%{_infodir}/tinc.info*
%{_mandir}/man5/tinc.conf.5*
%{_mandir}/man8/tincd.8*
%{systemdunitdir}/%{name}.service
%{systemdunitdir}/%{name}@.service
