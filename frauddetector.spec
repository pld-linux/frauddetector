%define		svnrev	79
%define		rel		0.1
%include	/usr/lib/rpm/macros.java
Summary:	Log analyzer with based on GeoIP distance
Name:		frauddetector
Version:	0.1
Release:	0.%{svnrev}.%{rel}
License:	Apache v2.0
Group:		Development/Languages/Java
# revno=
# svn co http://frauddetector.googlecode.com/svn/trunk${revno:+@$revno} frauddetector
# tar -cjf frauddetector-$(svnversion frauddetector).tar.bz2 --exclude=.svn frauddetector
# ../dropin frauddetector-$(svnversion frauddetector).tar.bz2
Source0:	%{name}-%{svnrev}.tar.bz2
# Source0-md5:	0bc4165092deacb904a66b381dc9f8c0
URL:		http://courses.cs.ut.ee/2009/security-seminar/
BuildRequires:	ant
BuildRequires:	jdk
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Frauddetector is log analyzer which can detect leaked passwords from
log files if same username distance in GeoIP is far away.

%prep
%setup -q -n %{name}

%build
%ant

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_bindir}/dbus
