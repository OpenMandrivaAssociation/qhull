%define major        0
%define libname      %mklibname %{name} %{major}
%define libnamedev   %mklibname %{name} %{major} -d
%define libnamesdev  %mklibname %{name} %{major} -d -s

Name:           qhull
Version:        2003.1
Release:        %mkrel 5
Epoch:          0
Summary:        Compute convex hulls
License:        GPL
Group:          System/Libraries
URL:            http://www.qhull.org/
Source0:        http://www.qhull.org/files/%{name}-%{version}-src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Qhull computes convex hulls, Delaunay triangulations, halfspace
intersections about a point, Voronoi diagrams, furthest-site Delaunay
triangulations, and furthest-site Voronoi diagrams. It runs in 2-d, 3-d,
4-d, and higher dimensions. It implements the Quickhull algorithm for
computing the convex hull. Qhull handles roundoff errors from floating
point arithmetic. It can approximate a convex hull.

%package -n %{libname}
Summary:        Shared libraries for %{name}
Group:          System/Libraries

%description -n %{libname}
Qhull computes convex hulls, Delaunay triangulations, Voronoi diagrams,
furthest-site Voronoi diagrams, and halfspace intersections about a point.
It runs in 2-d, 3-d, 4-d, or higher.  It implements the Quickhull algorithm
for computing convex hulls.  Qhull handles round-off errors from floating
point arithmetic.  It can approximate a convex hull.

The program includes options for hull volume, facet area, partial hulls,
input transformations, randomization, tracing, multiple output formats, and
execution statistics.

This package provide shared libraries for %{name}.

%package -n %{libnamedev}
Summary:        Header files and libraries for development with %{name}
Group:          Development/C
Requires:       %{libname} = %{epoch}:%{version}-%{release}
Provides:       %{name}-devel = %{epoch}:%{version}-%{release}
Provides:       lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:       %{_lib}%{name}-devel = %{epoch}:%{version}-%{release}

%description -n %{libnamedev}
Header files and libraries for development with %{name}.

%package -n %{libnamesdev}
Summary:        Static library for development with %{name}
Group:          Development/C
Requires:       %{libnamedev} = %{epoch}:%{version}-%{release}
Provides:       %{name}-static-devel = %{epoch}:%{version}-%{release}
Provides:       lib%{name}-static-devel = %{epoch}:%{version}-%{release}
Provides:       %{_lib}%{name}-static-devel = %{epoch}:%{version}-%{release}

%description -n %{libnamesdev}
Header files and static library for development with %{name}.

%prep
%setup -q
%{__perl} -pi -e 's|\r||g' configure.in Makefile.am src/Makefile.am src/Make-config.sh

%build
pushd src
sh ./Make-config.sh || :
/bin/touch MBorland Makefile.txt
popd

%{__perl} -pi -e 's|AM_INIT_AUTOMAKE\(qhull, 2002.1\)|AM_INIT_AUTOMAKE(%{name}, %{version})|' configure.in
%{__perl} -pi -e 's|^AC_PROG_LIBTOOL|AM_PROG_LIBTOOL|' configure.in

/bin/touch NEWS README AUTHORS ChangeLog
%{_bindir}/autoreconf --verbose --f --i

%{configure2_5x}
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall}
%{__rm} -rf %{buildroot}/usr/share/doc

%{__perl} -pi -e 's|\r$||g' *.txt html/*.{1,htm,man,txt}

%clean
%{__rm} -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc Announce.txt COPYING.txt README.txt REGISTER.txt
%{_bindir}/qconvex
%{_bindir}/qdelaunay
%{_bindir}/qhalf
%{_bindir}/qhull
%{_bindir}/qvoronoi
%{_bindir}/rbox
%{_mandir}/man1/qhull.1*
%{_mandir}/man1/rbox.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc html
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*

%files -n %{libnamesdev}
%defattr(-,root,root)
%{_libdir}/*.a
