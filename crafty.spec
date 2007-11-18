# TODO:
# - update to 21.6
Summary:	Superior chess program by Bob Hyatt for Unix systems
Summary(pl.UTF-8):	Jeden z lepszych programów szachowych dla uniksów autorstwa Boba Hyatta
Name:		crafty
Version:	20.1
Release:	0.2
License:	GPL
Group:		Applications/Games
Source0:	ftp://ftp.cis.uab.edu/pub/hyatt/source/%{name}-%{version}.zip
# Source0-md5:	1d88571c150544c3ed25247127bfc5bd
Source1:	ftp://ftp.cis.uab.edu/pub/hyatt/documentation/%{name}.doc.ascii
# NoSource1-md5:	5fd73027a1de1674763562e1987197ba
Source2:	ftp://ftp.cis.uab.edu/pub/hyatt/documentation/%{name}.doc.ps
# Source2-md5:	6cef69aa2f9ea1ceb74b6c14edc8291f
Source3:	%{name}.desktop
Source4:	xchess.png
Source5:	%{name}-misc.tar.bz2
Source6:	%{name}-bitmaps.tar.gz
Patch0:		%{name}-paths.patch
Patch1:		%{name}-Makefile.patch
Patch2:		%{name}-MDK.patch
URL:		http://www.limunltd.com/crafty/
BuildRequires:	libstdc++-devel
Provides:	chessprogram
Provides:	chess_backend
Suggests:	xboard
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fomit-frame-pointer

%description
Crafty is a Unix chess program, distributed as source by its author,
Bob Hyatt. The program plays at about 2200 strength and frequently
beats GNU Chess on the same hardware.

%description -l pl.UTF-8
Crafty to uniksowy program szachowy rozpowszechniany w postaci
źródłowej przez autora - Boba Hyatta. Program gra z siłą około 2200 i
często wygrywa z GNU Chess na tym samym sprzęcie.

%prep
%setup -q -a5 -a6
%patch0 -p1
%patch1 -p1
%patch2 -p0
mv doc/read.me README
mv doc/* .
mv bitmaps/README.bitmaps .
rm -f bitmaps/gifs.tar
cp %{SOURCE1} %{SOURCE2} .

%{__perl} -pi -e 's@.*machine/builtins.*@@' chess.h

%build
asmobj=""
optarch=""
target="LINUX"
%ifarch %{ix86}
optarch="-DUSE_ASSEMBLY_A -DUSE_ASSEMBLY_B"
asmobj="X86-elf.o"
%endif
%ifarch alpha
target="ALPHA"
%endif
%{__make} crafty-make \
	target="$target" \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -Wall -pipe -D_REENTRANT" \
	LDFLAGS="%{rpmldflags} -lpthread" \
	opt="-DCOMPACT_ATTACKS -DUSE_ATTACK_FUNCTIONS $optarch -DFAST" \
	asm="$asmobj"

sh make_books
# use large opening book
mv large_book.bin book.bin

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man6,%{_desktopdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{bitmaps,sound,tb}

install crafty $RPM_BUILD_ROOT%{_bindir}
install xcrafty $RPM_BUILD_ROOT%{_bindir}
install speak $RPM_BUILD_ROOT%{_bindir}/crafty-speak

install book.bin books.bin crafty.hlp $RPM_BUILD_ROOT%{_datadir}/%{name}
install bitmaps/* $RPM_BUILD_ROOT%{_datadir}/%{name}/bitmaps
install tb/*.emd $RPM_BUILD_ROOT%{_datadir}/%{name}/tb

install crafty.6 $RPM_BUILD_ROOT%{_mandir}/man6
echo ".so crafty.6" > $RPM_BUILD_ROOT%{_mandir}/man6/xcrafty.6

install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_pixmapsdir}

touch $RPM_BUILD_ROOT%{_datadir}/%{name}/book.lrn \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/position.{bin,lrn}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc crafty.doc* crafty.faq README* small.txt start.pgn tournament.howto
%attr(755,root,root) %{_bindir}/crafty*
%attr(755,root,root) %{_bindir}/xcrafty
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.bin
%{_datadir}/%{name}/*.hlp
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) %{_datadir}/%{name}/book.lrn
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) %{_datadir}/%{name}/position.bin
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) %{_datadir}/%{name}/position.lrn
%dir %{_datadir}/%{name}/bitmaps
%{_datadir}/%{name}/bitmaps/*.bm
%{_datadir}/%{name}/bitmaps/*.gif
%dir %{_datadir}/%{name}/tb
%{_datadir}/%{name}/tb/*.emd
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_mandir}/man6/*.6*
