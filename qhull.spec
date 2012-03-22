%define qhull_major		6
%define libqhull		%mklibname %{name} %{qhull_major}
%define libqhull_devel		%mklibname %{name} -d
%define libqhull_static_devel	%mklibname %{name} -d -s

Name:		qhull
Version:	2012.1
Release:	3
Summary:	Compute convex hulls
License:	GPL
Group:		System/Libraries
URL:		http://www.qhull.org/
Source0:	http://www.qhull.org/files/%{name}-%{version}-src.tgz
BuildRequires:	cmake
Patch0:		qhull-2012.1-format.patch

%description
Qhull computes convex hulls, Delaunay triangulations, halfspace
intersections about a point, Voronoi diagrams, furthest-site Delaunay
triangulations, and furthest-site Voronoi diagrams. It runs in 2-d, 3-d,
4-d, and higher dimensions. It implements the Quickhull algorithm for
computing the convex hull. Qhull handles roundoff errors from floating
point arithmetic. It can approximate a convex hull.

%package	-n %{libqhull}
Summary:	Shared libraries for %{name}
Group:		System/Libraries

%description	-n %{libqhull}
Qhull computes convex hulls, Delaunay triangulations, Voronoi diagrams,
furthest-site Voronoi diagrams, and halfspace intersections about a point.
It runs in 2-d, 3-d, 4-d, or higher.  It implements the Quickhull algorithm
for computing convex hulls.  Qhull handles round-off errors from floating
point arithmetic.  It can approximate a convex hull.

The program includes options for hull volume, facet area, partial hulls,
input transformations, randomization, tracing, multiple output formats, and
execution statistics.

This package provide shared libraries for %{name}.

%package	-n %{libqhull_devel}
Summary:	Header files and libraries for development with %{name}
Group:		Development/C
Requires:	%{libqhull} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Obsoletes:	%{mklibname qhull 0 -d}

%pretrans	-n %{libqhull_devel}
    if [ -d %{_includedir}/qhull ]; then
	mv %{_includedir}/qhull %{_includedir}/qhull.rpmsave
	ln -s %{_includedir}/qhull.rpmsave %{name}
    fi

%description	-n %{libqhull_devel}
Header files and libraries for development with %{name}.

%package	-n %{libqhull_static_devel}
Summary:	Static library for development with %{name}
Group:		Development/C
Requires:	%{libqhull_devel} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}
Provides:	lib%{name}-static-devel = %{EVRD}
Obsoletes:	%{mklibname qhull 0 -d -s}

%description	-n %{libqhull_static_devel}
Header files and static library for development with %{name}.

%prep
%setup -q
%patch0 -p1

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
pushd build
    cmake							\
	-DCMAKE_INSTALL_PREFIX:PATH=%{buildroot}%{_prefix}	\
	-DLIB_INSTALL_DIR:PATH=%{buildroot}%{_libdir}		\
	-DMAN_INSTALL_DIR:PATH=%{buildroot}%{_mandir}/man1	\
	-DDOC_INSTALL_DIR:PATH=%{buildroot}%{_docdir}/%{name}	\
	 ..
    %make
popd

%install
make -C build install
mkdir -p %{buildroot}%{_docdir}/%{name}
cp -fpa html %{buildroot}%{_docdir}/%{name}

# add some symlinks to satisfy octave configure
ln -sf libqhull %{buildroot}%{_includedir}/qhull
ln -sf libqhull.h %{buildroot}%{_includedir}/qhull/qhull.h

%files
%doc Announce.txt COPYING.txt README.txt REGISTER.txt
%{_bindir}/qconvex*
%{_bindir}/qdelaunay*
%{_bindir}/qhalf*
%{_bindir}/qhull*
%{_bindir}/qvoronoi*
%{_bindir}/rbox*
%{_bindir}/testqset*
%{_bindir}/user_eg*
%{_mandir}/man1/qhull.1*
%{_mandir}/man1/rbox.1*
%exclude %{_docdir}/%{name}/html

%files		-n %{libqhull}
%{_libdir}/*.so.%{qhull_major}*

%files		-n %{libqhull_devel}
%{_libdir}/*.so
%{_includedir}/*
%doc %{_docdir}/%{name}/html

%files		-n %{libqhull_static_devel}
%{_libdir}/*.a
