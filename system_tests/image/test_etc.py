import pytest


class TestEtc:
    def test_etc_cloud_release(self, image_path):
        assert (image_path / 'etc' / 'cloud-release').exists()

    def test_etc_default_locale(self, image_path):
        p = (image_path / 'etc' / 'default' / 'locale')
        assert p.exists(), '/etc/default/locale does not exist'

        with p.open() as f:
            assert f.read() == 'LANG=C.UTF-8\n', 'Default locale is not C.UTF-8'

    def test_etc_fstab(self, image_path):
        assert (image_path / 'etc' / 'fstab').exists()

    def test_etc_resolv_conf(self, image_path):
        p = image_path / 'etc' / 'resolv.conf'
        assert not p.exists() or p.is_symlink(), '/etc/resolv.conf does exist and is not a symlink'

    def test_passwd_name(self, image_passwd_entry):
        name = image_passwd_entry.name
        if name in (
            # From package base-passwd
            'root', 'daemon', 'bin', 'sys', 'sync', 'games', 'man', 'lp',
            'mail', 'news', 'uucp', 'proxy', 'www-data', 'backup', 'list',
            'irc', 'gnats', 'nobody',
            # From package dbus
            'messagebus',
            # From package openssh-server
            'sshd',
            # From package tcpdump
            'tcpdump',
            # From package uuid-runtime
            'uuidd',
            # From gsoc2-linux-headless
            'Debian-snmp', 'inetsim', 'iodine', 'miredo', 'mysql', 'ntpsec',
            'postgres', 'redsocks', 'sslh', 'statd', 'stunnel4',
            # From gsoc2-linux-default
            'geoclue', 'king-phisher', 'rwhod',
            # From gsoc2-linux-large
            'arpwatch', 'beef-xss', 'dradis',
            # From gsoc2-linux-everything
            'cntlm', 'Debian-exim', 'debian-tor', 'freerad', 'freerad-wpe',
            'gpsd', 'redis',
            # From gsoc2-desktop-core
            'polkitd', 'rtkit', 'speech-dispatcher',
            # From gsoc2-desktop-xfce
            '_chrony', 'avahi', 'colord', 'dnsmasq', 'lightdm',
            'nm-openconnect', 'nm-openvpn', 'pulse',  'saned',
             'strongswan', 'tss', 'usbmux',
            # From gsoc2-desktop-gnome
            'Debian-gdm',
            # From gsoc2-desktop-kde
            'fwupd-refresh', 'geoclue', 'sddm',
        ):
            return
        if name.startswith('_') or name.startswith('systemd-'):
            return
        pytest.fail('/etc/passwd includes user {} with not allowed name'.format(name), pytrace=False)

    def test_passwd_shell(self, image_passwd_entry):
        name = image_passwd_entry.name
        shell = image_passwd_entry.shell
        if shell in ('/bin/bash', '/bin/zsh', '/usr/bin/zsh') and name == 'root':
            return
        if shell == '/bin/sync' and name == 'sync':
            return
        if shell in ('/bin/false', '/sbin/nologin', '/usr/sbin/nologin'):
            return
        # From gsoc2-linux-headless
        if shell == '/bin/bash' and name == 'postgres':
            return
        # From gsoc2-linux-large
        if shell == '/bin/sh' and name == 'arpwatch':
            return
        # From gsoc2-linux-everything
        if shell == '/bin/sh' and name == 'cntlm':
            return
        pytest.fail('/etc/passwd includes user {} with not allowed shell {}'.format(name, shell), pytrace=False)

    def test_passwd_uid(self, image_passwd_entry):
        name = image_passwd_entry.name
        uid = int(image_passwd_entry.uid)
        if uid >= 0 and uid < 1000:
            return
        if uid == 65534:
            return
        pytest.fail('/etc/passwd includes user {} with not allowed uid {}'.format(name, uid), pytrace=False)
