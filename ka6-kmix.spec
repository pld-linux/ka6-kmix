#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kmix
Summary:	kmix
Name:		ka6-%{kaname}
Version:	25.04.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications/Games
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	327d6e597c189103391f89e77e9861ef
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kglobalaccel-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kf6-solid-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KMix is an application to allow you to change the volume of your sound
card. Though small, it is full-featured, and it supports several
platforms and sound drivers.

%description -l pl.UTF-8
KMix jest aplikacją pozwalającą Ci zmienić głośność Twojej karty
dźwiękowej. Choć mały, jest pełen możliwości, obsługuje wiele platform
i sterowników dźwięku.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{lt,sr}
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun


%files -f %{kaname}.lang
%defattr(644,root,root,755)
/etc/xdg/autostart/kmix_autostart.desktop
/etc/xdg/autostart/restore_kmix_volumes.desktop
%attr(755,root,root) %{_bindir}/kmix
%attr(755,root,root) %{_bindir}/kmixctrl
%attr(755,root,root) %{_bindir}/kmixremote
%attr(755,root,root) %{_libdir}/libkmixcore.so.*.*.*
%ghost %{_libdir}/libkmixcore.so.6
%{_desktopdir}/org.kde.kmix.desktop
%{_datadir}/config.kcfg/kmixsettings.kcfg
%{_datadir}/dbus-1/interfaces/org.kde.kmix.control.xml
%{_datadir}/dbus-1/interfaces/org.kde.kmix.mixer.xml
%{_datadir}/dbus-1/interfaces/org.kde.kmix.mixset.xml
%{_iconsdir}/hicolor/*x*/actions/kmix.png
%{_datadir}/kmix
%{_datadir}/knotifications6/kmix.notifyrc
%{_datadir}/kxmlgui5/kmix
%{_datadir}/metainfo/org.kde.kmix.appdata.xml
%{_datadir}/qlogging-categories6/kmix.categories
