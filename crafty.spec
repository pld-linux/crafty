# TODO: optflags, disable x86 assembly on !x86 (if possible)
Summary:	Superior chess program by Bob Hyatt for Unix systems
Summary(pl):	Jeden z lepszych programów szachowych dla uniksów autorstwa Boba Hyatta
Name:		crafty
Version:	18.9
Release:	2
License:	GPL
Group:		Applications/Games
Source0:	ftp://ftp.cis.uab.edu/pub/hyatt/v18/%{name}-%{version}.tar.gz
# Source0-md5:	4cae4e95fb86421c6626baefadbff18f
Source1:	ftp://ftp.cis.uab.edu/pub/hyatt/%{name}.faq
# NoSource1-md5: f744727e291b6dec7e7c69bb3586b6dd
Source2:	ftp://ftp.cis.uab.edu/pub/hyatt/read.me
# NoSource2-md5: ce9a5e014d23f36c2540628ba0dc1c0b
Source3:	ftp://ftp.cis.uab.edu/pub/hyatt/common/start.pgn.gz
# Source3-md5:	c3c54b29351408298e3c7548f4faed93
Source4:	ftp://ftp.cis.uab.edu/pub/hyatt/v18/%{name}.doc.ascii
# NoSource4-md5: 5fd73027a1de1674763562e1987197ba
Source5:	ftp://ftp.cis.uab.edu/pub/hyatt/doc/%{name}.doc.ps
# Source5-md5:	6cef69aa2f9ea1ceb74b6c14edc8291f
Patch0:		%{name}-paths.patch
Patch1:		%{name}-Makefile.patch
Icon:		xchess.gif
Provides:	chessprogram
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Crafty is a Unix chess program, distributed as source by its author,
Bob Hyatt. The program plays at about 2200 strength and frequently
beats GNU Chess on the same hardware.

%description -l pl
Crafty to uniksowy program szachowy rozpowszechniany w postaci
¼ród³owej przez autora - Boba Hyatta. Program gra z si³± oko³o 2200 i
czêsto wygrywa z GNU Chess na tym samym sprzêcie.

%prep
%setup -q -c
%patch0 -p0
%patch1 -p0
cd %{name}-%{version}
cp %{SOURCE2} README
cp %{SOURCE1} .
cp %{SOURCE4} %{SOURCE5} .
cp %{SOURCE3} . 
gzip -d start.pgn.gz

%build
cd %{name}-%{version}
%{__make} linux-elf
#mkdir -p %{_prefix}/lib/games/crafty
#touch %{_prefix}/lib/games/crafty/book.lrn %{_prefix}/lib/games/crafty/position.{bin,lrn}
#./crafty << _END_
#books create start.pgn 60
#quit
#_END_

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}-%{version}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/games/crafty}
install crafty $RPM_BUILD_ROOT%{_bindir}
#install books.bin $RPM_BUILD_ROOT%{_libdir}/games/crafty
#install -d %{_libdir}/games/crafty
#install books.bin %{_libdir}/games/crafty/books.bin

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /usr/lib/games/crafty/book.lrn /usr/lib/games/crafty/position.{bin,lrn}
chgrp games /usr/lib/games/crafty/book.lrn \
	/usr/lib/games/crafty/position.{bin,lrn}
chmod g+w /usr/lib/games/crafty/book.lrn \
        /usr/lib/games/crafty/position.{bin,lrn}

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}/{crafty.faq,crafty.doc.ascii,crafty.doc.ps,README}
%attr(755,root,root) %{_bindir}/crafty
%dir %{_libdir}/games/crafty
#%{_libdir}/games/crafty/books.bin
