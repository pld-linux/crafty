# TODO:
# - executable should be sgid games?
Summary:	Superior chess program by Bob Hyatt for Unix systems
Summary(pl.UTF-8):	Jeden z lepszych programów szachowych dla uniksów autorstwa Boba Hyatta
Name:		crafty
Version:	25.2
Release:	1
License:	Personal use only (see COPYRIGHT)
Group:		Applications/Games
Source0:	http://www.craftychess.com/downloads/source/%{name}-%{version}.zip
# Source0-md5:	d8ad87d9b0fc39a437595203d7b302fc
Source1:	http://www.craftychess.com/documentation/craftydoc.html
# Source1-md5:	584ef65843016328d67a7c9df4007e87
Source2:	http://www.craftychess.com/downloads/book/book.pgn.gz
# Source2-md5:	05efad71289b2d328da5110df4a19f85
Source3:	http://www.craftychess.com/downloads/book/start.pgn.gz
# Source3-md5:	880279c223dc34164837a351faafe2f0
Source4:	http://www.craftychess.com/downloads/book/startc.pgn.gz
# Source4-md5:	7a53d5f09d2baa5e7f0df4ee81961cfb
Source5:	%{name}-misc.tar.bz2
# Source5-md5:	28072241d4978a532ac3ef536b02557c
Source6:	%{name}-bitmaps.tar.gz
# Source6-md5:	e3e94a914f02dfe8b237b1de7376749e
Source7:	%{name}.desktop
Source8:	xchess.png
Patch0:		%{name}-paths.patch
Patch1:		%{name}-security.patch
Patch2:		%{name}-portable.patch
Patch3:		%{name}-spelling.patch
Patch4:		x32.patch
URL:		http://www.craftychess.com/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
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
%setup -q -c -a5 -a6
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p1
%{__mv} doc/read.me README
%{__mv} doc/* .
%{__mv} bitmaps/README.bitmaps .
%{__rm} bitmaps/gifs.tar
cp -p %{SOURCE1} .
zcat %{SOURCE2} > book.pgn
zcat %{SOURCE3} > start.pgn
zcat %{SOURCE4} > startc.pgn

%{__sed} -ne '/Crafty, copyright/,/ as stated previously/ p' main.c > COPYRIGHT
%{__sed} -ne '/version  description/,/^\*\*\*/ p; /^ \*\// q' main.c > ChangeLog

%build
%{__make} crafty-make \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -Wall -pipe -D_REENTRANT" \
	LDFLAGS="%{rpmldflags} -pthread" \
	opt="-DCPUS=4 -DSYZYGY" \
	target=UNIX

sh make_books

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man6,%{_desktopdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT{%{_datadir}/%{name}/{bitmaps,sound,tb},/var/lib/%{name}}

install crafty $RPM_BUILD_ROOT%{_bindir}
install xcrafty $RPM_BUILD_ROOT%{_bindir}
install speak $RPM_BUILD_ROOT%{_bindir}/crafty-speak

cp -p book.bin bookc.bin books.bin crafty.hlp $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p bitmaps/* $RPM_BUILD_ROOT%{_datadir}/%{name}/bitmaps
cp -p tb/*.emd $RPM_BUILD_ROOT%{_datadir}/%{name}/tb

cp -p crafty.6 $RPM_BUILD_ROOT%{_mandir}/man6
echo ".so crafty.6" > $RPM_BUILD_ROOT%{_mandir}/man6/xcrafty.6

cp -p %{SOURCE7} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE8} $RPM_BUILD_ROOT%{_pixmapsdir}

touch $RPM_BUILD_ROOT/var/lib/%{name}/book.lrn \
	$RPM_BUILD_ROOT/var/lib/%{name}/position.{bin,lrn}

for file in book.lrn position.{bin,lrn}; do
	ln -s /var/lib/%{name}/$file $RPM_BUILD_ROOT%{_datadir}/%{name}/$file
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog README* crafty.doc crafty.faq craftydoc.html tournament.howto
%attr(755,root,root) %{_bindir}/crafty
%attr(755,root,root) %{_bindir}/crafty-speak
%attr(755,root,root) %{_bindir}/xcrafty
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.bin
%{_datadir}/%{name}/*.hlp
%{_datadir}/%{name}/*.lrn
%dir %{_datadir}/%{name}/bitmaps
%{_datadir}/%{name}/bitmaps/*.bm
%{_datadir}/%{name}/bitmaps/*.gif
%dir %{_datadir}/%{name}/tb
%{_datadir}/%{name}/tb/*.emd
%dir /var/lib/%{name}
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/book.lrn
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/position.bin
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/position.lrn
%{_mandir}/man6/crafty.6*
%{_mandir}/man6/xcrafty.6*
%{_desktopdir}/crafty.desktop
%{_pixmapsdir}/xchess.png
