Name:		crafty
Version:	18.9
Summary:	Superior chess program by Bob Hyatt for Unix systems.
Group:		Applications/Games
Release:	2
ExcludeArch:	axp
License:	GPL
Icon:		xchess.gif
Source0:	ftp.cis.uab.edu:/pub/hyatt/%{name}-%{PACKAGE_VERSION}.tar.gz
Source1:	ftp.cis.uab.edu:/pub/hyatt/%{name}.faq
Source2:	ftp.cis.uab.edu:/pub/hyatt/read.me
Source3:	ftp.cis.uab.edu:/pub/hyatt/common/start.pgn
Source4:	ftp.cis.uab.edu:/pub/hyatt/v18/%{name}.doc.ascii
Source5:	ftp.cis.uab.edu:/pub/hyatt/v18/%{name}.doc.ps
Patch0:		%{name}-paths.patch
Provides:	chessprogram crafty

%description
Crafty is a Unix chess program, distributed as source by its author,
Bob Hyatt. The program plays at about 2200 strength and frequently
beats GNU Chess on the same hardware.

%prep
%setup -q -c -T -a 0
%patch -p1
cp ${RPM_SOURCE_DIR}/read.me README
cp ${RPM_SOURCE_DIR}/crafty.faq .
cp ${RPM_SOURCE_DIR}/crafty.doc.{ascii,ps} .
cp ${RPM_SOURCE_DIR}/start.pgn .

%build
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

%files
%defattr(644,root,root,755)
%doc crafty.faq
%doc crafty.doc.ascii
%doc crafty.doc.ps
%doc README
%dir %{_prefix}/lib/games/crafty
%attr(755,root,root) %{_bindir}/crafty
%{_prefix}/lib/games/crafty/books.bin
