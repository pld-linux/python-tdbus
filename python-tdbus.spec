
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (not compatible yet)

%define 	module	tdbus
Summary:	Simple ("trivial") Python bindings for D-BUS
Name:		python-%{module}
Version:	0.9
Release:	0.1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/p/python-tdbus/%{name}-%{version}.tar.gz
# Source0-md5:	5452a6afe95f9a4fc62d94130abd553f
Patch0:		%{name}-cflags.patch
URL:		https://github.com/hmvp/python-tdbus
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	python-gevent
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-gevent
BuildRequires:	python3-modules
%endif
Requires:	python-libs
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python-tdbus is a simple ("trivial") python interface for D-BUS. It
builds directly on top of libdbus and has no other dependencies. Some
benefits of python-tdbus with respect to the standard dbus-python [1]_
Python bindings:

 - The code is extremely simple. Python-tdbus is < 2.000 lines of code
   (C and Python), while dbus-python contains > 15.000 lines of code.
 - Event loop integration is not required for sending and receiving
   signals (if you can afford to block).
 - Includes `gevent' [2]_ event loop integration.
 - Event loop integration can be achieved in Python code rather than in
   C.
 - Uses native Python types for method and signal arguments, driven by
   a simple format string.
 - Provides a more "correct" object model (IMHO) where there's separate
   Dispatcher and Connection objects, instead of putting dispatching
   functionality into the connection object.

%package -n python3-%{module}
Summary:	Simple ("trivial") Python bindings for D-BUS
Group:		Libraries/Python

%description -n python3-%{module}
Python-tdbus is a simple ("trivial") python interface for D-BUS. It
builds directly on top of libdbus and has no other dependencies. Some
benefits of python-tdbus with respect to the standard dbus-python [1]_
Python bindings:

 - The code is extremely simple. Python-tdbus is < 2.000 lines of code
   (C and Python), while dbus-python contains > 15.000 lines of code.
 - Event loop integration is not required for sending and receiving
   signals (if you can afford to block).
 - Includes `gevent' [2]_ event loop integration.
 - Event loop integration can be achieved in Python code rather than in
   C.
 - Uses native Python types for method and signal arguments, driven by
   a simple format string.
 - Provides a more "correct" object model (IMHO) where there's separate
   Dispatcher and Connection objects, instead of putting dispatching
   functionality into the connection object.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q
%patch0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_tdbus.so
%dir %{py_sitedir}/%{module}/test
%{py_sitedir}/%{module}/test/*.py*
%if "%{py_ver}" > "2.4"
%{py_sitedir}/*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/__pycache__
%{py_sitedir}/%{module}/*.py
%attr(755,root,root) %{py_sitedir}/%{module}/_tdbus.so
%dir %{py_sitedir}/%{module}/test
%{py_sitedir}/%{module}/test/*.py
%{py_sitedir}/%{module}/test/__pycache__
%{py3_sitedir}/*.egg-info
%endif
