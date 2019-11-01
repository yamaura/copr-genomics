Name:		samtools
Version:	0.1.19
Release:	20%{?dist}
Summary:	Tools for nucleotide sequence alignments in the SAM format

License:	MIT
URL:		http://samtools.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		samtools-0.1.14-soname.patch
Patch1:		samtools-0.1.19-faidx_fetch_seq2.patch
# The Rsamtools upstream is fixing issues in the samtools 0.1.19 codebase
Patch2:		samtools-0.1.19-R-fixes.patch

BuildRequires:	gcc
BuildRequires:	zlib-devel >= 1.2.3
BuildRequires:	ncurses-devel

%description
SAM (Sequence Alignment/Map) is a flexible generic format for storing
nucleotide sequence alignment.
SAM Tools provide various utilities for manipulating alignments in the
SAM format, including sorting, merging, indexing and generating
alignments in a per-position format.


%package devel
Summary:	Header files and libraries for compiling against %{name}
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files and libraries for compiling against %{name}


%package libs
Summary:	Libraries for applications using %{name}

%description libs
Libraries for applications using %name


%prep
%setup -q
%patch0 -p1 -b .soname
%patch1 -p1 -b .seq2
%patch2 -p1 -b .Rfixes

# Remove misc/varfilter.py script using Python 2,
# as it has not been usable since 2011.
# https://github.com/samtools/samtools/commit/2c1daf5
rm -f misc/varfilter.py

# fix eol encoding
sed -i 's/\r//' misc/export2sam.pl


%build
make CFLAGS="%{optflags}" dylib %{?_smp_mflags}
make CFLAGS="%{optflags} -fPIC" samtools razip %{?_smp_mflags}

cd misc/
make CFLAGS="%{optflags} -fPIC" %{?_smp_mflags}

cd ../bcftools
make CFLAGS="%{optflags} -fPIC" %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -p samtools razip %{buildroot}%{_bindir}

# header and library files
mkdir -p %{buildroot}%{_includedir}/%{name}
install -p -m 644 *.h %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_libdir}
strip libbam.so.1
install -p -m 755 libbam.so.1 %{buildroot}%{_libdir}
ln -sf libbam.so.1 %{buildroot}%{_libdir}/libbam.so

mkdir -p %{buildroot}%{_mandir}/man1/
cp -p samtools.1 %{buildroot}%{_mandir}/man1/
#cp -p bcftools/bcftools.1 %%{buildroot}%%{_mandir}/man1/

cd misc/
install -p blast2sam.pl bowtie2sam.pl export2sam.pl interpolate_sam.pl	\
    maq2sam-long maq2sam-short md5fa md5sum-lite novo2sam.pl psl2sam.pl	\
    sam2vcf.pl samtools.pl soap2sam.pl wgsim wgsim_eval.pl	\
    zoom2sam.pl  	       		    				\
    %{buildroot}%{_bindir}

cd ../bcftools/
install -p bcftools vcfutils.pl %{buildroot}%{_bindir}
mv README README.bcftools



%ldconfig_scriptlets libs


%files
%doc AUTHORS ChangeLog.old COPYING INSTALL NEWS examples/ bcftools/README.bcftools bcftools/bcf.tex
%{_bindir}/*
%{_mandir}/man1/*


%files	devel
%{_includedir}/%{name}
%{_libdir}/libbam.so


%files libs
%{_libdir}/libbam.so.*


%changelog
* Fri Nov 01 2019 Jun Aruga <jaruga@redhat.com> - 0.1.19-20
- Remove Python 2 dependency (rhbz#1738176).

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Petr Pisar <ppisar@redhat.com> - 0.1.19-18
- varfilter.py is a Python 2 code (bug #1675976)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 25 2018 Adam Huffman <bloch@verdurin.com> - 0.1.19-16
- Add BR for python2

* Fri Jul 20 2018 Adam Huffman <bloch@verdurin.com> - 0.1.19-15
- Add BR for gcc

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Tom Callaway <spot@fedoraproject.org> - 0.1.19-7
- add fixes from Rsamtools

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun  9 2014 Tom Callaway <spot@fedoraproject.org> - 0.1.19-5
- add faidx_fetch_seq2 function from rsamtools

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.1.19-2
- Perl 5.18 rebuild

* Thu Apr 11 2013 Tom Callaway <spot@fedoraproject.org> - 0.1.19-1
- update to 0.1.19

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Adam Huffman <verdurin@fedoraproject.org> - 0.1.18-2
- make sure new seqtk tool included

* Tue Sep  6 2011 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.18-1
- Updated to 0.1.18

* Tue May 10 2011 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.16-1
- Updated to 0.1.16

* Mon Apr 11 2011 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.15-1
- Updated to 0.1.15

* Wed Mar 23 2011 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.14-1
- Updated to 0.1.14
- Build shared library instead of static

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.12a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec  6 2010 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.12a-2
- Fixed header files directory ownership
- Added missing header files

* Mon Dec  6 2010 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.12a-1
- Updated to 0.1.12a

* Tue Nov 23 2010 Adam Huffman <bloch@verdurin.com> - 0.1.8-4
- cleanup man page handling

* Sun Oct 10 2010 Adam Huffman <bloch@verdurin.com> - 0.1.8-4
- fix attributes for devel subpackage
- fix library location

* Sun Sep 26 2010 Adam Huffman <bloch@verdurin.com> - 0.1.8-3
- put headers and library in standard locations

* Mon Sep 6 2010 Adam Huffman <bloch@verdurin.com> - 0.1.8-2
- merge Rasmus' latest changes (0.1.8 update)
- include bam.h and libbam.a for Bio-SamTools compilation
- move bam.h and libbam.a to single directory
- put bgzf.h, khash.h and faidx.h in the same place
- add -fPIC to CFLAGS to make Bio-SamTools happy
- add virtual Provide as per guidelines

* Tue Aug 17 2010 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.8-1
- Updated to 0.1.8.

* Mon Nov 30 2009 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.7a-1
- Updated to 0.1.7a.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5c-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.5c-3
- Specfile cleanup.

* Sat Jul 11 2009 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.5c-2
- Fixed manpage location.
- Make sure optflags is passed to the makefiles.

* Sat Jul 11 2009 Rasmus Ory Nielsen <ron@ron.dk> - 0.1.5c-1
- Initial build.
