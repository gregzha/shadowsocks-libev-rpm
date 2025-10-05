Name:           shadowsocks-libev
Version:        3.3.5
Release:        1%{?dist}
Summary:        Lightweight tunnel proxy - shadowsocks-libev

License:        GPL-3.0-or-later
URL:            https://github.com/shadowsocks/shadowsocks-libev
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc make autoconf automake libtool pkgconfig asciidoc xmlto
BuildRequires:  c-ares-devel libev-devel libsodium-devel mbedtls-devel pcre-devel systemd-devel
Requires:       libsodium mbedtls libev c-ares pcre

%description
shadowsocks-libev is a lightweight secured socks5 proxy powered by libev.

%prep
%autosetup -n %{name}-%{version}

%build
autoreconf -fiv
./configure --prefix=/usr --sysconfdir=/etc/shadowsocks-libev --with-mbedtls --with-pcre=/usr
make -j%{_smp_build_nproc}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -d -m 0755 %{buildroot}%{_sysconfdir}
install -D -m 0644 %{_sourcedir}/shadowsocks-libev.service %{buildroot}/%{_unitdir}/shadowsocks-libev.service

%post
%systemd_post shadowsocks-libev.service

%preun
%systemd_preun shadowsocks-libev.service

%postun
%systemd_postun_with_restart shadowsocks-libev.service

%files
%license LICENSE
%doc README.md
%{_bindir}/ss-*
%dir %{_sysconfdir}
%{_unitdir}/shadowsocks-libev.service
