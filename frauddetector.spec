#
# Conditional build:
%bcond_without	tests		# don't build and run tests

%define		svnrev	86
%define		rel		0.1
Summary:	Log analyzer with based on GeoIP distance
Name:		frauddetector
Version:	0.1
Release:	0.%{svnrev}.%{rel}
License:	Apache v2.0
Group:		Development/Languages/Java
# revno=
# svn co http://frauddetector.googlecode.com/svn/trunk${revno:+@$revno} frauddetector
# tar -cjf frauddetector-$(svnversion frauddetector).tar.bz2 --exclude-vcs --exclude=GeoLiteCity.dat frauddetector
# ../dropin frauddetector-$(svnversion frauddetector).tar.bz2
Source0:	%{name}-%{svnrev}.tar.bz2
# Source0-md5:	bc29a6add663ae977fde560175ccf306
URL:		http://courses.cs.ut.ee/2009/security-seminar/
%{?with_tests:BuildRequires:	GeoIP-db-City}
BuildRequires:	ant
BuildRequires:	jdk
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	sed >= 4.0
Requires:	GeoIP-db-City
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}

%description
Frauddetector is log analyzer which can detect leaked passwords from
log files if same username distance in GeoIP is far away.

%prep
%setup -q -n %{name}

mv conf.sample.properties conf.properties
%undos conf.properties
sed -i -e '
	s,=geoIP/GeoLiteCity.dat,=%{_datadir}/GeoIP/GeoLiteCity.dat,
	s,=formats.xml,=%{_appdir}/formats.xml,
' conf.properties

cat <<'EOF' > %{name}.sh
#!/bin/sh
# Usage:
# $0 [config.properties]
exec java -jar %{_javadir}/%{name}.jar "$@"
EOF

%build
%ant

%if %{with tests}
ln -snf %{_datadir}/GeoIP/GeoLiteCity.dat geoIP
%java -jar %{name}.jar test/conf.properties
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_javadir},%{_appdir}}
cp -a frauddetector.jar $RPM_BUILD_ROOT%{_javadir}
cp -a formats.xml $RPM_BUILD_ROOT%{_appdir}
install -p %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc conf.properties
%attr(755,root,root) %{_bindir}/frauddetector
%{_javadir}/%{name}.jar
%{_appdir}
