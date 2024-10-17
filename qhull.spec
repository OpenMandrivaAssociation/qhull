%define qhull_major		%(echo %{version} |cut -d. -f2)
%define libqhull		%mklibname %{name} %{qhull_major}
%define libqhull_devel		%mklibname %{name} -d
%define libqhull_static_devel	%mklibname %{name} -d -s

Name:		qhull
Version:	2015.7.2.0
Release:	4
Summary:	Compute convex hulls
License:	GPL
Group:		System/Libraries
URL:		https://www.qhull.org/
Source0:	http://www.qhull.org/download/%{name}-%(echo %{version} |cut -d. -f1)-src-%(echo %{version} |cut -d. -f2-).tgz
Source100:	qhull.rpmlintrc
Patch0:         %{name}-2015.2-html_doc_path.patch
BuildRequires:	cmake

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
Obsoletes:	%{mklibname qhull 0 -d}

%description -n %{libqhull_devel}
Header files and libraries for development with %{name}.

%files -n %{libqhull_devel}
%{_libdir}/*.so
%{_includedir}/*
%doc %{_docdir}/%{name}/html

%pretrans -n %{libqhull_devel}
if [ -d %{_includedir}/qhull ]; then
	mv %{_includedir}/qhull %{_includedir}/qhull.rpmsave
	ln -s %{_includedir}/qhull.rpmsave %{name}
fi

#---------------------------------------------------------------------------

%package -n %{libqhull_static_devel}
Summary:	Static library for development with %{name}
Group:		Development/C
Requires:	%{libqhull_devel} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}
Provides:	lib%{name}-static-devel = %{EVRD}
Obsoletes:	%{mklibname qhull 0 -d -s}

%description -n %{libqhull_static_devel}
Header files and static library for development with %{name}.

%files -n %{libqhull_static_devel}
%{_libdir}/*.a

#---------------------------------------------------------------------------

%prep
%setup -qn %{name}-%(echo %{version} |cut -d. -f1).%(echo %{version} |cut -d. -f3)
%autopatch -p1

%build
%cmake
%make_build

%install
%make_install -C build

# add some symlinks to satisfy octave configure
ln -sf libqhull %{buildroot}%{_includedir}/qhull
ln -sf libqhull.h %{buildroot}%{_includedir}/qhull/qhull.h
