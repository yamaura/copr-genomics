Name: bcftools
Version: 1.9
Release: 6%{?dist}
Summary: Tools for genomic variant calling and manipulating VCF/BCF files

# This software is available under a choice of one of two licenses,
# the MIT/Expat (MIT) or the GNU General Public License Version 3 (GPLv3+).
# And if compiled with the GNU Scientific Library, in this case it is built
# with --enable-libgsl, the use of this software is governed by the GPLv3+
# license.
# See <https://github.com/samtools/bcftools/blob/develop/LICENSE>.
License: GPLv3+
# https:// is better than http://.
URL: https://www.htslib.org/
Source0: https://github.com/samtools/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
Patch0: bcftools-1.9-python3.patch
Patch1: bcftools-1.9-configure.patch

BuildRequires: gcc
BuildRequires: gsl-devel
BuildRequires: htslib-devel
BuildRequires: htslib-tools
BuildRequires: perl-interpreter
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: perl(File::Temp)
BuildRequires: perl(FindBin)
BuildRequires: perl(Getopt::Long)
BuildRequires: zlib-devel
BuildRequires: make
# bcftools had been included in samtools version 0.X.
# https://github.com/samtools/samtools/commit/e7ae7f96c7e78a2dd6eabdaed57037c483951929
Conflicts: samtools < 1.0
# A big-endian (s390x) environment is not supported.
# https://github.com/samtools/htslib/issues/355
ExcludeArch: s390x

%description
BCFtools is a set of utilities that manipulate genomic variant calls in the
Variant Call Format (VCF) and its binary counterpart (BCF). All commands work
transparently with both VCFs and BCFs, both uncompressed and BGZF-compressed.

(This BCFtools includes the polysomy subcommand, which is implemented using
the GNU Scientific Library. Hence this package is licensed according to the
GNU General Public License, rather than the MIT license used when BCFtools
is built without the polysomy subcommand.)


%prep
%setup -q
%patch0 -p1 -b .py3
%patch1 -p1 -b .conf

sed -i '1s|/usr/bin/env perl|/usr/bin/perl|' misc/*.pl misc/plot-vcfstats
sed -i '1s|/usr/bin/env python|%{__python3}|' misc/*.py


%build
%configure CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}" \
  --prefix=%{_prefix} \
  --with-htslib=system \
  --enable-perl-filters \
  --enable-libgsl \
  --with-bcf-plugin-path='%{_usr}/local/libexec/bcftools:$(plugindir)'
%make_build


%install
%make_install


%check
# Check if bcftools is built with system htslib.
ldd bcftools | grep -E '/lib(64)?/libhts\.so\.'

make test


%files
%doc AUTHORS NEWS
%license LICENSE
# We do not use a wildcard to list bin files, because this often leads
# to problems when the name changes or something additional is installed.
%{_bindir}/bcftools
%{_bindir}/color-chrs.pl
%{_bindir}/guess-ploidy.py
%{_bindir}/plot-roh.py
%{_bindir}/plot-vcfstats
%{_bindir}/run-roh.pl
%{_bindir}/vcfutils.pl
%{_libexecdir}/bcftools
%{_mandir}/man1/bcftools.1*


%changelog
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.9-4
- Perl 5.32 rebuild

* Tue Mar 17 2020 Jun Aruga <jaruga@redhat.com> - 1.9-3
- Fix the build failure adding perl(FindBin) build dependency.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 19 2019 Jun Aruga <jaruga@redhat.com> - 1.9-1
- Exclude a CPU architecture s390x.
- Add Conflicts tag for samtools < 1.0.
- Align the field delimiter as 1 space.
- Use additional RPM macros for Source0.
- Add a logic to check if bcftools is built with system htslib.
- Update comments for license.

* Wed Nov 06 2019 John Marshall <jmarshall@users.sourceforge.net> - 1.9-1
- New spec file for bcftools, now separate from samtools (#1767792).
- Backported Python 3 and configure patches from later upstream development.
