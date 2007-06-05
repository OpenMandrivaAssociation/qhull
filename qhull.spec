%define name	qhull
%define version	2003.1
%define release	%mkrel 3
%define major	0
%define libname	%mklibname %{name} %{major}

Summary:	Computes convex hulls
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		0
License:	GPL
Group:		System/Libraries
Url:		http://www.qhull.org/
Source0:	%{url}files/%{name}-%{version}-src.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
Qhull computes convex hulls, Delaunay triangulations, halfspace
intersections about a point, Voronoi diagrams, furthest-site Delaunay
triangulations, and furthest-site Voronoi diagrams. It runs in 2-d, 3-d,
4-d, and higher dimensions. It implements the Quickhull algorithm for
computing the convex hull. Qhull handles roundoff errors from floating
point arithmetic. It can approximate a convex hull.

%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries
Provides:	lib%{name} = %{epoch}:%{version}-%{release}

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

%package -n %{libname}-devel
Summary:	Header files and static library for development with %{name}
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}

%description -n %{libname}-devel
Header files and static library for development with %{name}.

%prep
%setup -q
%{__perl} -pi -e 's|\r||g' configure.in Makefile.am src/Makefile.am src/Make-config.sh

%build
pushd src
sh ./Make-config.sh || :
touch MBorland Makefile.txt
popd

%{__perl} -pi -e 's|AM_INIT_AUTOMAKE\(qhull, 2002.1\)|AM_INIT_AUTOMAKE(%{name}, %{version})|' configure.in
%{__perl} -pi -e 's|^AC_PROG_LIBTOOL|AM_PROG_LIBTOOL|' configure.in

touch NEWS README AUTHORS ChangeLog
autoreconf --verbose --force --install

%configure
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__rm} -rf %{buildroot}/usr/share/doc

%{__perl} -pi -e 's|\r||g' *.txt html/*.{1,htm,man,txt}

%clean
%{__rm} -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-, root, root)
%doc Announce.txt COPYING.txt README.txt REGISTER.txt
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%doc html
%{_bindir}/*
%{_mandir}/*/*
%{_libdir}/*.so
%{_libdir}/*.*a
%{_includedir}/*
