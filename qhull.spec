%define qhull_major		%(echo %{version} |cut -d. -f2)
%define libqhull		%mklibname %{name}
%define oldlibqhull		%mklibname %{name} 8
%define libqhull_devel		%mklibname %{name} -d
%define libqhull_static_devel	%mklibname %{name} -d -s

%bcond_without	shared_lib
%bcond_without	static_lib

Name:		qhull
Version:	2020.8.0.2
Release:	2
Summary:	Compute convex hulls
License:	GPL
Group:		System/Libraries
URL:		https://www.qhull.org/
Source0:	http://www.qhull.org/download/%{name}-%(echo %{version} |cut -d. -f1)-src-%(echo %{version} |cut -d. -f2-).tgz
Patch0:		qhull-2020-8.0.2-fix_path.patch
Source100:	qhull.rpmlintrc
BuildRequires:	cmake ninja

%description
Qhull computes convex hulls, Delaunay triangulations, halfspace
intersections about a point, Voronoi diagrams, furthest-site Delaunay
triangulations, and furthest-site Voronoi diagrams. It runs in 2-d, 3-d,
4-d, and higher dimensions. It implements the Quickhull algorithm for
computing the convex hull. Qhull handles roundoff errors from floating
point arithmetic. It can approximate a convex hull.

%files
%doc Announce.txt COPYING.txt README.txt REGISTER.txt
%{_bindir}/qconvex*
%{_bindir}/qdelaunay*
%{_bindir}/qhalf*
%{_bindir}/qhull*
%{_bindir}/qvoronoi*
%{_bindir}/rbox*
%{_mandir}/man1/qhull.1*
%{_mandir}/man1/rbox.1*
%exclude %{_docdir}/%{name}

#---------------------------------------------------------------------------

%package -n %{libqhull}
Summary:	Shared libraries for %{name}
Group:		System/Libraries
%rename %{oldlibqhull}

%description -n %{libqhull}
Qhull computes convex hulls, Delaunay triangulations, Voronoi diagrams,
furthest-site Voronoi diagrams, and halfspace intersections about a point.
It runs in 2-d, 3-d, 4-d, or higher. It implements the Quickhull algorithm
for computing convex hulls. Qhull handles round-off errors from floating
point arithmetic. It can approximate a convex hull.

The program includes options for hull volume, facet area, partial hulls,
input transformations, randomization, tracing, multiple output formats, and
execution statistics.

This package provide shared libraries for %{name}.

%files -n %{libqhull}
%{_libdir}/*.so.%{qhull_major}*

#---------------------------------------------------------------------------

%package -n %{libqhull_devel}
Summary:	Header files and libraries for development with %{name}
Group:		Development/C
Requires:	%{libqhull} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Obsoletes:	%{mklibname qhull 0 -d} < %{version}

%description -n %{libqhull_devel}
Header files and libraries for development with %{name}.

%files -n %{libqhull_devel}
%{_libdir}/*.so
%{_includedir}/*
%dir %{_libdir}/cmake/Qhull
%{_libdir}/cmake/Qhull/*.cmake
%{_libdir}/pkgconfig/qhull*.pc
%doc %{_docdir}/%{name}/html

#---------------------------------------------------------------------------

%if %{with static_lib}
%package -n %{libqhull_static_devel}
Summary:	Static library for development with %{name}
Group:		Development/C
Requires:	%{libqhull_devel} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}
Provides:	lib%{name}-static-devel = %{EVRD}
Obsoletes:	%{mklibname qhull 0 -d -s} < %{version}

%description -n %{libqhull_static_devel}
Header files and static library for development with %{name}.

%files -n %{libqhull_static_devel}
%{_libdir}/*.a
%endif

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%(echo %{version} |cut -d. -f1).%(echo %{version} |cut -d. -f4)

%build
%cmake \
	-DBUILD_SHARED_LIBS:BOOL=%{?with_shared_lib:ON}%{?!with_shared_lib:OFF} \
	-DBUILD_STATIC_LIBS:BOOL=%{?with_static_lib:ON}%{?!with_static_lib:OFF} \
	-GNinja
%ninja_build

%install
%ninja_install -C build

