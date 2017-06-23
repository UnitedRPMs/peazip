%define debug_package %{nil}
%global _iconsdir %{_datadir}/icons

Summary:	File and archive manager
Name:		peazip
Version:	6.4.1
Release:	1%{?dist}
License:	LGPLv3
Group:          Applications/Archiving
Url:		http://www.peazip.org/peazip-linux.html
Source0:	http://download.sourceforge.net/%{name}/%{name}-%{version}.src.zip
# configure to run in users home appdata
Source1:	altconf.txt
Source2:	%{name}.desktop
BuildRequires:	dos2unix
BuildRequires:	lazarus >= 1.2.0
BuildRequires:	qt4pas-devel
BuildRequires:	qt-devel
BuildRequires:	qtwebkit-devel
BuildRequires:	icoutils
BuildRequires:	desktop-file-utils
Requires:	p7zip
Requires:	upx >= 3.09
Requires:	desktop-file-utils
Recommends:	unrar
Recommends:	unace

%description
PeaZip is a free cross-platform file archiver that provides a unified
portable GUI for many Open Source technologies like 7-Zip, FreeArc, PAQ,
UPX...

%prep
%setup -q -n %{name}-%{version}.src
chmod +w res/lang
dos2unix readme*

%build
lazbuild --lazarusdir=%{_libdir}/lazarus \
%ifarch x86_64
	--cpu=x86_64 \
%endif
	--widgetset=qt \
	-B project_peach.lpi project_pea.lpi project_gwrap.lpi

%install
install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_datadir}/%{name}
rm -rf res/icons
cp -r res %{buildroot}%{_datadir}/%{name}
cp %{S:1} %{buildroot}%{_datadir}/%{name}/res

#install helper apps
install -d -m755 %{buildroot}%{_datadir}/%{name}/res/{7z,upx}
ln -s %{_bindir}/7z  %{buildroot}%{_datadir}/%{name}/res/7z
ln -s %{_bindir}/upx  %{buildroot}%{_datadir}/%{name}/res/upx

install pea %{buildroot}%{_datadir}/%{name}/res
ln -s %{_datadir}/%{name}/res/pea %{buildroot}%{_bindir}/pea
install %{name} %{buildroot}%{_datadir}/%{name}
ln -s %{_datadir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}
install pealauncher %{buildroot}%{_datadir}/%{name}/res
ln -s %{_datadir}/%{name}/res/pealauncher %{buildroot}%{_bindir}/pealauncher

install -d -m755 %{buildroot}%{_datadir}/applications
install -m 0644 %{S:2} %{buildroot}%{_datadir}/applications/

install -d -m755 %{buildroot}%{_iconsdir}/hicolor/256x256/apps
icotool -x -i 1 -o %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png %{name}.ico
rm -rf %{buildroot}%{_datadir}/%{name}/res/icons

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
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}/


%changelog

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

