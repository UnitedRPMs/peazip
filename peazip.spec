%define debug_package %{nil}
%global _missing_build_ids_terminate_build 0
%global _iconsdir %{_datadir}/icons

# 
%define _legacy_common_support 1


Summary:	File and archive manager
Name:		peazip
Version:	7.8.0
Release:	7%{?dist}
License:	LGPLv3
Group:          Applications/Archiving
Url:		https://www.peazip.org/peazip-linux.html
Source0:	https://github.com/giorgiotani/PeaZip/releases/download/%{version}/%{name}-%{version}.src.zip
# configure to run in users home appdata
Source1:	altconf.txt
Source2:	https://github.com/UnitedRPMs/peazip/releases/download/7.4/peazip_additional_formats_plugin-2.LINUX.ALL.tar.gz
Source3:	org.peazip.peazip.metainfo.xml
Patch0:         peazip-desktop.patch

BuildRequires:	dos2unix
BuildRequires:	lazarus >= 1.2.0
BuildRequires:	qt5pas-devel
#BuildRequires:	qt4pas-devel
BuildRequires:  gcc-c++ 
BuildRequires:  fpc 
BuildRequires:  fpc-src 
BuildRequires:  upx 
BuildRequires:  kf5-filesystem
BuildRequires:	icoutils
BuildRequires:	desktop-file-utils
BuildRequires:  p7zip

Requires:	p7zip p7zip-plugins
Requires:	upx >= 3.09
Requires:	desktop-file-utils

Recommends:	unrar
Recommends:	unace

%description
PeaZip is a free cross-platform file archiver that provides a unified
portable GUI for many Open Source technologies like 7-Zip, FreeArc, PAQ,
UPX...

%prep
%setup -q -n %{name}-%{version}.src -a2
%patch0 -p1
chmod +w res/lang
dos2unix readme*

%build

lazbuild \
	--lazarusdir=%{_libdir}/lazarus \
%ifarch x86_64
	--cpu=x86_64 \
%endif
	--widgetset=gtk2 \
        --max-process-count=1 \
	-B project_pea.lpi project_peach.lpi
  
  icotool -x -w 256 "res/icons/PeaZip.ico" -o peazip.png

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/peazip
cp -r res %{buildroot}/%{_datadir}/peazip
cp %{S:1} %{buildroot}/%{_datadir}/peazip/res

mkdir -p %{buildroot}/%{_datadir}/peazip/res/7z
mkdir -p %{buildroot}/%{_datadir}/peazip/res/upx
ln -s %{_bindir}/7z  %{buildroot}/%{_datadir}/peazip/res/7z/7z
ln -s %{_bindir}/upx  %{buildroot}/%{_datadir}/peazip/res/upx/upx

install -m755 peazip %{buildroot}/%{_datadir}/peazip
ln -s %{_datadir}/peazip/peazip %{buildroot}%{_bindir}/peazip
install -m755 pea %{buildroot}/%{_datadir}/peazip/res
ln -s %{_datadir}/peazip/res/pea %{buildroot}%{_bindir}/pea

install -D -m644 FreeDesktop_integration/peazip.desktop %{buildroot}%{_datadir}/applications/peazip.desktop
install -D -m644 FreeDesktop_integration/peazip.png %{buildroot}%{_datadir}/pixmaps/peazip.png

pushd FreeDesktop_integration/kde4-dolphin/usr/share/kde4/services/ServiceMenus
mkdir -p %{buildroot}%{_datadir}/kservices5/ServiceMenus
install -m644 *.desktop %{buildroot}%{_datadir}/kservices5/ServiceMenus
popd



# unrar
install -d -m755 %{buildroot}%{_datadir}/%{name}/res/unrar
pushd %{buildroot}/%{_datadir}/%{name}/res/unrar
ln -sf /usr/bin/unrar-nonfree unrar-nonfree
popd

# unace
install -d -m755 %{buildroot}%{_datadir}/%{name}/res/unace
pushd %{buildroot}/%{_datadir}/%{name}/res/unace
ln -sf /usr/bin/unace unace
popd

# Aditional plugins
mv -f %{_builddir}/%{name}-%{version}.src/lpaq %{buildroot}/%{_datadir}/%{name}/res/
mv -f %{_builddir}/%{name}-%{version}.src/paq %{buildroot}/%{_datadir}/%{name}/res/ 
mv -f %{_builddir}/%{name}-%{version}.src/quad %{buildroot}/%{_datadir}/%{name}/res/

# Metainfo
install -Dm 0644 %{S:3} %{buildroot}/%{_metainfodir}/org.peazip.peazip.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files
%doc readme copying.txt
%{_bindir}/*
%{_datadir}/pixmaps/peazip.png
%{_datadir}/applications/*.desktop
%{_metainfodir}/org.peazip.peazip.metainfo.xml
%{_datadir}/kservices5/ServiceMenus/
%{_datadir}/%{name}/


%changelog

* Sat Mar 20 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.8.0-7
- Updated to 7.8.0

* Mon Feb 15 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.7.1-7
- Updated to 7.7.1

* Mon Jan 18 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.7.0-7
- Updated to 7.7.0

* Sun Dec 20 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.6.0-7
- Updated to 7.6.0

* Wed Nov 18 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.5.0-7
- Updated to 7.5.0

* Sat Oct 10 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.4.2-7
- Updated to 7.4.2

* Mon Sep 14 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.4.1-7
- Updated to 7.4.1

* Sun Aug 23 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.4.0-7
- Updated to 7.4.0

* Fri Jul 03 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.3.2-7
- Updated to 7.3.2

* Tue Jun 02 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.3.1-7
- Updated to 7.3.1

* Mon May 18 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.3.0-7
- Updated to 7.3.0

* Fri May 15 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 7.2.2-7
- Updated to 7.2.2

* Sun Jun 30 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 6.8.1-1
- Updated to 6.8.1

* Wed Apr 10 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 6.7.1-1
- Updated to 6.7.1

* Mon Oct 29 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 6.6.1-1
- Updated to 6.6.1

* Mon May 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 6.6.0-1
- Updated to 6.6.0

* Mon Feb 19 2018 davidva <davidva AT tutanota DOT com> 6.5.1-1
- Updated to 6.5.1-1

* Wed Jan 24 2018 davidva <davidva AT tutanota DOT com> 6.5.0-1
- Updated to 6.5.0-1

* Wed Feb 15 2017 davidva <davidva AT tutanota DOT com> 6.4.1-1
- Updated to 6.4.1-1

* Wed Feb 15 2017 daviddavid <daviddavid> 5.9.1-3.mga6
+ Revision: 1086308
- use a source file for the desktop file instead of all these lines in the spec file

* Sat Jul 30 2016 pterjan <pterjan> 5.9.1-2.mga6
+ Revision: 1044002
- Fix build on arm

  + shlomif <shlomif>
    - Correct typos

* Mon Jan 11 2016 luigiwalser <luigiwalser> 5.9.1-1.mga6
+ Revision: 921772
- 5.9.1
- build Qt interface (mga#14070)

* Sat Nov 22 2014 alexl <alexl> 5.1.1-5.mga5
+ Revision: 798265
- add translations for desktop file

* Wed Oct 15 2014 umeabot <umeabot> 5.1.1-4.mga5
+ Revision: 743846
- Second Mageia 5 Mass Rebuild
- Mageia 5 Mass Rebuild
- Mageia 4 Mass Rebuild

* Tue Oct 15 2013 dams <dams> 5.1.1-1.mga4
+ Revision: 500632
- new version 5.1.1

  + fwang <fwang>
    - now based on gtk

* Fri Sep 13 2013 fwang <fwang> 5.1.0-1.mga4
+ Revision: 478289
- new version 5.1.0

* Tue Jun 25 2013 dams <dams> 5.0-2.mga4
+ Revision: 446651
- Finally disable debug as it's an empty rpm...
- Try to make specfile better...
- Add 'pea' and 'pealauncher'
- Enable debug package

* Tue Jun 25 2013 dams <dams> 5.0-1.mga4
+ Revision: 446620
- new version 5.0

* Tue Jun 25 2013 dams <dams> 4.9.2-1.mga4
+ Revision: 446606
- fix icons installation
- clean specfile
- improve icon rendering by providing a better icon size

