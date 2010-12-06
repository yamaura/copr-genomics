Name:		samtools
Version:	0.1.12a
Release:	1%{?dist}
Summary:	Tools for nucleotide sequence alignments in the SAM format

Group:		Applications/Engineering
License:	MIT
URL:		http://samtools.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	zlib-devel >= 1.2.3
BuildRequires:	ncurses-devel

%description
SAM (Sequence Alignment/Map) is a flexible generic format for storing
nucleotide sequence alignment. SAM tools provide efficient utilities on
manipulating alignments in the SAM format.

%package devel
Summary: Header files and libraries for compiling against %{name}
Group:	 Development/System
Requires: %name = %version-%release
Provides: samtools-static = %{version}-%{release}

%description	devel
Header files and libraries for compiling against %{name}

%prep
%setup -q

# fix wrong interpreter
perl -pi -e "s[/software/bin/python][%{__python}]" misc/varfilter.py


%build
make CFLAGS="%{optflags} -fPIC" samtools razip %{?_smp_mflags}

cd misc/
make CFLAGS="%{optflags} -fPIC" %{?_smp_mflags}

cd ../bcftools
make CFLAGS="%{optflags} -fPIC" %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -p samtools razip %{buildroot}%{_bindir}

#header and library for Bio-SamTools
mkdir -p %{buildroot}%{_includedir}/%{name}
install -p -m 644 bam.h bgzf.h khash.h faidx.h %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_libdir}
install -p -m 644 libbam.a %{buildroot}%{_libdir}

mkdir -p %{buildroot}%{_mandir}/man1/
cp -p samtools.1 %{buildroot}%{_mandir}/man1/
cp -p bcftools/bcftools.1 %{buildroot}%{_mandir}/man1/

cd misc/
install -p blast2sam.pl bowtie2sam.pl export2sam.pl interpolate_sam.pl	\
    maq2sam-long maq2sam-short md5fa md5sum-lite novo2sam.pl psl2sam.pl	\
    sam2vcf.pl samtools.pl soap2sam.pl varfilter.py wgsim wgsim_eval.pl	\
    zoom2sam.pl								\
    %{buildroot}%{_bindir}

cd ../bcftools/
install -p bcf-fix.pl bcftools vcfutils.pl %{buildroot}%{_bindir}
mv README README.bcftools


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS examples/ samtools.txt bcftools/README.bcftools
%{_bindir}/*
%{_mandir}/man1/*


%files	devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/bam.h
%{_includedir}/%{name}/bgzf.h
%{_includedir}/%{name}/khash.h
%{_includedir}/%{name}/faidx.h
%{_libdir}/libbam.a


%changelog
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
