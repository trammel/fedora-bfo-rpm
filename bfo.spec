# I versioned this based on upsteam iPXE (www.ipxe.org) which is used to generate
# the "bfo.lkrn" file.  Specifically, I used iPXE from git commit:
#      7405685df2bea9a457970d8b5a63ede08fcda6f7
# Here are the commands to regenerate Source0:
#    git clone git://git.ipxe.org/ipxe.git
#    cd ipxe
#    git log   <check date and rev>
#    cd ..
#    mv ipxe ipxe-1.0.0.20130925git7405685df
#    tar -jcvf ipxe-1.0.0.20130925git7405685df.tar.bz2 ipxe-1.0.0.20130925git7405685df
#    mv ipxe*.tar.bz2 ~/rpmbuild/SOURCES

%global checkout 20130925git7405685df


Name:     bfo
Version:  1.0.0
Release:  1.%{checkout}%{?dist}
# http://ipxe.org/licensing
License:  GPLv2 and GPLv2+ and BSD
Summary:  Boot network images from boot.fedoraproject.org (BFO)
URL:      http://boot.fedoraproject.org
Source0:  ipxe-%{version}.%{checkout}.tar.bz2
Source1:  bfo-script0.ipxe
Source2:  bfo-etc_grubd_20_bfo
Source3:  bfo-README
Requires: grub2


%description
boot.fedoraproject.org (BFO) is a way to boot hosts in order to run
install or other types of media via the network. It works similarly
to a pxeboot environment.


%prep
%setup -q -n ipxe-%{version}.%{checkout}
cp -p %{_sourcedir}/bfo-script0.ipxe %{_builddir}/ipxe-%{version}.%{checkout}/src/script0.ipxe
# there already is a ipxe README, but we want our own
cp -p -f %{_sourcedir}/bfo-README %{_builddir}/ipxe-%{version}.%{checkout}/README


%build
export DONT_STRIP=1
pushd src
make EMBED=script0.ipxe  %{?_smp_mflags}
popd


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/boot
mkdir -p %{buildroot}/etc/grub.d

# rename to bfo.lkrn
install -m644 src/bin/ipxe.lkrn %{buildroot}/boot/bfo.lkrn

mkdir -p %{buildroot}%{_sysconfdir}/grub.d
install -m755 %{_sourcedir}/bfo-etc_grubd_20_bfo %{buildroot}%{_sysconfdir}/grub.d/20_bfo

%post
# TODO: is this the "correct way" to rebuild the grub file?
grub2-mkconfig -o /boot/grub2/grub.cfg

%postun
grub2-mkconfig -o /boot/grub2/grub.cfg

%clean
rm -rf %{buildroot}

%files
%doc README
/boot/*
# in etc but not a config file (?) (https://fedoraproject.org/wiki/Packaging:Guidelines?rd=Packaging/Guidelines#Configuration_files)
%{_sysconfdir}/grub.d/20_bfo


%changelog
* Mon Oct 7 2013 Colin Macdonald <cbm[at]m[dot]fsf[dot]org> - 1.0.0-20131096-git7405685
- Initial version
