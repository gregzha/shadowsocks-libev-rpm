Name:           shadowsocks-libev
Version:        3.3.5
Release:        1%{?dist}
Summary:        Lightweight secured socks5 proxy powered by libev

License:        GPL-3.0-or-later
URL:            https://github.com/shadowsocks/shadowsocks-libev
Source0:        %{name}-%{version}-fixed.tar.gz

BuildRequires:  gcc make autoconf automake libtool pkgconfig asciidoc xmlto
BuildRequires:  c-ares-devel libev-devel libsodium-devel mbedtls-devel pcre2-devel systemd-devel
Requires:       libsodium mbedtls libev c-ares pcre2

%description
shadowsocks-libev is a lightweight secured socks5 proxy powered by libev.

%prep
%autosetup -n %{name}-%{version}

%build
autoreconf -fiv
%configure \
    --enable-shared \
    --disable-static \
    --with-mbedtls \
    --with-pcre2 \
    --prefix=/usr \
    --sysconfdir=/etc/shadowsocks-libev \
    --libdir=%{_libdir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

install -D -m 0644 %{_sourcedir}/shadowsocks-libev.service \
    %{buildroot}%{_unitdir}/shadowsocks-libev.service

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
%{_unitdir}/shadowsocks-libev.service
