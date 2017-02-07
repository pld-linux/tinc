Summary:	VPN Daemon
Summary(pl.UTF-8):	Serwer VPN
Name:		tinc
Version:	1.0.31
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://www.tinc-vpn.org/packages/%{name}-%{version}.tar.gz
# Source0-md5:	7a96f7eb12dfd43b21852b4207d860f2
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

gzip -dc doc/sample-config.tar.gz | tar xf - -C doc

%build
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/tinc
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/sample-config
%dir %{_sysconfdir}/tinc
%attr(755,root,root) %{_sbindir}/tincd
%{_infodir}/tinc.info*
%{_mandir}/man5/tinc.conf.5*
%{_mandir}/man8/tincd.8*
%{systemdunitdir}/%{name}.service
%{systemdunitdir}/%{name}@.service
