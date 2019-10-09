# The value of Makefile LIBHTS_SOVERSION.
%global so_version 2

Name:           htslib
Version:        1.9
Release:        1%{?dist}
Summary:        C library for high-throughput sequencing data formats

# The entire source code is MIT/Expat except cram/ which is Modified-BSD.
# But as there is no "Expat" license in short name list, set "MIT".
# Expat license is same with MIT license.
# https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/thread/C5AHVIW3F6LF5CYLR2PSHNANFYKP327P/
License:        MIT and BSD
URL:            http://www.htslib.org
Source0:        https://github.com/samtools/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

%description
HTSlib is an implementation of a unified C library for accessing common file
formats, such as SAM, CRAM and VCF, used for high-throughput sequencing data,
and is the core library used by samtools and bcftools.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        tools
Summary:        Additional htslib-based tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
Includes the popular tabix indexer, which indexes both .tbi and .csi formats,
the htsfile identifier tool, and the bgzip compression utility.


%prep
%setup -q

%build
%make_build CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"

%install
%make_install prefix=%{_prefix} libdir=%{_libdir}
pushd %{buildroot}/%{_libdir}
chmod 755 libhts.so.%{version}
popd

find %{buildroot} -name '*.la' -delete
rm -f %{buildroot}/%{_libdir}/libhts.a

%ldconfig_scriptlets

%files
%license LICENSE
%doc NEWS
%{_libdir}/libhts.so.%{version}
%{_libdir}/libhts.so.%{so_version}

%files devel
%{_includedir}/htslib
%{_libdir}/libhts.so
%{_libdir}/pkgconfig/htslib.pc
%{_mandir}/man5/faidx.5*
%{_mandir}/man5/sam.5*
%{_mandir}/man5/vcf.5*

%files tools
%{_bindir}/bgzip
%{_bindir}/htsfile
%{_bindir}/tabix
%{_mandir}/man1/bgzip.1*
%{_mandir}/man1/htsfile.1*
%{_mandir}/man1/tabix.1*


%changelog
* Fri Sep 06 2019 Jun Aruga <jaruga@redhat.com> - 1.9-1
- Update for htslib version 1.9

* Thu Jun 2 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.1-4
- Fix changelog
- Add comment RE:bzip2/lzma support

* Sat May 28 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.1-3
- Add LICENSE and NEWS to doc
- Remove unnecessary DESTDIR from call to make_install macro
- Remove explicit Provides

* Thu Apr 28 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.1-1
- Alter permissions of SO to permit strip

* Tue Apr 26 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.1-0
- Update for htslib version 1.3.1

* Tue Apr 12 2016 Sam Nicholls <sam@samnicholls.net> - 1.3.0-0
- Initial version
