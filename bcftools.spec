Name:		bcftools
Version:	1.9
Release:	1%{?dist}
Summary:	Tools for genomic variant calling and manipulating VCF/BCF files

# The bcftools source code is MIT-licensed, but the executable becomes
# GPL-licensed when --enable-libgsl is used.
License:	GPLv3+
URL:		http://www.htslib.org/
Source0:	https://github.com/samtools/bcftools/releases/download/%{version}/bcftools-%{version}.tar.bz2
Patch0:		bcftools-1.9-python3.patch
Patch1:		bcftools-1.9-configure.patch

BuildRequires:	gcc
BuildRequires:	gsl-devel
BuildRequires:	htslib-devel
BuildRequires:	htslib-tools
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::Embed)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	zlib-devel

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

sed -i '1s,/usr/bin/env perl,/usr/bin/perl,' misc/*.pl misc/plot-vcfstats
sed -i '1s,/usr/bin/env python,%{__python3},' misc/*.py


%build
%configure CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}" \
  --prefix=%{_prefix} \
  --with-htslib=system --enable-perl-filters --enable-libgsl \
  --with-bcf-plugin-path='%{_usr}/local/libexec/bcftools:$(plugindir)'
%make_build


%install
%make_install


%check
make test


%files
%doc AUTHORS NEWS
%license LICENSE
%{_bindir}/*
%{_libexecdir}/bcftools
%{_mandir}/man1/bcftools.1*


%changelog
* Wed Nov 06 2019 John Marshall <jmarshall@users.sourceforge.net> - 1.9-1
- New spec file for bcftools, now separate from samtools (#1767792).
- Backported Python 3 and configure patches from later upstream development.
