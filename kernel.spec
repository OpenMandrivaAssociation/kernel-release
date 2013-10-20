%define kernelversion	3
%define patchlevel	11
# sublevel is now used for -stable patches
%define sublevel	6

# Package release
%define mibrel		69

# kernel Makefile extraversion is substituted by
# kpatch wich are either 0 (empty), rc (kpatch)
%define kpatch		0
# kernel.org -gitX patch (only the number after "git")
%define kgit		0

# kernel base name (also name of srpm)
%define kname 		kernel

# Patch tarball tag
%define ktag		rosa

%if %kpatch
%if %kgit
%define rpmrel		0.%{kpatch}.%{kgit}.%{mibrel}
%else
%define rpmrel		0.%{kpatch}.%{mibrel}
%endif
%else
%define rpmrel		1
%endif

# fakerel and fakever never change, they are used to fool
# rpm/urpmi/smart
%define fakever		1
%define fakerel 	1

# version defines
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define kverrel   	%{kversion}-%{rpmrel}

# When we are using a pre/rc patch, the tarball is a sublevel -1
%if %kpatch
%if %sublevel
%define tar_ver   	%{kernelversion}.%{patchlevel}
%else
%define tar_ver		%{kernelversion}.%(expr %{patchlevel} - 1)
%endif
%define patch_ver 	%{kversion}-%{kpatch}-%{ktag}%{mibrel}
%else
%define tar_ver   	%{kernelversion}.%{patchlevel}
%define patch_ver 	%{kversion}-%{ktag}%{mibrel}
%endif

# Used for not making too long names for rpms or search paths
# replaced mibrel with rpmrel / release > we can use only ONE sources folder for nrj & nrjQL
%if %kpatch
%if %kgit
%define buildrpmrel     0.%{kpatch}.%{kgit}.%{mibrel}%{disttag}
%else
%define buildrpmrel     0.%{kpatch}.%{rpmrel}%{disttag}
%endif
%else
%define buildrpmrel     %{release}%{disttag}
%endif
%define buildrel     	%{kversion}-%{buildrpmrel}

# Having different top level names for packges means that you have to remove
# them by hard :(
%define top_dir_name 	%{kname}-%{_arch}

%define build_dir 	${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir 	%{build_dir}/linux-%{tar_ver}

# Disable useless debug rpms...
%define _enable_debug_packages 	%{nil}
%define debug_package 		%{nil}

# Build defines
%bcond_without doc
%bcond_without source
%bcond_without devel
%bcond_with debug

# Old Mandriva kernel flavours plus new two PAE flavours added by MIB

%bcond_without desktop
%bcond_without netbook
%bcond_without server

%ifarch %{ix86}
%bcond_with desktop586
%bcond_without desktop_pae
%bcond_with netbook_pae
%endif

# MIB low latency optimized flavours called "nrj V.5" plus 32bit PAE versions

%bcond_without nrj_desktop
%bcond_without nrj_realtime
%bcond_without nrj_laptop
%bcond_without nrj_netbook

%ifarch %{ix86}
%bcond_with nrj_desktop586
%bcond_without nrj_desktop_pae
%bcond_without nrj_realtime_pae
%bcond_without nrj_laptop_pae
%bcond_with nrj_netbook_pae
%endif

# MIB experimental low latency "32bit cpu level" optimized, called "nrj V.5" flavours plus PAE versions

%ifarch %{ix86}
%bcond_with nrj_netbook_atom
%bcond_with nrj_netbook_atom_pae
%bcond_with nrj_desktop_core2
%bcond_with nrj_desktop_core2_pae
%endif

# MIB experimental low latency optimized flavours called "nrjQL V.5" with BFS, CK1, UKSM, TOI

%bcond_without nrjQL_desktop
%bcond_without nrjQL_realtime
%bcond_without nrjQL_laptop
%bcond_without nrjQL_netbook
%bcond_without nrjQL_server
%bcond_without nrjQL_server_games
%bcond_without nrjQL_server_computing

# MIB experimental low latency optimized flavours called "nrjQL V.5" with BFS, CK1, UKSM, TOI plus PAE 

%ifarch %{ix86}
%bcond_without nrjQL_desktop_pae
%bcond_without nrjQL_realtime_pae
%bcond_without nrjQL_laptop_pae
%bcond_without nrjQL_netbook_pae
%endif

# MIB experimental "32bit cpu level" optimized flavours called "nrjQL V.5" with BFS, CK1, UKSM, TOI plus PAE 

%ifarch %{ix86}
%bcond_with nrjQL_desktop_core2
%bcond_without nrjQL_desktop_core2_pae
%endif

# END OF FLAVOURS


# build perf and cpupower tools
%bcond_without perf
%bcond_without cpupower

# compress modules with xz
%bcond_without modxz

# ARM builds
%ifarch %{arm}
%bcond_with desktop
%bcond_with netbook
%bcond_with server
%bcond_with iop32x
%bcond_without kirkwood
%bcond_without versatile
# no cpupower tools on arm yet
%bcond_with cpupower
# arm is currently not using xz
%bcond_with modxz
%endif
# End of user definitions

# For the .nosrc.rpm
%define build_nosrc 	0
%{?_with_nosrc: %global build_nosrc 1}


############################################################
### Linker start1 > Check point to build for cooker 2013 ###
############################################################
%if %cross_compiling
%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make ARCH=%target_arch CROSS_COMPILE=%(echo %__cc |sed -e 's,-gcc,-,') CC="$CC" LD="$LD" LDFLAGS="$LDFLAGS"
%else
%define kmake %make ARCH=%target_arch CROSS_COMPILE=%(echo %__cc |sed -e 's,-gcc,-,') LD="$LD" LDFLAGS="$LDFLAGS"
%endif
# there are places where parallel make don't work
%define smake make ARCH=%target_arch CROSS_COMPILE=%(echo %__cc |sed -e 's,-gcc,-,') LD="$LD" LDFLAGS="$LDFLAGS"
%else
%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make CC="$CC" LD="$LD" LDFLAGS="$LDFLAGS"
%else
%define kmake %make LD="$LD" LDFLAGS="$LDFLAGS"
%endif
# there are places where parallel make don't work
%define smake make LD="$LD" LDFLAGS="$LDFLAGS"
%endif
###########################################################
###  Linker end1 > Check point to build for cooker 2013 ###
###########################################################


# Parallelize xargs invocations on smp machines
%define kxargs xargs %([ -z "$RPM_BUILD_NCPUS" ] \\\
	&& RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"; \\\
	[ "$RPM_BUILD_NCPUS" -gt 1 ] && echo "-P $RPM_BUILD_NCPUS")

# Sparc arch wants sparc64 kernels
%define target_arch    %(echo %{_arch} | sed -e 's/mips.*/mips/' -e 's/arm.*/arm/' -e 's/aarch64/arm64/')


#
# SRC RPM description
#
Summary: 	Linux kernel built for Mandriva and ROSA
Name:		%{kname}
Version: 	%{kversion}
Release: 	%{rpmrel}
License: 	GPLv2
Group: 	 	System/Kernel and hardware
ExclusiveArch: %{ix86} x86_64 %{arm} aarch64
ExclusiveOS: 	Linux
URL:            http://www.kernel.org

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/linux-%{tar_ver}.tar.xz
Source1: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/linux-%{tar_ver}.tar.sign
### This is for stripped SRC RPM
%if %build_nosrc
NoSource: 0
%endif
# This is for disabling *config, mrproper, prepare, scripts on -devel rpms
Source2: 	disable-mrproper-prepare-scripts-configs-in-devel-rpms.patch

Source4: 	README.kernel-sources
Source5:	kernel.rpmlintrc

# config and systemd service file from fedora
Source50:	cpupower.service
Source51:	cpupower.config

# our patch tarball
Source100: 	linux-%{patch_ver}.tar.xz

####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v3.0/testing

%if %kpatch
%if %sublevel
Patch2:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/stable-review/patch-%{kversion}-%{kpatch}.xz
Source11:	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/stable-review/patch-%{kversion}-%{kpatch}.sign
%else
Patch1:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/testing/patch-%{kernelversion}.%{patchlevel}-%{kpatch}.bz2
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/testing/patch-%{kernelversion}.%{patchlevel}-%{kpatch}.sign	
%endif	
%endif
%if %kgit
Patch2:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/snapshots/patch-%{kernelversion}.%{patchlevel}-%{kpatch}-git%{kgit}.xz
Source11: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/snapshots/patch-%{kernelversion}.%{patchlevel}-%{kpatch}-git%{kgit}.sign
%endif
%if %sublevel
%if %kpatch
%define prev_sublevel %(expr %{sublevel} - 1)
%if %prev_sublevel
Patch1:   	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/patch-%{kernelversion}.%{patchlevel}.%{prev_sublevel}.xz
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/patch-%{kernelversion}.%{patchlevel}.%{prev_sublevel}.sign
%endif
%else
Patch1:   	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/patch-%{kversion}.xz
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/patch-%{kversion}.sign
%endif
%endif

#END
####################################################################

# Defines for the things that are needed for all the kernels
#
%define common_desc_kernel The kernel package contains the Linux kernel (vmlinuz), the core of your \
Mandriva and ROSA operating system. The kernel handles the basic functions \
of the operating system: memory allocation, process allocation, device \
input and output, etc.

%define common_desc_kernel_smp This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.


### Global Requires/Provides

%define requires1	microcode
%define requires2	dracut >= 034
%define requires3	kmod >= 12
%define requires4	sysfsutils >=  2.1.0-12
%define requires5	kernel-firmware >=  20120219-1

%define kprovides1 	%{kname} = %{kverrel}
%define kprovides2 	kernel = %{tar_ver}
%define kprovides3 	alsa = 1.0.27
%define kprovides_server drbd-api = 88

%define	kobsoletes1	dkms-r8192se <= 0019.1207.2010-2
%define	kobsoletes2	dkms-lzma <= 4.43-32
%define	kobsoletes3	dkms-psb <= 4.41.1-7

# conflict dkms packages that dont support kernel-3.10
# all driver versions must be carefully checked to add

%define kconflicts1	dkms-broadcom-wl < 5.100.82.112-12
%define kconflicts2	dkms-fglrx < 13.200.5-1
%define kconflicts3	dkms-nvidia-current < 325.15-1
%define kconflicts4	dkms-nvidia-long-lived < 319.49-1
%define kconflicts5	dkms-nvidia304 < 304.108-1
# nvidia173 does not support this kernel
# nvidia96xx does not support this kernel or x11-server-1.13

Autoreqprov: 		no

# might be useful too:
Suggests:	microcode

BuildRequires:	kmod-devel kmod-compat

BuildRequires: 	gcc bc

# for perf, cpufreq and other tools
BuildRequires:		elfutils-devel
BuildRequires:		zlib-devel
BuildRequires:		binutils-devel
BuildRequires:		newt-devel
BuildRequires:		python-devel
BuildRequires:		perl(ExtUtils::Embed)
BuildRequires:		pciutils-devel
BuildRequires:		asciidoc
BuildRequires:		xmlto
BuildRequires:		gettext
BuildRequires:		docbook-style-xsl
BuildRequires:		pkgconfig(gtk+-2.0)
BuildRequires:		flex
BuildRequires:		bison

%ifarch %{arm}
BuildRequires:		uboot-mkimage
%endif


%description
%common_desc_kernel
%ifnarch %{arm}
%common_desc_kernel_smp
%endif

# Define obsolete/provides to help automatic upgrades of old kernel-xen-pvops
%define latest_obsoletes_server kernel-xen-pvops-latest < 3.2.1-1
%define latest_provides_server kernel-xen-pvops-latest = %{kverrel}
%define latest_obsoletes_devel_server kernel-xen-pvops-devel-latest < 3.2.1-1
%define latest_provides_devel_server kernel-xen-pvops-devel-latest = %{kverrel}

# mkflavour() name flavour processor
# name: the flavour name in the package name
# flavour: first parameter of CreateKernel()
%define mkflavour()					\
%package -n %{kname}-%{1}-%{buildrel}			\
Version:	%{fakever}				\
Release:	%{fakerel}				\
Provides:	%kprovides1 %kprovides2 %kprovides3	\
%{expand:%%{?kprovides_%{1}:Provides: %{kprovides_%{1}}}} \
Provides:   %{kname}-%{1}              			 \
%if %{with nrj_desktop}              		\
Provides:   kernel-desktop              		\
%endif                                  		\
Requires(pre):	%requires1 %requires2 %requires3 %requires4 \
Requires:	%requires2 %requires5			\
Obsoletes:	%kobsoletes1 %kobsoletes2 %kobsoletes3	\
Conflicts:	%kconflicts1 %kconflicts2 %kconflicts3	\
Conflicts:	%kconflicts4 %kconflicts5		\
Provides:	should-restart = system			\
Suggests:	crda					\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
Summary:	%{expand:%{summary_%(echo %{1} | sed -e "s/-/_/")}} \
Group:		System/Kernel and hardware		\
%description -n %{kname}-%{1}-%{buildrel}		\
%common_desc_kernel %{expand:%{info_%(echo %{1} | sed -e "s/-/_/")}} \
%ifnarch %{arm}						\
%common_desc_kernel_smp					\
%endif							\
							\
%if %{with devel}					\
%package -n	%{kname}-%{1}-devel-%{buildrel}		\
Version:	%{fakever}				\
Release:	%{fakerel}				\
Requires:	glibc-devel ncurses-devel make gcc perl	\
Summary:	The kernel-devel files for %{kname}-%{1}-%{buildrel} \
Group:		Development/Kernel			\
Provides:	%{kname}-devel = %{kverrel} 		\
Provides:	%{kname}-%{1}-devel			\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
%description -n %{kname}-%{1}-devel-%{buildrel}		\
This package contains the kernel files (headers and build tools) \
that should be enough to build additional drivers for   \
use with %{kname}-%{1}-%{buildrel}.                     \
							\
If you want to build your own kernel, you need to install the full \
%{kname}-source-%{buildrel} rpm.			\
							\
%endif							\
							\
%if %{with debug}					\
%package -n	%{kname}-%{1}-%{buildrel}-debuginfo	\
Version:	%{fakever}				\
Release:	%{fakerel}				\
Summary:	Files with debuginfo for %{kname}-%{1}-%{buildrel} \
Group:		Development/Debug			\
Provides:	kernel-debug = %{kverrel} 		\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
%description -n %{kname}-%{1}-%{buildrel}-debuginfo	\
This package contains the files with debuginfo to aid in debug tasks \
when using %{kname}-%{1}-%{buildrel}.			\
							\
If you need to look at debug information or use some application that \
needs debugging info from the kernel, this package may help. \
							\
%endif							\
							\
%package -n %{kname}-%{1}-latest			\
Version:	%{kversion}				\
Release:	%{rpmrel}				\
Summary:	Virtual rpm for latest %{kname}-%{1}	\
Group:		System/Kernel and hardware		\
Requires:	%{kname}-%{1}-%{buildrel}		\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
%{expand:%%{?latest_obsoletes_%{1}:Obsoletes: %{latest_obsoletes_%{1}}}} \
%{expand:%%{?latest_provides_%{1}:Provides: %{latest_provides_%{1}}}} \
%description -n %{kname}-%{1}-latest			\
This package is a virtual rpm that aims to make sure you always have the \
latest %{kname}-%{1} installed...			\
							\
%if %{with devel}					\
%package -n %{kname}-%{1}-devel-latest			\
Version:	%{kversion}				\
Release:	%{rpmrel}				\
Summary:	Virtual rpm for latest %{kname}-%{1}-devel \
Group:		Development/Kernel			\
Requires:	%{kname}-%{1}-devel-%{buildrel}		\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
Provides:	%{kname}-devel-latest			\
%{expand:%%{?latest_obsoletes_devel_%{1}:Obsoletes: %{latest_obsoletes_devel_%{1}}}} \
%{expand:%%{?latest_provides_devel_%{1}:Provides: %{latest_provides_devel_%{1}}}} \
%description -n %{kname}-%{1}-devel-latest		\
This package is a virtual rpm that aims to make sure you always have the \
latest %{kname}-%{1}-devel installed...			\
							\
%endif							\
							\
%post -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-post \
%posttrans -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-posttrans \
%preun -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-preun \
%postun -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-postun \
							\
%if %{with devel}					\
%post -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-post \
%preun -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-preun \
%postun -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-postun \
%endif							\
							\
%files -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1} \
%files -n %{kname}-%{1}-latest				\
							\
%if %{with devel}					\
%files -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1} \
%files -n %{kname}-%{1}-devel-latest			\
%endif							\
							\
%if %{with debug}					\
%files -n %{kname}-%{1}-%{buildrel}-debuginfo -f kernel_debug_files.%{1} \
%endif

%ifarch %{ix86}
#
# kernel-desktop586: i586, smp-alternatives, 4GB
#
%if %{with desktop586}
%define summary_desktop586 Linux kernel for desktop use with i586 & 4GB RAM
%define info_desktop586 This kernel is compiled for desktop use, single or \
multiple i586 processor(s)/core(s) and less than 4GB RAM, using HZ_1000, \
voluntary preempt, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour desktop586
%endif
%endif

#
# kernel-desktop: i686, smp-alternatives, 4 GB / x86_64
#
%if %{with desktop}
%ifarch %{ix86}
%define summary_desktop Linux Kernel for desktop use with i686 & 4GB RAM
%define info_desktop This kernel is compiled for desktop use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using HZ_1000, \
voluntary preempt, CFS cpu scheduler and BFQ i/o scheduler.
%else
%define summary_desktop Linux Kernel for desktop use with %{_arch}
%define info_desktop This kernel is compiled for desktop use, single or \
multiple %{_arch} processor(s)/core(s), using HZ_1000, \
voluntary preempt, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%endif
%mkflavour desktop
%endif

#
# kernel-netbook: i686, smp-alternatives, 4 GB / x86_64
#
%if %{with netbook}
%ifarch %{ix86}
%define summary_netbook Linux Kernel for netbook use with i686 & 4GB RAM
%define info_netbook This kernel is compiled for netbook use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using HZ_250, \
voluntary preempt, CFS cpu scheduler and BFQ i/o scheduler.
%else
%define summary_netbook Linux Kernel for netbook use with %{_arch}
%define info_netbook This kernel is compiled for netbook use, single or \
multiple %{_arch} processor(s)/core(s), using HZ_250, \
voluntary preempt, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%endif
%mkflavour netbook
%endif

#
# kernel-server: i686, smp-alternatives, 64 GB / x86_64
#
%if %{with server}
%ifarch %{ix86}
%define summary_server Linux Kernel for server use with i686 & 64GB RAM
%define info_server This kernel is compiled for server use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using \
no preempt, HZ_100, CFS cpu scheduler and BFQ i/o scheduler, PERFORMANCE governor.
%else
%define summary_server Linux Kernel for server use with %{_arch}
%define info_server This kernel is compiled for server use, single or \
multiple %{_arch} processor(s)/core(s), using no preempt, HZ_100, \
CFS cpu scheduler and BFQ i/o scheduler, PERFORMANCE governor.
%endif
%mkflavour server
%endif

%ifarch %{ix86}
#
# kernel-desktop-pae: i686, smp-alternatives, 64GB
#
%if %{with desktop_pae}
%define summary_desktop_pae Linux kernel for desktop use with i686 & upto 64GB RAM
%define info_desktop_pae This kernel is compiled for desktop use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using HZ_1000, \
voluntary preempt, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour desktop-pae
%endif
%endif

%ifarch %{ix86}
#
# kernel-netbook-pae: i686, smp-alternatives, 64 GB
#
%if %{with netbook_pae}
%define summary_netbook_pae Linux Kernel for for netbook use with i686 & upto 64GB RAM
%define info_netbook_pae This kernel is compiled for netbook use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using HZ_250, \
voluntary preempt, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour netbook-pae
%endif
%endif

%ifarch %{ix86}
#
# kernel-nrj-desktop586: nrj, i586, smp-alternatives, 4GB
#
%if %{with nrj_desktop586}
%define summary_nrj_desktop586 Linux kernel for desktop use with i586 & 4GB RAM
%define info_nrj_desktop586 This kernel is compiled for desktop use, single or \
multiple i586 processor(s)/core(s) and less than 4GB RAM, using HZ_1000, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour nrj-desktop586
%endif
%endif

#
# kernel-nrj-desktop: nrj, i686, smp-alternatives, 4 GB / x86_64
#
%if %{with nrj_desktop}
%ifarch %{ix86}
%define summary_nrj_desktop Linux Kernel for desktop use with i686 & 4GB RAM
%define info_nrj_desktop This kernel is compiled for desktop use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using HZ_1000, \
full preempt, rcu boost, RIFS cpu scheduler and BFQ I/O scheduler, ONDEMAND governor.
%else
%define summary_nrj_desktop Linux Kernel for desktop use with %{_arch}
%define info_nrj_desktop This kernel is compiled for desktop use, single or \
multiple %{_arch} processor(s)/core(s), using HZ_1000, \
full preempt, rcu boost, RIFS cpu scheduler and BFQ I/O scheduler, ONDEMAND governor.
%endif
%mkflavour nrj-desktop
%endif

#
# kernel-nrj-realtime: nrj, i686, smp-alternatives, 4 GB / x86_64
#
%if %{with nrj_realtime}
%ifarch %{ix86}
%define summary_nrj_realtime Linux Kernel for low latency use with i686 & 4GB RAM
%define info_nrj_realtime This kernel is compiled for low latency use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using HZ_1000, \
full preempt, rcu boost, CFS cpu scheduler and new BFQ I/O scheduler, PERFORMANCE governor.
%else
%define summary_nrj_realtime Linux Kernel for low latency use with %{_arch}
%define info_nrj_realtime This kernel is compiled for low latency use, single or \
multiple %{_arch} processor(s)/core(s), using HZ_1000, \
full preempt, rcu boost, CFS cpu scheduler and new BFQ I/O scheduler, PERFORMANCE governor.
%endif
%mkflavour nrj-realtime
%endif

#
# kernel-nrj-laptop: nrj, i686, smp-alternatives, 4 GB / x86_64
#
%if %{with nrj_laptop}
%ifarch %{ix86}
%define summary_nrj_laptop Linux Kernel for laptop use with i686 & 4GB RAM
%define info_nrj_laptop This kernel is compiled for laptop use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using HZ_300, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%else
%define summary_nrj_laptop Linux Kernel for laptop use with %{_arch}
%define info_nrj_laptop This kernel is compiled for laptop use, single or \
multiple %{_arch} processor(s)/core(s), using HZ_300, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%endif
%mkflavour nrj-laptop
%endif

#
# kernel-nrj-netbook: nrj, i686, smp-alternatives, 4 GB / x86_64
#
%if %{with nrj_netbook}
%ifarch %{ix86}
%define summary_nrj_netbook Linux Kernel for netbook use with i686 & 4GB RAM
%define info_nrj_netbook This kernel is compiled for netbook use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using HZ_250, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%else
%define summary_nrj_netbook Linux Kernel for netbook use with %{_arch}
%define info_nrj_netbook This kernel is compiled for netbook use, single or \
multiple %{_arch} processor(s)/core(s), using HZ_250, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%endif
%mkflavour nrj-netbook
%endif

#
%ifarch %{ix86}
#
# kernel-nrj-desktop-pae: nrj, i686, smp-alternatives, 64GB
#
%if %{with nrj_desktop_pae}
%define summary_nrj_desktop_pae Linux kernel for desktop use with i686 & upto 64GB RAM
%define info_nrj_desktop_pae This kernel is compiled for desktop use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using HZ_1000, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour nrj-desktop-pae
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrj-realtime-pae: nrj, i686, smp-alternatives, 64GB
#
%if %{with nrj_realtime_pae}
%define summary_nrj_realtime_pae Linux kernel for low latency use with i686 & upto 64GB RAM
%define info_nrj_realtime_pae This kernel is compiled for low latency use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using HZ_1000, \
full preempt, rcu boost, CFS cpu scheduler and new BFQ I/O scheduler, PERFORMANCE governor.
%mkflavour nrj-realtime-pae
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrj-laptop-pae: nrj, i686, smp-alternatives, 64 GB
#
%if %{with nrj_laptop_pae}
%define summary_nrj_laptop_pae Linux Kernel for for laptop use with i686 & upto 64GB RAM
%define info_nrj_laptop_pae This kernel is compiled for laptop use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using HZ_300, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour nrj-laptop-pae
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrj-netbook-pae: nrj, i686, smp-alternatives, 64 GB
#
%if %{with nrj_netbook_pae}
%define summary_nrj_netbook_pae Linux Kernel for for netbook use with i686 & upto 64GB RAM
%define info_nrj_netbook_pae This kernel is compiled for netbook use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using HZ_250, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour nrj-netbook-pae
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrj-netbook-atom: nrj, for Intel Atom cpu, smp-alternatives, 4 GB
#
%if %{with nrj_netbook_atom}
%define summary_nrj_netbook_atom Linux Kernel for netbook use with Intel Atom cpu, less than 4GB RAM
%define info_nrj_netbook_atom This kernel is compiled for netbook use, single or \
multiple Intel Atom cpu processor(s)/core(s) and less than 4GB RAM, using HZ_250, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour nrj-netbook-atom
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrj-netbook-atom-pae: nrj, for Intel Atom cpu, smp-alternatives, 64 GB
#
%if %{with nrj_netbook_atom_pae}
%define summary_nrj_netbook_atom_pae Linux Kernel for netbook use with Intel Atom cpu & upto 64GB RAM
%define info_nrj_netbook_atom_pae This kernel is compiled for netbook use, single or \
multiple Intel Atom cpu processor(s)/core(s) and up to 64GB RAM using PAE, using HZ_250, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour nrj-netbook-atom-pae
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrj-desktop-core2: nrj, Intel Core 2 and newer, smp-alternatives, 4 GB 
#
%if %{with nrj_desktop_core2}
%define summary_nrj_desktop_core2 Linux Kernel for desktop use with i686 & 4GB RAM
%define info_nrj_desktop_core2 This kernel is compiled for desktop use, single or \
multiple Intel Core 2 and newer processor(s)/core(s) and less than 4GB RAM, using HZ_1000, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour nrj-desktop-core2
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrj-desktop-core2-pae: nrj, Intel Core 2 and newer, smp-alternatives, 64 GB
#
%if %{with nrj_desktop_core2_pae}
%define summary_nrj_desktop_core2_pae Linux Kernel for desktop use with i686 & upto 64GB RAM
%define info_nrj_desktop_core2_pae This kernel is compiled for desktop use, single or \
multiple Intel Core 2 and newer processor(s)/core(s) and up to 64GB RAM using PAE, using HZ_1000, \
full preempt, rcu boost, CFS cpu scheduler and BFQ i/o scheduler, ONDEMAND governor.
%mkflavour nrj-desktop-core2-pae
%endif
%endif

#
# ARM kernels
#
%ifarch %{arm}
%if %{with iop32x}
%define summary_iop32x Linux Kernel for Arm machines based on Xscale IOP32X
%define info_iop32x This kernel is compiled for iop32x boxes. It will run on n2100 \
or ss4000e or sanmina boards.
%mkflavour iop32x
%endif
%if %{with kirkwood}
%define summary_kirkwood Linux Kernel for Arm machines based on Kirkwood
%define info_kirkwood This kernel is compiled for kirkwood boxes. It will run on openrd boards.
%mkflavour kirkwood
%endif
%if %{with versatile}
%define summary_versatile Linux Kernel for Versatile arm machines
%define info_versatile This kernel is compiled for Versatile boxes. It will run on Qemu for instance.
%mkflavour versatile
%endif
%endif

#
# kernel-nrjQL-desktop: nrjQL, i686, smp-alternatives, 4 GB / x86_64
#
%if %{with nrjQL_desktop}
%ifarch %{ix86}
%define summary_nrjQL_desktop Linux Kernel for desktop use with i686 & 4GB RAM
%define info_nrjQL_desktop This kernel is compiled for desktop use, single or \
multiple i686 processor(s)/core(s), less than 4GB RAM (usually 3-3.5GB detected)\
using HZ_1000, full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler.\
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_nrjQL_desktop Linux Kernel for desktop use with %{_arch}
%define info_nrjQL_desktop This kernel is compiled for desktop use, single or \
multiple %{_arch} processor(s)/core(s),\
using HZ_1000, full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler.\
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour nrjQL-desktop
%endif

#
# kernel-nrjQL-realtime: nrjQL, i686, smp-alternatives, 4 GB / x86_64
#
%if %{with nrjQL_realtime}
%ifarch %{ix86}
%define summary_nrjQL_realtime Linux Kernel for desktop and realtime use with i686 & 4GB RAM
%define info_nrjQL_realtime This kernel is compiled for desktop and realtime use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM (usually 3-3.5GB detected), \
using full preempt and realtime, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler.\
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_nrjQL_realtime Linux Kernel for desktop and realtime use with %{_arch}
%define info_nrjQL_realtime This kernel is compiled for desktop and realtime use, single or \
multiple %{_arch} processor(s)/core(s), \
using full preempt and realtime, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler.\
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour nrjQL-realtime
%endif

#
# kernel-nrjQL-laptop: nrjQL, i686, smp-alternatives, 4 GB / x86_64
#
%if %{with nrjQL_laptop}
%ifarch %{ix86}
%define summary_nrjQL_laptop Linux Kernel for laptop use with i686 & 4GB RAM
%define info_nrjQL_laptop This kernel is compiled for laptop use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM (usually 3-3.5GB detected), \
using HZ_300 and CPU frequency scaling ondemand default, everything to save battery, \
using full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler, \
and some other laptop-specific optimizations. \
If you want to sacrifice battery life for performance, you better use the \
%{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter. \
NOTE! This kernel also uses TuxOnIce by default.
%else
%define summary_nrjQL_laptop Linux Kernel for laptop use with %{_arch}
%define info_nrjQL_laptop This kernel is compiled for laptop use, single or \
multiple %{_arch} processor(s)/core(s), \
using HZ_300 and CPU frequency scaling ondemand default, everything to save battery, \
using full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler, \
and some other laptop-specific optimizations. \
If you want to sacrifice battery life for performance, you better use the \
%{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter. \
NOTE! This kernel also uses TuxOnIce by default.
%endif
%mkflavour nrjQL-laptop
%endif

#
# kernel-nrjQL-netbook: nrj, i686, smp-alternatives, 4 GB / x86_64
#
%if %{with nrjQL_netbook}
%ifarch %{ix86}
%define summary_nrjQL_netbook Linux Kernel for netbook use with i686 & 4GB RAM
%define info_nrjQL_netbook This kernel is compiled for netbook use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM (usually 3-3.5GB detected), \
using HZ_250 and CPU frequency scaling ondemand default, everything to save battery, \
using full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler, \
and some other netbook-specific optimizations. \
If you want to sacrifice battery life for performance, you better use the \
%{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter. \
NOTE! This kernel also uses TuxOnIce by default.
%else
%define summary_nrjQL_netbook Linux Kernel for netbook use with %{_arch}
%define info_nrjQL_netbook This kernel is compiled for netbook use, single or \
multiple %{_arch} processor(s)/core(s), \
using HZ_250 and CPU frequency scaling ondemand default, everything to save battery, \
using full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler, \
and some other netbook-specific optimizations. \
If you want to sacrifice battery life for performance, you better use the \
%{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter. \
NOTE! This kernel also uses TuxOnIce by default.
%endif
%mkflavour nrjQL-netbook
%endif

#
# kernel-server: i686, smp-alternatives, 64 GB / x86_64
#
%if %{with nrjQL_server}
%ifarch %{ix86}
%define summary_nrjQL_server Linux Kernel for server use with i686 & 64GB RAM
%define info_nrjQL_server This kernel is compiled for server use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using \
no preempt, HZ_100, CK1, BFS cpu scheduler, BFQ I/O scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_nrjQL_server Linux Kernel for server use with %{_arch}
%define info_nrjQL_server This kernel is compiled for server use, single or \
multiple %{_arch} processor(s)/core(s), using no preempt, HZ_100, \
CK1, BFS cpu scheduler, BFQ I/O scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour nrjQL-server
%endif

#
# kernel-server-computing: i686, smp-alternatives, 64 GB / x86_64
#
%if %{with nrjQL_server_computing}
%ifarch %{ix86}
%define summary_nrjQL_server_computing Linux Kernel for server use with i686 & 64GB RAM
%define info_nrjQL_server_computing This kernel is compiled for server use, to obtain a \
optimized dedicated encoding / compiling / computational machine, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using \
no preempt, HZ_100, CK1, BFS cpu scheduler, BFQ I/O scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_nrjQL_server_computing Linux Kernel for server use with %{_arch}
%define info_nrjQL_server_computing This kernel is compiled for server use, to obtain a \
optimized dedicated encoding / compiling / computational machine, single or \
multiple %{_arch} processor(s)/core(s), using no preempt, HZ_100, \
CK1, BFS cpu scheduler, BFQ I/O scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour nrjQL-server-computing
%endif

#
# kernel-server-games: i686, smp-alternatives, 64 GB / x86_64
#
%if %{with nrjQL_server_games}
%ifarch %{ix86}
%define summary_nrjQL_server_games Linux Kernel for games server use with i686 & 64GB RAM
%define info_nrjQL_server_games This kernel is compiled for games server use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, \
using no preempt, HZ_3000, CK1, BFS cpu scheduler, BFQ I/O scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_nrjQL_server_games Linux Kernel for games server use with %{_arch}
%define info_nrjQL_server_games This kernel is compiled for games server use, single or \
multiple %{_arch} processor(s)/core(s), \
using no preempt, HZ_3000, CK1, BFS cpu scheduler, BFQ I/O scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour nrjQL-server-games
%endif

#
%ifarch %{ix86}
#
# kernel-nrjQL-desktop-pae: nrjQL, i686, smp-alternatives, 64GB
#
%if %{with nrjQL_desktop_pae}
%define summary_nrjQL_desktop_pae Linux kernel for desktop use with i686 & upto 64GB RAM
%define info_nrjQL_desktop_pae This kernel is compiled for desktop use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, \
using HZ_1000, full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler.\
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%mkflavour nrjQL-desktop-pae
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrjQL-realtime-pae: nrjQL, i686, smp-alternatives, 64GB
#
%if %{with nrjQL_realtime_pae}
%define summary_nrjQL_realtime_pae Linux kernel for desktop and realtime use with i686 & upto 64GB RAM
%define info_nrjQL_realtime_pae This kernel is compiled for desktop and realtime use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, \
using full preempt and realtime, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler.\
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%mkflavour nrjQL-realtime-pae
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrjQL-laptop-pae: nrjQL, i686, smp-alternatives, 64 GB
#
%if %{with nrjQL_laptop_pae}
%define summary_nrjQL_laptop_pae Linux Kernel for for laptop use with i686 & upto 64GB RAM
%define info_nrjQL_laptop_pae This kernel is compiled for laptop use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, \
using HZ_300 and CPU frequency scaling ondemand default, everything to save battery, \
using full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler, \
and some other laptop-specific optimizations. \
If you want to sacrifice battery life for performance, you better use the \
%{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter. \
NOTE! This kernel also uses TuxOnIce by default.
%mkflavour nrjQL-laptop-pae
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrjQL-netbook-pae: nrjQL, i686, smp-alternatives, 64 GB
#
%if %{with nrjQL_netbook_pae}
%define summary_nrjQL_netbook_pae Linux Kernel for netbook use with i686 & upto 64GB RAM
%define info_nrjQL_netbook_pae This kernel is compiled for netbook use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, \
using HZ_250 and CPU frequency scaling ondemand default, everything to save battery, \
using full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler, \
and some other netbook-specific optimizations. \
If you want to sacrifice battery life for performance, you better use the \
%{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter. \
NOTE! This kernel also uses TuxOnIce by default.
%mkflavour nrjQL-netbook-pae
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrjQL-desktop-core2: nrjQL, Intel Core 2 and newer, smp-alternatives, 4 GB 
#
%if %{with nrjQL_desktop_core2}
%define summary_nrjQL_desktop_core2 Linux Kernel for desktop use with i686 & 4GB RAM
%define info_nrjQL_desktop_core2 This kernel is compiled for desktop use, single or \
multiple Intel Core 2 and newer processor(s)/core(s) and less than 4GB RAM (usually 3-3.5GB detected), \
using HZ_1000, full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler.\
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%mkflavour nrjQL-desktop-core2
%endif
%endif

#
%ifarch %{ix86}
#
# kernel-nrjQL-desktop-core2-pae: nrjQL, Intel Core 2 and newer, smp-alternatives, 64 GB
#
%if %{with nrjQL_desktop_core2_pae}
%define summary_nrjQL_desktop_core2_pae Linux Kernel for desktop use with i686 & upto 64GB RAM
%define info_nrjQL_desktop_core2_pae This kernel is compiled for desktop use, single or \
multiple Intel Core 2 and newer processor(s)/core(s) and up to 64GB RAM using PAE, \
using HZ_1000, full preempt, rcu boost, CK1, BFS cpu scheduler, BFQ I/O scheduler.\
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%mkflavour nrjQL-desktop-core2-pae
%endif
%endif


#
# kernel-source
#
%if %{with source}
%package -n %{kname}-source-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl, diffutils
Summary: 	The Linux source code for %{kname}-%{buildrel}
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source = %{kverrel}
Buildarch:	noarch

%description -n %{kname}-source-%{buildrel}
The %{kname}-source package contains the source code files for the Mandriva and
ROSA kernel. Theese source files are only needed if you want to build your own
custom kernel that is better tuned to your particular hardware.

If you only want the files needed to build 3rdparty (nVidia, Ati, dkms-*,...)
drivers against, install the *-devel-* rpm that is matching your kernel.

#
# kernel-source-latest: virtual rpm
#
%package -n %{kname}-source-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source
Group:   	Development/Kernel
Requires: 	%{kname}-source-%{buildrel}
Buildarch:	noarch

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...
%endif

#
# kernel-doc: documentation for the Linux kernel
#
%if %{with doc}
%package -n %{kname}-doc
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Various documentation bits found in the %{kname} source
Group: 		Documentation
Buildarch:	noarch

%description -n %{kname}-doc
This package contains documentation files from the %{kname} source.
Various bits of information about the Linux kernel and the device drivers
shipped with it are documented in these files. You also might want install
this package if you need a reference to the options that can be passed to
Linux kernel modules at load time.
%endif

#
# kernel/tools
#
%if %{with perf}
%package -n perf
Version:	%{kversion}
Release:	%{rpmrel}
Summary:	perf tool and the supporting documentation
Group:		System/Kernel and hardware

%description -n perf
the perf tool and the supporting documentation.
%endif

%if %{with cpupower}
%package -n cpupower
Version:	%{kversion}
Release:	%{rpmrel}
Summary:	the cpupower tools
Group:		System/Kernel and hardware
Requires(post):  rpm-helper >= 0.24.0-3
Requires(preun): rpm-helper >= 0.24.0-3
Obsoletes:	cpufreq cpufrequtils

%description -n cpupower
the cpupower tools.

%post -n cpupower
%_post_service cpupower

%preun -n cpupower
%_preun_service cpupower

%package -n cpupower-devel
Version:	%{kversion}
Release:	%{rpmrel}
Summary:	devel files for cpupower
Group:		Development/Kernel
Requires:	cpupower = %{kversion}-%{rpmrel}
Conflicts:	%{_lib}cpufreq-devel

%description -n cpupower-devel
This package contains the development files for cpupower.
%endif

%package headers
Version:	%kversion
Release:	%rpmrel
Summary:	Linux kernel header files mostly used by your C library
Group:		System/Kernel and hardware
Epoch:		1
%rename linux-userspace-headers

%description headers
C header files from the Linux kernel. The header files define
structures and constants that are needed for building most
standard programs, notably the C library.

This package is not suitable for building kernel modules, you
should use the 'kernel-devel' package instead.

%files headers
%_includedir/*
# Don't conflict with cpupower-devel
%if %{with cpupower}
%exclude %_includedir/cpufreq.h
%endif

#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c
%setup -q -n %top_dir_name -D -T -a100

%define patches_dir ../%{patch_ver}/

cd %src_dir

%if %sublevel
%if %kpatch
%if %prev_sublevel
%patch1 -p1
%endif
%patch2 -p1
%else
%patch1 -p1
%endif
%else
%if %kpatch
%patch1 -p1
%endif
%endif
%if %kgit
%patch2 -p1
%endif


#
# Setup Begin
#

# Prepare all the variables for calling create_configs

%if %{with debug}
%define debug --debug
%else
%define debug --no-debug
%endif


# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile

# get rid of unwanted files
find . -name '*~' -o -name '*.orig' -o -name '*.append' | %kxargs rm -f


%build

############################################################
### Linker start2 > Check point to build for cooker 2013 ###
############################################################
# Make sure we don't use gold
export LD="%{_target_platform}-ld.bfd"
export LDFLAGS="--hash-style=sysv --build-id=none"
############################################################
###  Linker end2 > Check point to build for cooker 2013  ###
############################################################

# Common target directories
%define _kerneldir /usr/src/linux-%{kversion}-%{buildrpmrel}
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _efidir %{_bootdir}/efi/mandriva

# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}

PrepareKernel() {
	name=$1
	extension=$2
%ifarch %{ix86} x86_64
	config_dir=arch/x86/configs
%endif
%ifarch	%arm
	config_dir=arch/arm/configs
%endif
%ifarch aarc64
	config_dir=arch/arm64/configs
%endif
	echo "Make config for kernel $extension"

	%smake -s mrproper

	if [ "%{target_arch}" == "i386" -o "%{target_arch}" == "x86_64" ]; then
	    if [ -z "$name" ]; then
		cp ${config_dir}/%{target_arch}_defconfig-desktop .config
	    else
		cp ${config_dir}/%{target_arch}_defconfig-$name .config
	    fi
	else
	    if [ -z "$name" ]; then
		cp arch/%{target_arch}/defconfig-desktop .config
	    else
		cp arch/%{target_arch}/defconfig-$name .config
	    fi
	fi

	# make sure EXTRAVERSION says what we want it to say
	LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile

	%smake oldconfig
}

BuildKernel() {
	KernelVer=$1

	echo "Building kernel $KernelVer"

	%kmake -s all

	# kirkwood boxes have u-boot
	if [ "$KernelVer" = "%{kversion}-kirkwood-%{buildrpmrel}" ]; then
		%kmake uImage
	fi

	# Start installing stuff
	install -d %{temp_boot}
	install -m 644 System.map %{temp_boot}/System.map-$KernelVer
	install -m 644 .config %{temp_boot}/config-$KernelVer
	xz -c Module.symvers > %{temp_boot}/symvers-$KernelVer.xz

	%ifarch %{arm}
		if [ -f arch/arm/boot/uImage ]; then
			cp -f arch/arm/boot/uImage %{temp_boot}/uImage-$KernelVer
		else
			cp -f arch/arm/boot/zImage %{temp_boot}/vmlinuz-$KernelVer
		fi
	%else
		cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install

	# headers	
	%make INSTALL_HDR_PATH=%{temp_root}%_prefix KERNELRELEASE=$KernelVer headers_install

	# remove /lib/firmware, we use a separate kernel-firmware
	rm -rf %{temp_root}/lib/firmware
}

SaveDevel() {
	devel_flavour=$1

	DevelRoot=/usr/src/linux-%{kversion}-$devel_flavour-%{buildrpmrel}
	TempDevelRoot=%{temp_root}$DevelRoot

	mkdir -p $TempDevelRoot
	for i in $(find . -name 'Makefile*'); do cp -R --parents $i $TempDevelRoot;done
	for i in $(find . -name 'Kconfig*' -o -name 'Kbuild*'); do cp -R --parents $i $TempDevelRoot;done
	cp -fR include $TempDevelRoot
	ln -s ../generated/uapi/linux/version.h $TempDevelRoot/include/linux/version.h
	cp -fR scripts $TempDevelRoot
	cp -fR kernel/bounds.c $TempDevelRoot/kernel
	cp -fR tools/include $TempDevelRoot/tools/
	%ifarch %{arm}
		cp -fR arch/%{target_arch}/tools $TempDevelRoot/arch/%{target_arch}/
	%endif
	%ifarch %{ix86} x86_64
		cp -fR arch/x86/kernel/asm-offsets.{c,s} $TempDevelRoot/arch/x86/kernel/
		cp -fR arch/x86/kernel/asm-offsets_{32,64}.c $TempDevelRoot/arch/x86/kernel/
		cp -fR arch/x86/syscalls/syscall* $TempDevelRoot/arch/x86/syscalls/
		cp -fR arch/x86/include $TempDevelRoot/arch/x86/
		cp -fR arch/x86/tools $TempDevelRoot/arch/x86/
	%else
		cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} $TempDevelRoot/arch/%{target_arch}/kernel/
		for f in $(find arch/%{target_arch} -name include); do cp -fR --parents $f $TempDevelRoot; done
	%endif
	cp -fR .config Module.symvers $TempDevelRoot
	cp -fR 3rdparty/mkbuild.pl $TempDevelRoot/3rdparty

	# Needed for truecrypt build (Danny)
	cp -fR drivers/md/dm.h $TempDevelRoot/drivers/md/

	# Needed for lguest
	cp -fR drivers/lguest/lg.h $TempDevelRoot/drivers/lguest/

	# Needed for lirc_gpio (#39004)
	cp -fR drivers/media/pci/bt8xx/bttv{,p}.h $TempDevelRoot/drivers/media/pci/bt8xx/
	cp -fR drivers/media/pci/bt8xx/bt848.h $TempDevelRoot/drivers/media/pci/bt8xx/
	cp -fR drivers/media/common/btcx-risc.h $TempDevelRoot/drivers/media/common/

	# Needed for external dvb tree (#41418)
	cp -fR drivers/media/dvb-core/*.h $TempDevelRoot/drivers/media/dvb-core/
	cp -fR drivers/media/dvb-frontends/lgdt330x.h $TempDevelRoot/drivers/media/dvb-frontends/

	# add acpica header files, needed for fglrx build
	cp -fR drivers/acpi/acpica/*.h $TempDevelRoot/drivers/acpi/acpica/

	# aufs2 has a special file needed
	cp -fR fs/aufs/magic.mk $TempDevelRoot/fs/aufs

	for i in alpha arc avr32 blackfin c6x cris frv h8300 hexagon ia64 m32r m68k m68knommu metag microblaze \
		 mips mn10300 openrisc parisc powerpc s390 score sh sparc tile unicore32 xtensa; do
		rm -rf $TempDevelRoot/arch/$i
	done

	%ifnarch %{arm}
		rm -rf $TempDevelRoot/arch/arm
		rm -rf $TempDevelRoot/include/kvm/arm*
	%endif
	%ifnarch aarch64
		rm -rf $TempDevelRoot/arch/arm64
	%endif
	%ifnarch %{ix86} x86_64
		rm -rf $TempDevelRoot/arch/x86
	%endif

	# Clean the scripts tree, and make sure everything is ok (sanity check)
	# running prepare+scripts (tree was already "prepared" in build)
	pushd $TempDevelRoot >/dev/null
		%smake -s prepare scripts
		%smake -s clean
	popd >/dev/null
	rm -f $TempDevelRoot/.config.old

	# fix permissions
	chmod -R a+rX $TempDevelRoot

	# disable mrproper in -devel rpms
	patch -p1 --fuzz=0 -b -z .nomrproper~ -d $TempDevelRoot -i %{SOURCE2}

	kernel_devel_files=../kernel_devel_files.$devel_flavour


### Create the kernel_devel_files.*
cat > $kernel_devel_files <<EOF
%dir $DevelRoot
%dir $DevelRoot/arch
%dir $DevelRoot/include
$DevelRoot/3rdparty
$DevelRoot/Documentation
%ifarch %{arm}
$DevelRoot/arch/arm
$DevelRoot/arch/arm64
%endif
$DevelRoot/arch/um
%ifarch %{ix86} x86_64
$DevelRoot/arch/x86
%endif
$DevelRoot/block
$DevelRoot/crypto
$DevelRoot/drivers
$DevelRoot/firmware
$DevelRoot/fs
$DevelRoot/include/Kbuild
$DevelRoot/include/acpi
$DevelRoot/include/asm-generic
$DevelRoot/include/clocksource
$DevelRoot/include/config
$DevelRoot/include/crypto
$DevelRoot/include/drm
$DevelRoot/include/dt-bindings
$DevelRoot/include/generated
$DevelRoot/include/keys
$DevelRoot/include/linux
$DevelRoot/include/math-emu
$DevelRoot/include/media
$DevelRoot/include/memory
$DevelRoot/include/misc
$DevelRoot/include/net
$DevelRoot/include/pcmcia
$DevelRoot/include/ras
$DevelRoot/include/rdma
$DevelRoot/include/rxrpc
$DevelRoot/include/scsi
$DevelRoot/include/sound
$DevelRoot/include/target
$DevelRoot/include/trace
$DevelRoot/include/uapi
$DevelRoot/include/video
$DevelRoot/include/xen
$DevelRoot/init
$DevelRoot/ipc
$DevelRoot/kernel
$DevelRoot/lib
$DevelRoot/mm
$DevelRoot/net
$DevelRoot/samples
$DevelRoot/scripts
$DevelRoot/security
$DevelRoot/sound
$DevelRoot/tools
$DevelRoot/usr
$DevelRoot/virt
$DevelRoot/.config
$DevelRoot/Kbuild
$DevelRoot/Kconfig
$DevelRoot/Makefile
$DevelRoot/Module.symvers
$DevelRoot/arch/Kconfig
%doc README.kernel-sources
EOF


### Create -devel Post script on the fly
cat > $kernel_devel_files-post <<EOF
if [ -d /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel} ]; then
	rm -f /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/{build,source}
	ln -sf $DevelRoot /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/build
	ln -sf $DevelRoot /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/source
fi
EOF


### Create -devel Preun script on the fly
cat > $kernel_devel_files-preun <<EOF
if [ -L /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/build ]; then
	rm -f /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/build
fi
if [ -L /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/source ]; then
	rm -f /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/source
fi
exit 0
EOF

### Create -devel Postun script on the fly
cat > $kernel_devel_files-postun <<EOF
rm -rf /usr/src/linux-%{kversion}-$devel_flavour-%{buildrpmrel} >/dev/null
EOF
}

SaveDebug() {
	debug_flavour=$1

	install -m 644 vmlinux \
	      %{temp_boot}/vmlinux-%{kversion}-$debug_flavour-%{buildrpmrel}
	kernel_debug_files=../kernel_debug_files.$debug_flavour
	echo "%{_bootdir}/vmlinux-%{kversion}-$debug_flavour-%{buildrpmrel}" \
		>> $kernel_debug_files

	find %{temp_modules}/%{kversion}-$debug_flavour-%{buildrpmrel}/kernel \
		-name "*.ko" | \
		%kxargs -I '{}' objcopy --only-keep-debug '{}' '{}'.debug
	find %{temp_modules}/%{kversion}-$debug_flavour-%{buildrpmrel}/kernel \
		-name "*.ko" | %kxargs -I '{}' \
		sh -c 'cd `dirname {}`; \
		       objcopy --add-gnu-debuglink=`basename {}`.debug \
		       --strip-debug `basename {}`'

	pushd %{temp_modules}
	find %{kversion}-$debug_flavour-%{buildrpmrel}/kernel \
		-name "*.ko.debug" > debug_module_list
	popd
	cat %{temp_modules}/debug_module_list | \
		sed 's|\(.*\)|%{_modulesdir}/\1|' >> $kernel_debug_files
	cat %{temp_modules}/debug_module_list | \
		sed 's|\(.*\)|%exclude %{_modulesdir}/\1|' \
		>> ../kernel_exclude_debug_files.$debug_flavour
	rm -f %{temp_modules}/debug_module_list
}

CreateFiles() {
	kernel_flavour=$1

	kernel_files=../kernel_files.$kernel_flavour

ker="vmlinuz"
if [ "$kernel_flavour" = "kirkwood" ]; then
       ker="uImage"
fi
### Create the kernel_files.*
cat > $kernel_files <<EOF
%{_bootdir}/System.map-%{kversion}-$kernel_flavour-%{buildrpmrel}
%{_bootdir}/symvers-%{kversion}-$kernel_flavour-%{buildrpmrel}.xz
%{_bootdir}/config-%{kversion}-$kernel_flavour-%{buildrpmrel}
%{_bootdir}/$ker-%{kversion}-$kernel_flavour-%{buildrpmrel}
%dir %{_modulesdir}/%{kversion}-$kernel_flavour-%{buildrpmrel}/
%{_modulesdir}/%{kversion}-$kernel_flavour-%{buildrpmrel}/kernel
%{_modulesdir}/%{kversion}-$kernel_flavour-%{buildrpmrel}/modules.*
%doc README.kernel-sources
EOF

%if %{with debug}
    cat ../kernel_exclude_debug_files.$kernel_flavour >> $kernel_files
%endif

### Create kernel Post script
cat > $kernel_files-post <<EOF
%ifarch %{arm}
/sbin/installkernel -i -N %{kversion}-$kernel_flavour-%{buildrpmrel}
%else
/sbin/installkernel %{kversion}-$kernel_flavour-%{buildrpmrel}
pushd /boot > /dev/null
if [ -L vmlinuz-$kernel_flavour ]; then
	rm -f vmlinuz-$kernel_flavour
fi
ln -sf vmlinuz-%{kversion}-$kernel_flavour-%{buildrpmrel} vmlinuz-$kernel_flavour
if [ -L initrd-$kernel_flavour.img ]; then
	rm -f initrd-$kernel_flavour.img
fi
ln -sf initrd-%{kversion}-$kernel_flavour-%{buildrpmrel}.img initrd-$kernel_flavour.img
popd > /dev/null
%endif
%if %{with devel}
# create kernel-devel symlinks if matching -devel- rpm is installed
if [ -d /usr/src/linux-%{kversion}-$kernel_flavour-%{buildrpmrel} ]; then
	rm -f /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/{build,source}
	ln -sf /usr/src/linux-%{kversion}-$kernel_flavour-%{buildrpmrel} /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/build
	ln -sf /usr/src/linux-%{kversion}-$kernel_flavour-%{buildrpmrel} /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/source
fi
%endif
EOF

### Create kernel Posttrans script
cat > $kernel_files-posttrans <<EOF
if [ -x /usr/sbin/dkms_autoinstaller -a -d /usr/src/linux-%{kversion}-$kernel_flavour-%{buildrpmrel} ]; then
    /usr/sbin/dkms_autoinstaller start %{kversion}-$kernel_flavour-%{buildrpmrel}
fi
EOF

### Create kernel Preun script on the fly
cat > $kernel_files-preun <<EOF
/sbin/installkernel -R %{kversion}-$kernel_flavour-%{buildrpmrel}
pushd /boot > /dev/null
if [ -L vmlinuz-$kernel_flavour ]; then
	if [ "$(readlink vmlinuz-$kernel_flavour)" = "vmlinuz-%{kversion}-$kernel_flavour-%{buildrpmrel}" ]; then
		rm -f vmlinuz-$kernel_flavour
	fi
fi
if [ -L initrd-$kernel_flavour.img ]; then
	if [ "$(readlink initrd-$kernel_flavour.img)" = "initrd-%{kversion}-$kernel_flavour-%{buildrpmrel}.img" ]; then
		rm -f initrd-$kernel_flavour.img
	fi
fi
popd > /dev/null
%if %{with devel}
if [ -L /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/build ]; then
	rm -f /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/build
fi
if [ -L /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/source ]; then
	rm -f /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/source
fi
%endif
exit 0
EOF


### Create kernel Postun script on the fly
cat > $kernel_files-postun <<EOF
/sbin/kernel_remove_initrd %{kversion}-$kernel_flavour-%{buildrpmrel}
rm -rf /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel} >/dev/null
if [ -d /var/lib/dkms ]; then
    rm -f /var/lib/dkms/*/kernel-%{kversion}-$devel_flavour-%{buildrpmrel}-%{_target_cpu} >/dev/null
    rm -rf /var/lib/dkms/*/*/%{kversion}-$devel_flavour-%{buildrpmrel} >/dev/null
    rm -f /var/lib/dkms-binary/*/kernel-%{kversion}-$devel_flavour-%{buildrpmrel}-%{_target_cpu} >/dev/null
    rm -rf /var/lib/dkms-binary/*/*/%{kversion}-$devel_flavour-%{buildrpmrel} >/dev/null
fi
EOF
}


CreateKernel() {
	flavour=$1

	PrepareKernel $flavour $flavour-%{buildrpmrel}

	BuildKernel %{kversion}-$flavour-%{buildrpmrel}
	%if %{with devel}
		SaveDevel $flavour
	%endif
	%if %{with debug}
		SaveDebug $flavour
	%endif
	CreateFiles $flavour
}


###
# DO it...
###


# Create a simulacro of buildroot
rm -rf %{temp_root}
install -d %{temp_root}


# make sure we are in the directory
cd %src_dir

# %{patches_dir}/scripts/apply_patches-vanilla
# %{patches_dir}/scripts/create_configs-vanilla %debug --user_cpu="%{target_arch}"

%{patches_dir}/scripts/apply_patches
%{patches_dir}/scripts/create_configs-old-mdv %debug --user_cpu="%{target_arch}"

%ifarch %{ix86}
%if %{with desktop586}
CreateKernel desktop586
%endif
%endif

%if %{with desktop}
CreateKernel desktop
%endif

%if %{with netbook}
CreateKernel netbook
%endif

%if %{with server}
CreateKernel server
%endif

%ifarch %{ix86}
%if %{with desktop_pae}
CreateKernel desktop-pae
%endif
%endif

%ifarch %{ix86}
%if %{with netbook_pae}
CreateKernel netbook-pae
%endif
%endif

%{patches_dir}/scripts/apply_patches-NRJ
%{patches_dir}/scripts/create_configs-withBFQ %debug --user_cpu="%{target_arch}"

%ifarch %{ix86}
%if %{with nrj_desktop586}
CreateKernel nrj-desktop586
%endif
%endif

%if %{with nrj_desktop}
CreateKernel nrj-desktop
%endif

%if %{with nrj_realtime}
CreateKernel nrj-realtime
%endif

%if %{with nrj_laptop}
CreateKernel nrj-laptop
%endif

%if %{with nrj_netbook}
CreateKernel nrj-netbook
%endif

%ifarch %{ix86}
%if %{with nrj_desktop_pae}
CreateKernel nrj-desktop-pae
%endif
%endif

%ifarch %{ix86}
%if %{with nrj_realtime_pae}
CreateKernel nrj-realtime-pae
%endif
%endif

%ifarch %{ix86}
%if %{with nrj_laptop_pae}
CreateKernel nrj-laptop-pae
%endif
%endif

%ifarch %{ix86}
%if %{with nrj_netbook_pae}
CreateKernel nrj-netbook-pae
%endif
%endif

%ifarch %{ix86}
%if %{with nrj_netbook_atom}
CreateKernel nrj-netbook-atom
%endif
%endif

%ifarch %{ix86}
%if %{with nrj_netbook_atom_pae}
CreateKernel nrj-netbook-atom-pae
%endif
%endif

%ifarch %{ix86}
%if %{with nrj_desktop_core2}
CreateKernel nrj-desktop-core2
%endif
%endif

%ifarch %{ix86}
%if %{with nrj_desktop_core2_pae}
CreateKernel nrj-desktop-core2-pae
%endif
%endif

%ifarch %{arm}
%if %{with iop32x}
CreateKernel iop32x
%endif
%if %{with kirkwood}
CreateKernel kirkwood
%endif
%if %{with versatile}
CreateKernel versatile
%endif
%endif

%{patches_dir}/scripts/apply_patches-QL
%{patches_dir}/scripts/create_configs-QL %debug --user_cpu="%{target_arch}"

%if %{with nrjQL_desktop}
CreateKernel nrjQL-desktop
%endif

%if %{with nrjQL_realtime}
CreateKernel nrjQL-realtime
%endif

%if %{with nrjQL_laptop}
CreateKernel nrjQL-laptop
%endif

%if %{with nrjQL_netbook}
CreateKernel nrjQL-netbook
%endif

%if %{with nrjQL_server}
CreateKernel nrjQL-server
%endif

%if %{with nrjQL_server_computing}
CreateKernel nrjQL-server-computing
%endif

%if %{with nrjQL_server_games}
CreateKernel nrjQL-server-games
%endif

%ifarch %{ix86}
%if %{with nrjQL_desktop_pae}
CreateKernel nrjQL-desktop-pae
%endif
%endif

%ifarch %{ix86}
%if %{with nrjQL_realtime_pae}
CreateKernel nrjQL-realtime-pae
%endif
%endif

%ifarch %{ix86}
%if %{with nrjQL_laptop_pae}
CreateKernel nrjQL-laptop-pae
%endif
%endif

%ifarch %{ix86}
%if %{with nrjQL_netbook_pae}
CreateKernel nrjQL-netbook-pae
%endif
%endif

%ifarch %{ix86}
%if %{with nrjQL_desktop_core2}
CreateKernel nrjQL-desktop-core2
%endif
%endif

%ifarch %{ix86}
%if %{with nrjQL_desktop_core2_pae}
CreateKernel nrjQL-desktop-core2-pae
%endif
%endif


# set extraversion to match srpm to get nice version reported by the tools
LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{rpmrel}/" Makefile


############################################################
### Linker start3 > Check point to build for cooker 2013 ###
############################################################
# build perf

%if %{with perf}
%make -C tools/perf -s HAVE_CPLUS_DEMANGLE=1 prefix=%{_prefix} LDFLAGS="%optflags" all
%make -C tools/perf -s prefix=%{_prefix} LDFLAGS="%optflags" man
%endif

# build cpupower

%if %{with cpupower}
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
%kmake -C tools/power/cpupower CPUFREQ_BENCH=false LDFLAGS="%optflags"
%endif
############################################################
###  Linker end3 > Check point to build for cooker 2013  ###
############################################################


# We don't make to repeat the depend code at the install phase
%if %{with source}
%ifarch %{arm}
    PrepareKernel "kirkwood" %{buildrpmrel}custom
%else
    PrepareKernel "" %{buildrpmrel}custom
%endif
%smake -s mrproper
%endif


###
### install
###
%install
install -m 644 %{SOURCE4}  .

cd %src_dir

# Directories definition needed for installing
%define target_source %{buildroot}%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}

# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %{with source}
install -d %{target_source}

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}

# we remove all the source files that we don't ship
# first architecture files
for i in alpha arc avr32 blackfin c6x cris frv h8300 hexagon ia64 m32r m68k m68knommu metag microblaze \
	 mips openrisc parisc powerpc s390 score sh sh64 sparc tile unicore32 v850 xtensa mn10300; do
	rm -rf %{target_source}/arch/$i
done
%ifnarch %{arm}
	rm -rf %{target_source}/include/kvm/arm*
%endif

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.gitignore,.lst,.mailmap}
rm -f %{target_source}/{.missing-syscalls.d,arch/.gitignore,firmware/.gitignore}
rm -rf %{target_source}/.tmp_depmod/

#endif %{with source}
%endif

# compressing modules
%if %{with modxz}
find %{target_modules} -name "*.ko" | %kxargs xz -6e
%else
find %{target_modules} -name "*.ko" | %kxargs gzip -9
%endif

# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be
for i in %{target_modules}/*; do
	rm -f $i/build $i/source
done

# sniff, if we compressed all the modules, we change the stamp :(
# we really need the depmod -ae here
pushd %{target_modules}
for i in *; do
	/sbin/depmod -ae -b %{buildroot} -F %{target_boot}/System.map-$i $i
	echo $?
done

for i in *; do
	pushd $i
	echo "Creating modules.description for $i"
	modules=`find . -name "*.ko.[g,x]z"`
	echo $modules | %kxargs /sbin/modinfo \
	| perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
	popd
done
popd

# need to set extraversion to match srpm again to avoid rebuild
LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{rpmrel}/" Makefile
%if %{with perf}

# perf tool binary and supporting scripts/binaries
make -C tools/perf -s V=1 DESTDIR=%{buildroot} HAVE_CPLUS_DEMANGLE=1 prefix=%{_prefix} install

# perf man pages (note: implicit rpm magic compresses them later)
make -C tools/perf  -s V=1 DESTDIR=%{buildroot} HAVE_CPLUS_DEMANGLE=1 prefix=%{_prefix} install-man
%endif

############################################################
### Linker start4 > Check point to build for cooker 2013 ###
############################################################
%if %{with cpupower}
%make -C tools/power/cpupower DESTDIR=%{buildroot} libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false LDFLAGS="%optflags" install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE50} %{buildroot}%{_unitdir}/cpupower.service
install -m644 %{SOURCE51} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%endif
############################################################
### Linker start4 > Check point to build for cooker 2013 ###
############################################################

###
### source and doc file lists
###

%if %{with source}
%files -n %{kname}-source-%{buildrel}
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/3rdparty
%{_kerneldir}/Documentation
%{_kerneldir}/arch/Kconfig
%{_kerneldir}/arch/arm
%{_kerneldir}/arch/arm64
%{_kerneldir}/arch/um
%{_kerneldir}/arch/x86
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/firmware
%{_kerneldir}/fs
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
%{_kerneldir}/include/clocksource
%{_kerneldir}/include/crypto
%{_kerneldir}/include/drm
%{_kerneldir}/include/dt-bindings
%{_kerneldir}/include/keys
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/media
%{_kerneldir}/include/memory
%{_kerneldir}/include/misc
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/ras
%{_kerneldir}/include/rdma
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/target
%{_kerneldir}/include/trace
%{_kerneldir}/include/uapi
%{_kerneldir}/include/video
%{_kerneldir}/include/xen
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/virt
%{_kerneldir}/samples
%{_kerneldir}/scripts
%{_kerneldir}/security
%{_kerneldir}/sound
%{_kerneldir}/tools
%{_kerneldir}/usr
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Kbuild
%{_kerneldir}/Kconfig
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
%doc README.kernel-sources

%files -n %{kname}-source-latest
%endif

%if %{with doc}
%files -n %{kname}-doc
%doc linux-%{tar_ver}/Documentation/*
%endif

%if %{with perf}
%files -n perf
%{_bindir}/perf
%dir %{_prefix}/libexec/perf-core
%{_prefix}/libexec/perf-core/*
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%endif

%if %{with cpupower}
%files -n cpupower -f cpupower.lang
%{_bindir}/cpupower
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.0
%{_unitdir}/cpupower.service
%{_mandir}/man[1-8]/cpupower*
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower

%files -n cpupower-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%endif
