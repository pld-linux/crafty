Name:		crafty
Version:	18.9
Release:	2
License:	GPL
Group:		Applications/Games
Summary:	Superior chess program by Bob Hyatt for Unix systems.
Icon:		xchess.gif
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
Provides:	chessprogram
ExcludeArch:	axp

%description
Crafty is a Unix chess program, distributed as source by its author,
Bob Hyatt. The program plays at about 2200 strength and frequently
beats GNU Chess on the same hardware.

%prep
%setup -q -c -T -a 0
%patch -p0
cd %{name}-%{version}
cp %{SOURCE2} README
cp %{SOURCE1} .
cp %{SOURCE4} %{SOURCE5} .
cp %{SOURCE3} . 
gzip -d start.pgn.gz

%build
cd %{name}-%{version}
%{__make} linux-elf
mkdir -p %{_prefix}/lib/games/crafty
touch %{_prefix}/lib/games/crafty/book.lrn %{_prefix}/lib/games/crafty/position.{bin,lrn}
./crafty << _END_
books create start.pgn 60
quit
_END_

%install
rm -rf $RPM_BUILD_ROOT
install -d %{_prefix}/lib/games/crafty
install -m 02755 -g games crafty %{_bindir}/crafty
install -m 0644 -g games books.bin %{_prefix}/lib/games/crafty/books.bin

%post
touch /usr/lib/games/crafty/book.lrn /usr/lib/games/crafty/position.{bin,lrn}
chgrp games /usr/lib/games/crafty/book.lrn \
	/usr/lib/games/crafty/position.{bin,lrn}
chmod g+w /usr/lib/games/crafty/book.lrn \
        /usr/lib/games/crafty/position.{bin,lrn}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc crafty.faq
%doc crafty.doc.ascii
%doc crafty.doc.ps
%doc README
%dir %{_prefix}/lib/games/crafty
%attr(755,root,root) %{_bindir}/crafty
%{_prefix}/lib/games/crafty/books.bin
