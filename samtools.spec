Name:		samtools
Version:	0.1.7a
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


%prep
%setup -q


%build
make CFLAGS="%{optflags}" samtools razip %{?_smp_mflags}

cd misc/
make CFLAGS="%{optflags}" %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -p samtools razip %{buildroot}%{_bindir}

gzip samtools.1
mkdir -p %{buildroot}%{_mandir}/man1/
cp -p samtools.1.gz %{buildroot}%{_mandir}/man1/

cd misc/
install -p blast2sam.pl bowtie2sam.pl export2sam.pl interpolate_sam.pl	\
    maq2sam-long maq2sam-short md5fa md5sum-lite novo2sam.pl sam2vcf.pl	\
    samtools.pl soap2sam.pl wgsim wgsim_eval.pl zoom2sam.pl		\
    %{buildroot}%{_bindir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS examples/ samtools.txt
%{_bindir}/*
%{_mandir}/man1/*


%changelog
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
