# MIB header

%if %{mdvver} <= 201100
%define distsuffix mib
%define disttag %{distsuffix}
Vendor: MIB - Mandriva International Backports
%endif

Packager: Nicolo' Costanza <abitrules@yahoo.it>
# end MIB header

#
%define kernelversion	3
%define patchlevel	13
# sublevel is now used for -stable patches
%define sublevel	11

# Package release
# Experimental kernel serie with CK patches, BFS, BFQ, TOI, UKSM
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

# define rpmtag		%{disttag}
%define rpmtag		%{disttag}
%if %kpatch
%if %kgit
%define rpmrel		%mkrel 0.%{kpatch}.%{kgit}.%{mibrel}
%else
%define rpmrel		%mkrel 0.%{kpatch}.%{mibrel}
%endif
%else
%define rpmrel		69
%endif

# fakerel and fakever never change, they are used to fool
# rpm/urpmi/smart
%define fakever		1
%define fakerel 	%mkrel 1

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
%define buildrpmrel     0.%{kpatch}.%{kgit}.%{rpmrel}%{rpmtag}
%else
%define buildrpmrel     0.%{kpatch}.%{rpmrel}%{rpmtag}
%endif
%else
%define buildrpmrel     %{rpmrel}%{rpmtag}
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
%define build_doc 		1
%define build_source 		1
%define build_devel 		1

%define build_debug 		0

#
# Old Mandriva kernel flavours plus new two PAE flavours
#

#
# MIB experimental low latency optimized flavours
#

# Build nrjQL desktop (i686 / 4GB) / x86_64 / sparc64 sets
%define build_nrjQL_desktop			1

# Build nrjQL realtime (i686 / 4GB) / x86_64 / sparc64 sets
%define build_nrjQL_realtime			0

# Build nrjQL laptop (i686 / 4GB) / x86_64
%define build_nrjQL_laptop			0

# Build nrjQL netbook (i686 / 4GB) / x86_64
%define build_nrjQL_netbook			0

# Build nrjQL_server (i686 / 64GB)/x86_64 / sparc64 sets
%define build_nrjQL_server			0

# Build nrjQL_gameserver (i686 / 64GB)/x86_64 / sparc64 sets
%define build_nrjQL_server_games		0

# Build nrjQL_gameserver (i686 / 64GB)/x86_64 / sparc64 sets
%define build_nrjQL_server_computing		0

#
# MIB experimental low latency optimized flavours with PAE 
#

# Build nrjQL desktop pae (i686 / 64GB)
%ifarch %{ix86}
%define build_nrjQL_desktop_pae			0
%endif

# Build nrjQL realtime pae (i686 / 64GB)
%ifarch %{ix86}
%define build_nrjQL_realtime_pae		0
%endif

# Build nrjQL laptop pae (i686 / 64GB)
%ifarch %{ix86}
%define build_nrjQL_laptop_pae			0
%endif

# Build nrjQL netbook pae (i686 / 64GB)
%ifarch %{ix86}
%define build_nrjQL_netbook_pae			0
%endif

#
# Begin > experimental "cpu level" optimized flavours
#

# Build nrjQL desktop Intel Core2 (mcore2 / 4GB)
%ifarch %{ix86}
%define build_nrjQL_desktop_core2	   	0
%endif

# Build nrjQL desktop Intel Core2 pae (mcore2 / 64GB)
%ifarch %{ix86}
%define build_nrjQL_desktop_core2_pae  	 	0
%endif

#
# End for > experimental "cpu level" optimized flavours
# END OF FLAVOURS


# build perf and cpupower tools
%if %{mdvver} >= 201200
%define build_perf		1
%define build_cpupower		1
%else
%define build_perf		0
%define build_cpupower		0
%endif

# compress modules with xz
%if %{mdvver} >= 201200
%define build_modxz		1
%else
%define build_modxz		0
%endif

# ARM builds
%ifarch %{arm}
%define build_desktop		0
%define build_netbook		0
%define build_server		0
%define build_iop32x		0
%define build_kirkwood		1
%define build_versatile		1
# no cpupower tools on arm yet
%define build_cpupower		0
# arm is currently not using xz
%define build_modxz		0
%endif
# End of user definitions

# buildtime flags
%{?_without_nrjQL_desktop: %global build_nrjQL_desktop 0}
%{?_without_nrjQL_realtime: %global build_nrjQL_realtime 0}

%{?_without_nrjQL_laptop: %global build_nrjQL_laptop 0}
%{?_without_nrjQL_laptop: %global build_nrjQL_netbook 0}

%{?_without_nrjQL_server: %global build_nrjQL_server 0}
%{?_without_nrjQL_gameserver: %global build_nrjQL_server_games 0}
%{?_without_nrjQL_gameserver: %global build_nrjQL_server_computing 0}

%{?_without_nrjQL_desktop_pae: %global build_nrjQL_desktop_pae 0}
%{?_without_nrjQL_desktop_pae: %global build_nrjQL_realtime_pae 0}

%{?_without_nrjQL_laptop_pae: %global build_nrjQL_laptop_pae 0}
%{?_without_nrjQL_laptop_pae: %global build_nrjQL_netbook_pae 0}

%{?_without_nrjQL_desktop_core2: %global build_nrjQL_desktop_core2 0}
%{?_without_nrjQL_desktop_core2_pae: %global build_nrjQL_desktop_core2_pae 0}

%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}
%{?_without_debug: %global build_debug 0}
%{?_without_perf: %global build_perf 0}
%{?_without_cpupower: %global build_cpupower 0}
%{?_without_modxz: %global build_modxz 0}


%{?_with_nrjQL_desktop: %global build_nrjQL_desktop 1}
%{?_with_nrjQL_realtime: %global build_nrjQL_realtime 1}

%{?_with_nrjQL_laptop: %global build_nrjQL_laptop 1}
%{?_with_nrjQL_netbook: %global build_nrjQL_netbook 1}

%{?_with_nrjQL_server: %global build_nrjQL_server 1}
%{?_with_nrjQL_gameserver: %global build_nrjQL_server_games 1}
%{?_with_nrjQL_gameserver: %global build_nrjQL_server_computing 1}

%{?_with_nrjQL_desktop_pae: %global build_nrjQL_desktop_pae 1}
%{?_with_nrjQL_realtime_pae: %global build_nrjQL_realtime_pae 1}

%{?_with_nrjQL_laptop_pae: %global build_nrjQL_laptop_pae 1}
%{?_with_nrjQL_laptop_pae: %global build_nrjQL_netbook_pae 1}

%{?_with_nrjQL_desktop_core2: %global build_nrjQL_desktop_core2 1}
%{?_with_nrjQL_desktop_core2_pae: %global build_nrjQL_desktop_core2_pae 1}

%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_devel: %global build_devel 1}
%{?_with_debug: %global build_debug 1}
%{?_with_perf: %global build_perf 1}
%{?_with_cpupower: %global build_cpupower 1}
%{?_with_modxz: %global build_modxz 1}


# ARM builds
%{?_with_iop32x: %global build_iop32x 1}
%{?_with_kirkwood: %global build_kirkwood 1}
%{?_with_versatile: %global build_versatile 1}
%{?_without_iop32x: %global build_iop32x 0}
%{?_without_kirkwood: %global build_kirkwood 0}
%{?_without_versatile: %global build_versatile 0}

# For the .nosrc.rpm
%define build_nosrc 	0
%{?_with_nosrc: %global build_nosrc 1}


############################################################
### Linker start1 > Check point to build for cooker 2013 ###
############################################################
%if %{mdvver} < 201300
%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make CC="$CC"
%else
%define kmake %make
%endif
# there are places where parallel make don't work
%define smake make
%endif

%if %{mdvver} >= 201300
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
%endif
############################################################
###  Linker end1 > Check point to build for cooker 2013  ###
############################################################


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
Patch1:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.x/testing/patch-%{kernelversion}.%{patchlevel}-%{kpatch}.xz
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

%if %{mdvver} >= 201300
%define requires1	microcode
%define requires2	dracut >= 026
%define requires3	kmod >= 12
%define requires4	sysfsutils >=  2.1.0-12
%define requires5	kernel-firmware >=  20120219-1
%endif

%if %{mdvver} == 201210
%define requires1	bootloader-utils >= 1.15-8
%define requires2	dracut >= 017-16
%define requires3	kmod >= 7-6
%define requires4	sysfsutils >=  2.1.0-12
%define requires5	kernel-firmware >=  20120219-1
%endif

%if %{mdvver} == 201200
%define requires1	bootloader-utils >= 1.15-8
%define requires2	dracut >= 017-16
%define requires3	module-init-tools >= 3.16-5
%define requires4	sysfsutils >=  2.1.0-12
%define requires5	kernel-firmware >=  20120219-1
%endif

%if %{mdvver} < 201200
%define requires1	bootloader-utils >= 1.13-1
%define requires2	mkinitrd >= 4.2.17-31
%define requires3	module-init-tools >= 3.0-7
%define requires4	sysfsutils >= 1.3.0-1
%define requires5	kernel-firmware >= 20101024-2
%endif

%define kprovides1 	%{kname} = %{kverrel}
%define kprovides2 	kernel = %{tar_ver}
%define kprovides3 	alsa = 1.0.27
%define kprovides_server drbd-api = 88

%define	kobsoletes1	dkms-r8192se <= 0019.1207.2010-2
%define	kobsoletes2	dkms-lzma <= 4.43-32
%define	kobsoletes3	dkms-psb <= 4.41.1-7

# conflict dkms packages that dont support kernel-3.10
# all driver versions must be carefully checked to add

# config for all distros apart mdvver == 2013.0 or 2012.1
%define kconflicts1	dkms-broadcom-wl < 5.100.82.112-12
%define kconflicts2	dkms-fglrx < 13.200.5-1
%define kconflicts3	dkms-nvidia-current < 325.15-2
%define kconflicts4	dkms-nvidia-long-lived < 304.88-3
%define kconflicts5	dkms-nvidia173 < 173.14.37-4
# nvidia96xx does not support this kernel or x11-server-1.13

%if %{mdvver} >= 201300
%define kconflicts1	dkms-broadcom-wl < 5.100.82.112-12
%define kconflicts2	dkms-fglrx < 13.200.5-1
%define kconflicts3	dkms-nvidia-current < 325.15-1
%define kconflicts4	dkms-nvidia-long-lived < 319.49-1
%define kconflicts5	dkms-nvidia304 < 304.108-1
# nvidia173 does not support this kernel
# nvidia96xx does not support this kernel or x11-server-1.13
%endif

%if %{mdvver} == 201210
%define kconflicts1	dkms-broadcom-wl < 5.100.82.112-12
%define kconflicts2	dkms-fglrx < 13.200.5-1
%define kconflicts3	dkms-nvidia-current < 325.15-2
%define kconflicts4	dkms-nvidia-long-lived < 304.108-1
%define kconflicts5	dkms-nvidia173 < 173.14.37-4
# nvidia96xx does not support this kernel or x11-server-1.13
%endif

Autoreqprov: 		no

# might be useful too:
Suggests:	microcode

%if %{mdvver} >= 201210
BuildRequires:	kmod-devel kmod-compat 
%else
BuildRequires:	module-init-tools
%endif

BuildRequires: 	gcc bc binutils

BuildRequires:  audit-devel perl-devel

%if %{mdvver} >= 201210
BuildRequires:	libunwind-devel
%endif

%ifarch x86_64
BuildRequires:  numa-devel
%endif

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
Provides:   %{kname}-%{1}               		\
%if %{build_nrjQL_desktop}              		\
Provides:   kernel-desktop              		\
%endif                                  		\
Requires(pre):	%requires1 %requires2 %requires3 %requires4 \
Requires:	%requires2 %requires5 			\
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
%if %build_devel					\
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
%if %build_debug					\
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
%if %build_devel					\
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
%if %build_devel					\
%post -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-post \
%preun -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-preun \
%postun -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-postun \
%endif							\
							\
%files -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1} \
%files -n %{kname}-%{1}-latest				\
							\
%if %build_devel					\
%files -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1} \
%files -n %{kname}-%{1}-devel-latest			\
%endif							\
							\
%if %build_debug					\
%files -n %{kname}-%{1}-%{buildrel}-debuginfo -f kernel_debug_files.%{1} \
%endif

#
# kernel-nrjQL-desktop: nrjQL, i686, smp-alternatives, 4 GB / x86_64
#
%if %build_nrjQL_desktop
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
%if %build_nrjQL_realtime
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
%if %build_nrjQL_laptop
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
%if %build_nrjQL_netbook
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
%if %build_nrjQL_server
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
%if %build_nrjQL_server_computing
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
%if %build_nrjQL_server_games
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
%if %build_nrjQL_desktop_pae
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
%if %build_nrjQL_realtime_pae
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
%if %build_nrjQL_laptop_pae
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
%if %build_nrjQL_netbook_pae
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
%if %build_nrjQL_desktop_core2
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
%if %build_nrjQL_desktop_core2_pae
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
# ARM kernels
#
%ifarch %{arm}
%if %build_iop32x
%define summary_iop32x Linux Kernel for Arm machines based on Xscale IOP32X
%define info_iop32x This kernel is compiled for iop32x boxes. It will run on n2100 \
or ss4000e or sanmina boards.
%mkflavour iop32x
%endif
%if %build_kirkwood
%define summary_kirkwood Linux Kernel for Arm machines based on Kirkwood
%define info_kirkwood This kernel is compiled for kirkwood boxes. It will run on openrd boards.
%mkflavour kirkwood
%endif
%if %build_versatile
%define summary_versatile Linux Kernel for Versatile arm machines
%define info_versatile This kernel is compiled for Versatile boxes. It will run on Qemu for instance.
%mkflavour versatile
%endif
%endif

#
# kernel-source
#
%if %build_source
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
%if %build_doc
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
%if %{build_perf}
%package -n perf
Version:	%{kversion}
Release:	%{rpmrel}
Summary:	perf tool and the supporting documentation
Group:		System/Kernel and hardware

%description -n perf
the perf tool and the supporting documentation.
%endif

%if %{build_cpupower}
%package -n cpupower
Version:	%{kversion}
Release:	%{rpmrel}
Summary:	the cpupower tools
Group:		System/Kernel and hardware
Requires(post):  rpm-helper >= 0.24.0-3
Requires(preun): rpm-helper >= 0.24.0-3
%if %{mdvver} >= 201200
Obsoletes:	cpufreq cpufrequtils
%endif

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
%if %{build_cpupower}
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

%{patches_dir}/scripts/apply_patches
%{patches_dir}/scripts/apply_patches-geek
%{patches_dir}/scripts/apply_patches-latest
%{patches_dir}/scripts/apply_patches-NRJ
%{patches_dir}/scripts/apply_patches-QL
# PATCH END


#
# Setup Begin
#

# Prepare all the variables for calling create_configs

%if %build_debug
%define debug --debug
%else
%define debug --no-debug
%endif


%{patches_dir}/scripts/create_configs-QL %debug --user_cpu="%{target_arch}"

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile

# get rid of unwanted files
find . -name '*~' -o -name '*.orig' -o -name '*.append' | %kxargs rm -f


%build

############################################################
### Linker start2 > Check point to build for cooker 2013 ###
############################################################
%if %{mdvver} >= 201300
# Make sure we don't use gold
export LD="%{_target_platform}-ld.bfd"
export LDFLAGS="--hash-style=sysv --build-id=none"
%endif
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
	# ln -s ../generated/uapi/linux/version.h $TempDevelRoot/include/linux/version.h
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

#3rdparty/vloopback/vloopback.c:179:2: error: #error "need CONFIG_VIDEO_V4L1_COMPAT"
#3rdparty/vloopback/vloopback.c:203:28: fatal error: linux/videodev.h: No such file or directory
#compilation terminated.
#make[2]: *** [3rdparty/vloopback/vloopback.o] Error 1
#make[1]: *** [3rdparty/vloopback] Error 2
#make: *** [3rdparty] Error 2
#make: *** Waiting for unfinished jobs....

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
		rm -rf $TempDevelRoot/arch/arm*
		rm -rf $TempDevelRoot/include/kvm/arm*
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
	patch -p1 --fuzz=0 -d $TempDevelRoot -i %{SOURCE2}

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

%if %build_debug
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
%if %build_devel
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
%if %build_devel
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
	%if %build_devel
		SaveDevel $flavour
	%endif
	%if %build_debug
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

%if %build_nrjQL_desktop
CreateKernel nrjQL-desktop
%endif

%if %build_nrjQL_realtime
CreateKernel nrjQL-realtime
%endif

%if %build_nrjQL_laptop
CreateKernel nrjQL-laptop
%endif

%if %build_nrjQL_netbook
CreateKernel nrjQL-netbook
%endif

%if %build_nrjQL_server
CreateKernel nrjQL-server
%endif

%if %build_nrjQL_server_computing
CreateKernel nrjQL-server-computing
%endif

%if %build_nrjQL_server_games
CreateKernel nrjQL-server-games
%endif

%ifarch %{ix86}
%if %build_nrjQL_desktop_pae
CreateKernel nrjQL-desktop-pae
%endif
%endif

%ifarch %{ix86}
%if %build_nrjQL_realtime_pae
CreateKernel nrjQL-realtime-pae
%endif
%endif

%ifarch %{ix86}
%if %build_nrjQL_laptop_pae
CreateKernel nrjQL-laptop-pae
%endif
%endif

%ifarch %{ix86}
%if %build_nrjQL_netbook_pae
CreateKernel nrjQL-netbook-pae
%endif
%endif

%ifarch %{ix86}
%if %build_nrjQL_desktop_core2
CreateKernel nrjQL-desktop-core2
%endif
%endif

%ifarch %{ix86}
%if %build_nrjQL_desktop_core2_pae
CreateKernel nrjQL-desktop-core2-pae
%endif
%endif


%ifarch %{arm}
%if %build_iop32x
CreateKernel iop32x
%endif
%if %build_kirkwood
CreateKernel kirkwood
%endif
%if %build_versatile
CreateKernel versatile
%endif
%endif

# set extraversion to match srpm to get nice version reported by the tools
LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{rpmrel}/" Makefile


############################################################
### Linker start3 > Check point to build for cooker 2013 ###
############################################################
# build perf

%if %{build_perf}
%if %{mdvver} < 201300
%make -C tools/perf -s HAVE_CPLUS_DEMANGLE=1 prefix=%{_prefix} all
%make -C tools/perf -s prefix=%{_prefix} man
%else
%make -C tools/perf -s HAVE_CPLUS_DEMANGLE=1 prefix=%{_prefix} LDFLAGS="%optflags" all
%make -C tools/perf -s prefix=%{_prefix} LDFLAGS="%optflags" man
%endif
%endif

# build cpupower

%if %{build_cpupower}
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
%if %{mdvver} < 201300
%make -C tools/power/cpupower CPUFREQ_BENCH=false
%else
%kmake -C tools/power/cpupower CPUFREQ_BENCH=false LDFLAGS="%optflags"
%endif
%endif
############################################################
###  Linker end3 > Check point to build for cooker 2013  ###
############################################################


# We don't make to repeat the depend code at the install phase
%if %build_source
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
%if %build_source
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

#endif %build_source
%endif

# compressing modules
%if %{build_modxz}
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

%if %{build_perf}
# perf tool binary and supporting scripts/binaries
make -C tools/perf -s V=1 DESTDIR=%{buildroot} HAVE_CPLUS_DEMANGLE=1 prefix=%{_prefix} install

# perf man pages (note: implicit rpm magic compresses them later)
make -C tools/perf  -s V=1 DESTDIR=%{buildroot} HAVE_CPLUS_DEMANGLE=1 prefix=%{_prefix} install-man
%endif

############################################################
### Linker start4 > Check point to build for cooker 2013 ###
############################################################
%if %{build_cpupower}
%if %{mdvver} < 201300
make -C tools/power/cpupower DESTDIR=%{buildroot} libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
%else
%make -C tools/power/cpupower DESTDIR=%{buildroot} libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false LDFLAGS="%optflags" install
%endif
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
### clean
###
%clean
rm -rf %{buildroot}


# We don't want to remove this, the whole reason of its existence is to be
# able to do several rpm --short-circuit -bi for testing install
# phase without repeating compilation phase
#rm -rf %{temp_root}

###
### source and doc file lists
###

%if %build_source
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

%if %build_doc
%files -n %{kname}-doc
%doc linux-%{tar_ver}/Documentation/*
%endif

%if %{build_perf}
%files -n perf
%{_bindir}/perf
%{_bindir}/trace
%dir %{_prefix}/libexec/perf-core
%{_libdir}/libperf-gtk.so
%{_prefix}/libexec/perf-core/*
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%endif

%if %{build_cpupower}
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


%changelog

* Thu Apr 24 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.13.11-69
+ update to 3.13.11 (EOL) - stable
- update patches:
  * tuxonice-for-linux-3.13.11-2014-04-24.patch
  * uksm-0.1.2.2-for-v3.13.ge.9.patch
- update BFQ to v7r3
  * 0001-block-cgroups-kconfig-build-bits-for-BFQ-v7r3-3.13.patch
  * 0002-block-introduce-the-BFQ-v7r3-I-O-sched-for-3.13.patch
  * 0003-block-bfq-add-Early-Queue-Merge-EQM-to-BFQ-v7r3-for-.patch
- suggestion / request received by Per Øyvind Karlsen (POK)
  * CONFIG_ACPI_CUSTOM_DSDT=y
- ---------------------------------------------------------------------
- Kernel 3.13 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel (-1) (mainline serie), with official kernel sources and addons,
- the rel (-69) will be used for development and experimental flavours,
- instead (-70) is born by the -1 % -69 merge, can generate all flavours
- Yin & Yang (69) release - it's a very complete kernel flavour sets
- ---------------------------------------------------------------------

* Mon Apr 14 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.13.10-69
+ update to 3.13.10 - stable
- on request by Alexander Khryukin: 
  * adding keys requested by Fedya to solve this issue:
  * https://issues.openmandriva.org/show_bug.cgi?id=165
  * http://pastie.org/9079599 > fixed missing features
  * Cgroup sched: missing
  * Cgroup cpu account: missing
  * Cgroup memory controller: missing
- ---------------------------------------------------------------------
- Kernel 3.13 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel (-1) (mainline serie), with official kernel sources and addons,
- the rel (-69) will be used for development and experimental flavours,
- instead (-70) is born by the -1 % -69 merge, can generate all flavours
- Yin & Yang (69) release - it's a very complete kernel flavour sets
- ---------------------------------------------------------------------

* Sun Apr 13 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.13.10-0
+ update to 3.13.10 - rc1
- add: /patches-latest with its script (where are the latest things)
  * criu-no-expert.patch
  * linux-003-no_dev_console.patch
  * linux-004_lower_undefined_mode_timeout.patch
  * linux-006_enable_utf8.patch
  * linux-991.01-ptrace_fix.patch
- ---------------------------------------------------------------------
- Kernel 3.13 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel (-1) (mainline serie), with official kernel sources and addons,
- the rel (-69) will be used for development and experimental flavours,
- instead (-70) is born by the -1 % -69 merge, can generate all flavours
- Yin & Yang (69) release - it's a very complete kernel flavour sets
- ---------------------------------------------------------------------

* Fri Apr 04 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.13.9-69
+ update to 3.13.9 stable
- add: /patches-queue (for tests) and /patches-geek with HW support:
- * DVB cards, IR receivers, WiFi devices, Game controllers, Laptops  
- add: 6 patches to improve NFS behaviour, fixing ops and start time
- add: the 3 patches for Pegatron device driver (offered by Benatto)
- add: new kernel driver modules are enabled, just below the list:
  * CONFIG_DVB_USB_DVBSKY=m
  * CONFIG_HID_SPINELPLUS=m
  * CONFIG_LIRC_XBOX=m 
  * CONFIG_PEGATRON_LAPTOP=m 
- add: patch to fix a disconnection USB problem with some slow USB HW
- suggested by Marco Benatto and was requested by Colin Close (itchka)
  - website: http://marc.info/?l=linux-usb&m=137714769606183&w=2
  * USB:_Fix_USB_device_disconnects_on_resume.patch
- on request by Fedya
  * adding keys requested by Fedya to solve this issue:
  * https://issues.openmandriva.org/show_bug.cgi?id=165
- fix: Benatto sent a working solution for UKSM 3.13 build error 3.13.9
  * 0001-uksm-0.1.2.2-for-v3.13.patch
  * 0002-uksm_change_compound_head_call.patch
-  visual improvements: boot and console appereance changes:
- add: colored printk feature with the default colors for all .configs
  * we must setup our preferred color palette, different than (=0x07)
- add: font-8x16-iso-latin-1-v3.patch
  * this shows the boot with more readable fonts, with a more dense look
- ---------------------------------------------------------------------
- Kernel 3.13 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel (-1) (mainline serie), with official kernel sources and addons,
- the rel (-69) will be used for development and experimental flavours,
- instead (-70) is born by the -1 % -69 merge, can generate all flavours
- Yin & Yang (69) release - it's a very complete kernel flavour sets
- ---------------------------------------------------------------------

* Mon Mar 31 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.13.8-69
+ update to 3.13.8 stable
- sync patches
- ---------------------------------------------------------------------
- Kernel 3.13 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel (-1) (mainline serie), with official kernel sources and addons,
- the rel (-69) will be used for development and experimental flavours,
- instead (-70) is born by the -1 % -69 merge, can generate all flavours
- Yin & Yang (69) release - it's a very complete kernel flavour sets
- ---------------------------------------------------------------------

* Fri Mar 28 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.13.7-69
+ update to 3.13.7 stable
- sync with few nrjQL patches
- sync all the patches for 3.13.8 (rc1)
- add REISER4 (file system) support, with two new patches:
  * 0004-reiser4-for-3.13.6.patch
  * 0005-3.13.1-reiser4-different-transaction-models.patch
- ---------------------------------------------------------------------
- Kernel 3.13 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel (-1) (mainline serie), with official kernel sources and addons,
- the rel (-69) will be used for development and experimental flavours,
- instead (-70) is born by the -1 % -69 merge, can generate all flavours
- Yin & Yang (69) release - it's a very complete kernel flavour sets
- ---------------------------------------------------------------------

* Mon Mar 10 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.13.6-69
+ update to 3.13.6 stable
+ this is first version of "nrj" stable 3.13.x, in its early development
- stage, so, it's only for testing purposes, please, dont use this srpm,
- because is still to fix all over!!!
- all the defconfigs have been prepared for the 3.13 series
- all the patches have been added for the 3.13 series
- all the create_configs scripts have been updated to v.2.1
- all the kernel specs have been updated to the 3.13 series
- ---------------------------------------------------------------------
- Kernel 3.13 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel (-1) (mainline serie), with official kernel sources and addons,
- the rel (-69) will be used for development and experimental flavours,
- instead (-70) is born by the -1 % -69 merge, can generate all flavours
- Yin & Yang (69) release - it's a very complete kernel flavour sets
- ---------------------------------------------------------------------

* Sun Feb 23 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.13-69
+ kernel 3.12.13 stable
- drop 2 patches, already in mainstream:
  * x86-xen-mmu-fix-NUMA-crash.patch
  * revert-usbcore-set-lpm_capable-field-for-lpm-capable-root-hubs.patch
- small fixes and cleanups
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel (-1) (mainline serie), with official kernel sources and addons,
- the rel (-69) will be used for development and experimental flavours,
- instead (-70) is born by the -1 % -69 merge, can generate all flavours
- Yin & Yang (69) release - it's a very complete kernel flavour sets
- ---------------------------------------------------------------------

* Fri Feb 21 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.12-69
+ kernel 3.12.12 stable
- add: libunwind-devel as BR for %mdvver >= 201210 (ROSA 2012.1)
- change ftp://ftp.kernel.org patch format from .bz2 to .xz
- update: tuxonice-for-linux-3.12.12-2014-02-21.patch
- small fixes and cleanups
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel (-1) (mainline serie), with official kernel sources and addons,
- the rel (-69) will be used for development and experimental flavours,
- instead (-70) is born by the -1 % -69 merge, can generate all flavours
- Yin & Yang (69) release - it's a very complete kernel flavour sets
- ---------------------------------------------------------------------

* Sat Feb 15 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.11-69
+ kernel 3.12.11 stable
- add: H930C-part1.patch, H930C-part2.patch, H930C-part3.patch
- add: kernel-3.11.8-i915-quirk-acer-aspire-v3-772g.patch
- drop: 2 drm patches, already in mainstream
- update: BFQ (disk I/O scheduler) from v7r1 to v7r2
- update: tuxonice-for-linux-3.12.11-2014-02-15.patch
- update: linux-saa716x_PCIe_interface_chipset.patch
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Feb 11 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.10-69
+ kernel 3.12.10 stable
- update BFQ (disk I/O scheduler) to v7r1
- enable the key: CONFIG_DRM_RADEON_UMS=y
- drop 12 patches, already in mainstream
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Feb 04 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.9-69v7
+ this is only a fix release replacement - not changed release nr.
- create_configs > enabled NAMESPACES & UIDGID_STRICT_TYPE_CHECKS
- this release has new BFQv7 enabled, prepared for testing purposes
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Feb 04 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.9-69
+ this is only a fix release replacement - not changed release nr.
- create_configs > enabled NAMESPACES & UIDGID_STRICT_TYPE_CHECKS
- this release has BFQv6r2, not the newest BFQv7, better waiting...
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Feb 02 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.9-69v7
+ kernel 3.12.9 stable
- this is the first testing version with new BFQv7 disk I/O scheduler
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu Jan 30 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.9-69
+ update to 3.12.9 stable
- small fixes and cleanups:
- removed all the remaining warning msgs from create_configs:
- fixed .defconfigs (arm.config, i386.config, x86_64.config)
 - satisfied all build CHK (audit, numa and unwind): 
- BuildRequires: audit-devel numa-devel unwind-devel
- sync & add new patches
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Jan 26 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.8-69
+ update to 3.12.8 stable
- sync & add new patches
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Mon Jan 13 2014 Nicolo' Costanza <abitrules@yahoo.it> 3.12.7-69
+ update to 3.12.7 stable
- sync & add new patches
- drop 3rdparty heci driver (obsoleted by in-kernel mei driver)
- switch to percpu squashfs multi-decompressor on i586 & x86_64
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Dec 31 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.12.6-69
+ update to 3.12.6 stable
- add fix to properly rebuild the modules for latest VMware products 
- add patch: reiser4-for-3.12.6.patch
- add fix to all kernel.spec for a proper "cooker" rebuild 
- drop a workaround introduced since 3.7.9-1 to fix issues with dkms: 
- # /linux/version.h symlink to /include/generated/uapi/linux/version.h
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Dec 20 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.12.5-69
+ update to 3.12.5 stable
+ this is first version of "nrj" stable 3.12.x, in its early development
- stage, so, it's only for testing purposes, please, dont use this srpm,
- because is still to fix all over!!!
-
- hoping there will follow many other kernels developed by me...
-
- all the defconfigs have been prepared for the 3.12 series
- all the patches have been added for the 3.12 series
- all the create_configs scripts have been updated to v.2.0
- all the kernel specs have been updated to the 3.12 series
- ---------------------------------------------------------------------
- Kernel 3.12 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Dec 01 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.11.10-69
- Virtual package for new nrj kernel for properly install and updates.
+ update to 3.11.10 stable
- http://lwn.net/Articles/575269/ > This is EOL for 3.11
- * 44 files changed, 395 insertions(+), 195 deletions(-)
- update: /patches-QL/tuxonice-for-linux-3.11.10-2013-11-30.patch
- small fixes and cleanups
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu Nov 28 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.11.9-69
+ update to 3.11.9 stable
- revert latest EFI changes
  * CONFIG_EFIVAR_FS set to m
  * CONFIG_EFI_VARS set to y
- update: /patches-QL/tuxonice-for-linux-3.11.9-2013-11-22.patch
- ---------------------------------------------------------------------
- Kernel 3.11 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- --------------------------------------------------------------------

* Sat Nov 16 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.11.8-69
+ update to 3.11.8 stable 
- update: /patches-QL/tuxonice-for-linux-3.11.8-2013-11-15.patch
- Thanks to Eugene Shatokhin we have a modified BFS patch compatible with
- the ondemand speed-up patch, so also nrjQL should perform even better...
- ---------------------------------------------------------------------
- Kernel 3.11 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- --------------------------------------------------------------------

* Sun Nov 10 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.11.7-69
+ update to 3.11.7 stable plus all the patches from the 3.11.8-rc1
- update: /patches-QL/uksm-0.1.2.2-for-v3.11.ge.7.patch
- ---------------------------------------------------------------------
- Kernel 3.11 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- --------------------------------------------------------------------

* Thu Nov 07 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.11.7-69
+ update to 3.11.7 stable
- update: /patches-QL/tuxonice-for-linux-3.11.7-2013-11-07.patch
- add 'on request' by Eugene Shatokhin, few MEI changes to avoid too many error logs wasting space
  * CONFIG_INTEL_MEI from "=y" to "=m"
  * CONFIG_INTEL_MEI_ME from "=y" to "=m"
- add 'on request' by Alexander Burmashev: CONFIG_DRM_LOAD_EDID_FIRMWARE=y
  * with this we should be able to override the wrong EDID of displays with options at kernel boot
  * About EDID override howto, you read here:
  * https://www.osadl.org/monitoring/patches/r2s0/drivers-gpu-drm-allow-to-load-edid-firmware.patch
- add 'on request' by Alexander Kazancev the full configs for UEFI from: 
  * https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface#Linux_Kernel_Config_options_for_UEFI
  * add CONFIG_RELOCATABLE=y also for i386.config
  * change CONFIG_EFIVAR_FS from "=m" to "=y"
  * change CONFIG_EFI_VARS from "=y" to "=n"
- add a patch to speed-up nuveau / radeon timers improvments for (from an 3.12 idea),
- it was addded patches-NRJ-only, /scripts/apply_patches-NRJ-only, and a spec modify
  * openSUSE 13.1 RC2 Updates Systemd, Has Speedy Fix:
  * http://www.phoronix.com/scan.php?page=news_item&px=MTQ5OTc
  * Here's Why Radeon Graphics Are Faster On Linux 3.12:
  * http://www.phoronix.com/scan.php?page=article&item=linux_312_performance&num=1
- ---------------------------------------------------------------------
- Kernel 3.11 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- --------------------------------------------------------------------

* Sat Oct 19 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.11.6-69
+ update to 3.11.6 stable
- add 'on request' by 'Bero' aka Bernhard Rosenkränzer:
  * add: linux-3.11.4-saa716x.patch > driver for SAA7160 based DVB cards
  * add: to the /configs/*.config the proper keys for the SAA7160 driver
- add 3.11-haswell-intel_pstate.patch > to support P-state in new Haswell
- add 'on request' by Eugene Shatokhin: if debug > DEBUG_INFO_REDUCED=y
- add /specs folder with 4 kernel.spec, so you can use any other .specs
- drop to cleanups two old and really not used patches:
  * /patches-NRJ/kernel-inittmpfs.patch
  * /patches-NRJ/vhba-3.8-20130427.patch
- update: tuxonice-for-linux-3.11.6-2013-10-19.patch
- fix: missing XEN configs to all the -server flavours with config_xen();
- small fixes and aestetic cleanups to all the create_configs-* /scripts
- ---------------------------------------------------------------------
- Kernel 3.11 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- --------------------------------------------------------------------

* Wed Oct 09 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.11.4-69
+ update to 3.11.4 stable
- update: tuxonice-for-linux-3.11.4-2013-10-06.patch
- remove: patches-others, patches-extras folders as now are patches-NRJ
- remove: /scripts/apply_patches-extras, /scripts/apply_patches-others
- change: kernel.spec now apply_patches-NRJ instead then extras, others
- ---------------------------------------------------------------------
- Kernel 3.11 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- --------------------------------------------------------------------

* Sun Oct 06 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.11.1-69
+ this is first version of nrjQL stable 3.11.1, in its early development
- stage, so, it's only for testing purposes, please, dont use this srpm,
- because is still to fix all over!!!
+ update to 3.11.1 stable
- defconfigs: have been prepared for 3.11 series
- patches: have been updated for the 3.11 series
- specs: some needed updates to nrj, nrjQL, ONE
- ---------------------------------------------------------------------
- Kernel 3.11 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sat Oct 05 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.15-69
+ update to 3.10.15 stable
- sync: /patches
- modified defconfigs for:
 * # CONFIG_FW_LOADER_USER_HELPER is not set
 * # CONFIG_X86_GOLDFISH is not set
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Oct 01 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.14-69
+ update to 3.10.14 stable
- drop: fbcondecor.patch from /patches-others and /patches-NRJ (one)
- changes in defconfigs:
- drop config for CONFIG_FB_CON_DECOR
- recover to CONFIG_FB_TILEBLITTING=y
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Sep 27 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.13-69
+ update to 3.10.13 stable
- update patch
- * /patches-QL/tuxonice-for-linux-3.10.13-2013-09-27.patch
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Mon Sep 16 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.12-69
+ update to 3.10.12 stable
- add patch
- * linux-fixuClibc.patch
- (it was recommended by Alexander Burmashev: uclibc builds on kernel 3.10
- we have a lot of such stuff in cooker, especially recommended for cooker)
- drop patches from previous 3.0.11 (these are already applied in 3.10.12):
  * net-sched-psched_ratecfg_precompute-improvements.patch
  * net-sched-restore-linklayer-atm-handling.patch
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Sep 10 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.11-69
+ update to 3.10.11 stable
- the compressed folder now is the same (mibrel 69) for -1/-69/-70(one) 
- sync: new /patches:
  * /patches-QL/tuxonice-for-linux-3.10.11-2013-09-10.patch
- drop old 3.10.10 patches (these are already applied in 3.10.11):
  * kernel-workqueue-cond_resched-after-processing-each-work-item.patch
  * jfs-fix-readdir-cookie-incompatibility-with-nfsv4.patch
  * drm-nouveau-mc-fix-race-condition-between-constructor-and-request_irq.patch
  * net-wireless-ath-ath9k-Enable-PLL-fix-only-for-AR9340-AR9330.patch
  * net-mac80211-add-a-flag-to-indicate-CCK-support-for-HT-clients.patch
  * net-sunrpc-Fix-memory-corruption-issue-on-32-bit-highmem-systems.patch
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- the rel -69  is used for development and the experimental flavours,
- the rel -70 is merge of mainline & experimental flavours in ONE srpm
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Sep 01 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.10-69
+ update to 3.10.10 stable
- BFQ: replaced with fixed version (nr.3 patches 3.10.8+-v6r2/ dated 25 August)
- sync: /patches
- updates: /patches-others /patches-NRJ /patches-QL /patches-RT
- modified all defconfigs, enabled: CONFIG_CHECKPOINT_RESTORE=y
- modified create_configs (all -server flavours: compression from XZ to GZIP)
- fixed Kconflicts for all distro or almost (hoping...)
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu Aug 22 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.9-69
- replacement 3.10.9 release
- To fix the "hangs on boot issue" signaled: bugs.rosalinux.ru/show_bug.cgi?id=2530
- add: /patches-NRJ/0004-block-Switch-from-BFQ-v6r2-for-3.10.0-to-BFQ-v6r2-fo.patch
- sync: /patches
- update: /patches-QL/tuxonice-for-linux-3.10.9-2013-08-21.patch
- fix conflicts as suggested by Tomasz ﻿Paweł﻿ Gajc: dkms-nvidia-current < 325.15-1
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Aug 21 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.9-69
+ update to 3.10.9 stable
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Aug 20 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.8-69
+ update to 3.10.8 stable
- sync and update few patches
- the compressed folder has redundant contents to be used for NRJ4/NRJ5:
- the same folder can be used with kernel.spec for new Kernels ONE model
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu Aug 15 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.7-69
+ update to 3.10.7 stable
- sync patches, drop old stable queue, drm-radeon and zram patches
- fixed the Conflicts: dkms-broadcom-wl < 5.100.82.112-12
- fixed create_configs (ver 1.8) - removed question when -netbook +pae
  * modified from: $values{XEN} = "n"; >>> to >>> $to_add{XEN} = "n";
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Aug 13 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.6-69
+ update to 3.10.6 stable
- sync all /patches
- update QL patch: tuxonice-for-linux-3.10.6-2013-08-13.patch
- fixed Conflicts with new proprietary driver version-release
- fixed Provides value for Alsa
- small fix to .spec for %files headers section
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Aug 07 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.5-69
+ update to 3.10.5 stable
- sync all /patches
- sync defconfigs
- enable ndiswrapper
- update QL patch: tuxonice-for-linux-3.10.5-2013-08-04.patch
- revert to power save disable to verify if fixes an issue of audio noise:
- (that issue has been firstly reported by "dago68", then verified by me)
  * CONFIG_SND_HDA_POWER_SAVE_DEFAULT=0
  * CONFIG_SND_AC97_POWER_SAVE_DEFAULT=0
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Aug 07 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.5-69
+ update to 3.10.5 stable
- sync all /patches
- sync defconfigs
- enable ndiswrapper
- update QL patch: tuxonice-for-linux-3.10.5-2013-08-04.patch
- revert to power save disable to verify if fixes an issue of audio noise:
- (that issue has been firstly reported by "dago68", then verified by me)
  * CONFIG_SND_HDA_POWER_SAVE_DEFAULT=0
  * CONFIG_SND_AC97_POWER_SAVE_DEFAULT=0
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu Aug 01 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.4-69
+ update to 3.10.4 stable
- revert to old /scripts/create_configs-QL behaviour:
  * now -laptop and -netbook are 300 and 250HZ again
- sync /patches
- update patch: tuxonice-for-linux-3.10.4-2013-07-30.patch
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Jul 30 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.1-69
+ update to 3.10.1 stable
- all the defconfigs have been prepared for 3.10 series
- all the patches have been updated for the 3.10 series
- update kernel specs
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Jul 26 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.10.1-69
+ this is first version of nrjQL stable 3.10.1, in its early development
- stage, so, it's only for testing purposes, please, dont use this srpm,
- because is still to fix all over!!!
- ---------------------------------------------------------------------
- Kernel 3.10 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Jul 23 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.9.11-69
+ update to stable 3.9.11 (EOL)
- update patches:
  * tuxonice-for-linux-3.9.11-2013-07-21.patch
- update defconfigs
- ---------------------------------------------------------------------
- Kernel 3.9 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Jul 17 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.9.10-69
+ update to 3.9.10 stable
- update patches:
  * tuxonice-for-linux-3.9.10-2013-07-14.patch
  * uksm-0.1.2.2-for-v3.9.ge.8.patch
- update defconfigs
- ---------------------------------------------------------------------
- Kernel 3.9 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Jul 05 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.9.9-69
+ update to 3.9.9 stable
- update patch: tuxonice-for-linux-3.9-8-2013-06-29.patch
- added patch: net-wireless-bcma-add-support-for-BCM43142.patch
- ---------------------------------------------------------------------
- Kernel 3.9 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu Jun 27 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.9.8-69
+ update to 3.9.8 stable
- update patch: tuxonice-for-linux-3.9-7-2013-06-23.patch
- add patch: ath9k_htc > Handle IDLE state transition properly
- removed unused config keys: ATH9K_RATE_CONTROL=y & USB_CHIPIDEA_HOST=y
- ---------------------------------------------------------------------
- Kernel 3.9 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu Jun 20 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.9.7-69
+ update to 3.9.7 stable
- fixed a shutdown issue reported on nrjQL laptop -netbook and -server 
- now BFQ is the version updated to v6r2, dated 15 June
- replaced 3 patches:
  * 0001-block-cgroups-kconfig-build-bits-for-BFQ-v6r2-3.8.patch
  * 0002-block-introduce-the-BFQ-v6r2-I-O-sched-for-3.8.patch
  * 0003-block-bfq-add-Early-Queue-Merge-EQM-to-BFQ-v6r2-for-3.8.0.patch
- new key since 3.9.7 >>> # CONFIG_ATH9K_LEGACY_RATE_CONTROL is not set
- ---------------------------------------------------------------------
- Kernel 3.9 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sat Jun 15 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.9.6-69
+ update to 3.9.6 stable
- update TOI patch >>> tuxonice-for-linux-3.9-6-2013-06-15.patch
- update all defconfigs: insert the new key values in the proper places
- update kernel.spec about text descriptions for nrj and nrjQL flavours
- small overall cleanups
- ---------------------------------------------------------------------
- Kernel 3.9 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Jun 12 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.9.5-69
+ update to 3.9.5 stable
- update TOI patch >>> tuxonice-for-linux-3.9-5-2013-06-08.patch
- ---------------------------------------------------------------------
- Kernel 3.9 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Jun 11 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.9.1-69
+ update to 3.9.1 stable
- all the defconfigs have been prepared for 3.9 series
- all the patches have been updated for the 3.9 series
- update kernel specs
- update kernel scripts
- on mainline nrj kernels we apply again > create_configs-withBFQ
- we've received some good suggestions, and all have been accepted
- 1> suggestions and requests received by Per Øyvind Karlsen (POK)
  * TOI (tuxonice) was only in laptop/netbook, now in all flavours
  * CONFIG_PM_AUTOSLEEP=y 
  * CONFIG_SFI =m
  * CONFIG_BLK_DEV_DRBD=m 
  * # CONFIG_DRBD_FAULT_INJECTION is not set
  * CONFIG_HW_RANDOM_TIMERIOMEM=m 
  * CONFIG_DRM_VIA=m 
  * CONFIG_FB_ATY128_BACKLIGHT=y  
  * CONFIG_USB_RIO500=m 
  * CONFIG_DRM_VMWGFX_FBCON=y
  * CONFIG_SND_PCSP=m 
  * CONFIG_SND_HDA_POWER_SAVE_DEFAULT=10
  * CONFIG_SND_AC97_POWER_SAVE_DEFAULT=10
- 2> suggestions from an advanced user to A.Burmashev
  * CONFIG_TCP_CONG_ADVANCED=y
  * CONFIG_TCP_CONG_BIC=m
  * CONFIG_TCP_CONG_CUBIC=y
  * CONFIG_TCP_CONG_WESTWOOD=m
  * CONFIG_TCP_CONG_HTCP=m
  * CONFIG_TCP_CONG_HSTCP=m
  * CONFIG_TCP_CONG_HYBLA=m
  * CONFIG_TCP_CONG_VEGAS=m
  * CONFIG_TCP_CONG_SCALABLE=m
  * CONFIG_TCP_CONG_LP=m
  * CONFIG_TCP_CONG_VENO=m
  * CONFIG_TCP_CONG_YEAH=m
  * CONFIG_TCP_CONG_ILLINOIS=m
  * CONFIG_DEFAULT_CUBIC=y
  * # CONFIG_DEFAULT_RENO is not set
- ---------------------------------------------------------------------
- Kernel 3.9 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri May 17 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.13-69
+ update to 3.8.13 stable (EOL)
- * 87 files changed, 902 insertions(+), 445 deletions(-)
- patches updated
- two kernel keys have been modified:
- * CONFIG_NLS_DEFAULT="iso8859-1" to CONFIG_NLS_DEFAULT="utf8"
- * new add > CONFIG_MOUSE_CYAPA=m
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu May 16 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.12-69.2
+ update to 3.8.12 stable - second release
- BFQ patches update to v6r1 that contain two important fixes.
- BFQ is disable on mainline kernels (nrj), as v6 caused some rare oops:
- but you can still enable it easily from kernel.spec using the command 
- create_configs-withBFQ instead of create_configs (one of 2 must be #)
- BFQ is enable on development kernels nrjQL, but now is the fixed v6r1
- ZSwap patch dropped, as it caused some rare oops...
- ZSMALLOC is now built-in on arm to workaround a build failure
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu May 09 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.12-69
+ update to 3.8.12 stable 
- * 129 files changed, 641 insertions(+), 320 deletions(-)
- patches dropped, now in upstream
- patches updated to newer versions
- * tuxonice 3.8.12 20130509
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue May 07 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.11-69
+ update to 3.8.11 stable 
- * 49 files changed, 454 insertions(+), 166 deletions(-)
- patches dropped, now in upstream
- patches updated to newer versions
- * aufs3 3.8 20130504
- * tuxonice 3.8.11 20130504
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sat Apr 27 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.10-69
+ update to 3.8.10 stable 
- * 58 files changed, 405 insertions(+), 222 deletions(-)
- * 3 files changed, 27 insertions(+), 1 deletion(-)
- patches updated to newer versions dated 20130427:
  * aufs3, fbcondor, ureadahead, toi, vhba, zwap 
- patch add: try removing a boot warning about kernelvariables
  * /patches-extras/kernelvariables.patch
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Apr 17 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.8-69
+ update to 3.8.8 stable 
- *  37 files changed, 335 insertions(+), 344 deletions(-)
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Mon Apr 15 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.7-69
+ update to 3.8.7 stable 
- * 67 files changed, 507 insertions(+), 341 deletions(-)
- new patches added, enabled and configured with default values
  * /patches-extras/linux-3.8.6-colored-printk.patch
  * /patches-extras/zswap-3.8-20130415.patch
  * zswap now is enabled only on x86 arch, not in ARM (using zcache2)
- patches updated to newer versions 20130414:
  * aufs3, toi 
- patches updated to newer versions 20130415:
  * fbcondor, ureadahead, vhba
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Apr 07 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.6-69
+ update to 3.8.6 stable 
- * (158 files changed, 1341 insertions(+), 658 deletions(-)
- patch add: reiserfs4 ver.3.8 with its configuration as new module
  * add an experimental support to Reiser4 FS: please test this FS!
- patches updated to newer git version 20130406:
  * aufs3, brtfs-lz4, fbcondor, toi, ureadahead, vhba
- Some kernel.spec changes from cooker to make it ARM/ARM64 compatible:
  * Import Bero commit 0e1b905e24 from openmandriva cooker kernel.spec
  * Import Fedya commit 4254d039f6 from openmandriva cooker kernel.spec
- add conflict for dkms-nvidia173 <= 173.14.36
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Thu Mar 28 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.5-69
+ update to 3.8.5 stable 
- * (109 files changed, 778 insertions(+), 683 deletions(-)
- add two new keys to defconfigs:
  * CONFIG_EFI_VARS_PSTORE=y
  * # CONFIG_EFI_VARS_PSTORE_DEFAULT_DISABLE is not set
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Mar 24 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.4-69
+ update to 3.8.4 stable (86 fixes all over)
+ NRJ 4, scripts v 1.6: more info on file > create_configs_changelog
+ Import Bero commit 32d3796b8b from openmandriva cooker kernel.spec
- patches updated:
  * AUFS3 to 3.8 20130324
  * TOI to 3.8.3 20130324
- patches added:
  * uksm-0.1.2.2-for-v3.8.ge.3.patch
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Mar 15 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.3-69
+ update to 3.8.3 stable (144 fixes all over)
+ Imported "Build kernel-headers in here" from OpenMandriva kernel
- drop Haswell id fixup: gpu-drm-i915-Fix-Haswell-CRW-PCI-IDs.patch
+ patches new entries are placed in /extras folder:
- kernel-esfq.patch
- kernel-inittmpfs.patch
- btrfs-lz4-3.8-20130314.patch
- ureadahead-3.8-20130314.patch
+ patches updated:
- AUFS3 to 3.8 20130315
- TOI to 3.8.3 20130315
- VHBA 3.8 20130314
+ NRJ 4, scripts v 1.5: 
- nrjQL_server & nrjQL_server_computing: dynticks enabled to save energy 
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Mon Mar 11 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.2-69
+ update to 3.8.2 stable (80 fixes all over)
+ Patch added from ZEN:
- Virtual (SCSI) HBA for Virtual CD emulation module
+ update to the patches:
- AUFS3 to 3.8 20130310
- TOI to 3.8.2 20130310
+ some spec cleanup for cooker
+ defconfigs updated for VHBA, enable for x86/x86_64, disable for ARM
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Mar 10 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.8.1-69
+ update to 3.8.1 stable 
+ update to nrj v4 - rel 1.4 (09 mar 2013) 
- This version is first attempt to merge stuff with OpenMandriva devel:
- it should build from mdv2010/2011, rosa2012.0/2012.1, and cooker 2013
- ---------------------------------------------------------------------
- Kernel 3.8 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Mar 03 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.7.10-69
+ update to 3.7.10 stable (79 fixes all over)
- With this version, 3.7 has reached the EOL status (End of Life)
+ update to nrj v4 - rel 1.3 (05 mar 2013) 
- On request of Alexander Khryukin, fixed configs and scripts for ARM:
- fixed configs, removed all warnings, enabled again all arm defconfigs
- defconfigs for kirkwood, versatile, iop32x have BFQ enable by default
- ---------------------------------------------------------------------
- Kernel 3.7 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Feb 20 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.7.9-69
+ update to 3.7.9 stable (12 fixes all over)
- update AUFS3 to 3.7.9 20130218
- specific for nrjQL addons:
- update tuxonice 3.7.9 20130218
- add a workaround to fix issue with dkms drivers for recent distros:
- /linux/version.h symlink to /include/generated/uapi/linux/version.h
- ---------------------------------------------------------------------
- Kernel 3.7 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sat Feb 16 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.7.8-69
+ update to 3.7.8 stable (69 fixes all over)
- update AUFS3 to 3.7 20130215
- specific for nrjQL addons:
- update tuxonice 3.7.8 20130215
- updated scripts:
- all nrj flavours use BFQ v6 (disk I/O) enabled by default
- all nrj laptop flavours since now use the full preemption 
- ---------------------------------------------------------------------
- Kernel 3.7 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Feb 13 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.7.7-69
+ update to 3.7.7 stable (34 fixes all over)
- update AUFS3 to 3.7 20130212
- specific for nrjQL addons:
- update BFQ v6 I-O-sched for-3.7
- update tuxonice 3.7.7 20130212
- remove microcode from "requires", now it's in "suggests"
- ---------------------------------------------------------------------
- Kernel 3.7 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Mon Feb 04 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.7.6-69
+ update to 3.7.6 stable (101 fixes all over)
- add "# CONFIG_NETFILTER_XT_TARGET_NOTRACK is not set" to defconfigs
- ---------------------------------------------------------------------
- Kernel 3.7 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours,
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sat Feb 02 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.7.5-69
+ update to 3.7.5 stable
- drop two staging patches
- ---------------------------------------------------------------------
- Kernel 3.7 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sat Feb 02 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.7.1-69
+ update to 3.7.1 stable
- update kernel.spec to be complaint with new V4 nrj/nrjQL model 
- update all scripts to be complaint with new V4 nrj/nrjQL model
- merged defconfigs for nrj & nrjQL, source folders and contents have been unified
- merged all changelogs, as now nrj and nrjQL will be developed in perfect sync
- applied all ROSA customizations of defconfigs as requested by Alexander Burmashev
- update AUFS3 to 3.7 20130128
- update 4200_fbcondecor-0.9.6
- add 08-18-brcmsmac-Add-support-for-writing-debug-messages-to-the-trace-buffer.patch
- specific for nrjQL addons:
- update BFQ v5r1 I-O-sched for-3.7
- update ck1 3.7 and bfs426-427
- update tuxonice 3.7.5 20130128
- update uksm 0.1.2.2 for v3.7.ge.1
- ---------------------------------------------------------------------
- Kernel 3.7 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Mon Jan 14 2013 Nicolo' Costanza <abitrules@yahoo.it> 3.6.11-69
+ update to 3.6.11 stable (56 fixes all over)
- update BFQ version to v5r1
- update UKMS version to 0.1.2.2
- add brcmsmac-Add-support-for-writing-debug-messages-to-the-trace-buffer.patch
- add i915.CADLinopregion.patch
- changed power profile for nrjQL-desktop from PERFORMANCE to ONDEMAND
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Dec 12 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.10-69
+ update to 3.6.10 stable (29 fixes all over)
- update AUFS3 version to git 20121207
- update T.O.I version to gif 20121207
- add speakup-lower-default-software-speech-rate.patch
- ROSA 2012.1 release version 
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Nov 30 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.9-rc1-69
+ update to 3.6.9-rc1-69 (56 fixes all over)
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Nov 30 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.8-69
+ update to 3.6.8-69 (96 fixes all over)
- add 6 patches AUFS3 with the MagOS config keys
- add 12 patches to ext4 from Fedora 3.6
- update AUFS3 to git version 20121127
- update TOI to 20121127 git version
- add 4200_fbcondecor-0.9.6.patch
- add config key CONFIG_FB_CON_DECOR=y, changed FB_TILEBLITTING=n
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Nov 20 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.7-69
+ update to 3.6.7-69 (89 fixes all over)
- updated all patches for kernel 3.6.7: AUFS3, OverlayFS, TOI
- modified freq. for nrjQL-desktop from HZ=1500 to 2000 to comply VBox
- re-add cpufreq_ondemand_performance_optimise_default_settings.patch
- drop nrjQL-desktop-vm - experimentally tuned for virtual machines
- now nrjQL-desktop has been fine tuned also for VM and is good enough
- small modifies and fixes to "create_configs" and "kernel.spec" files
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Wed Nov 07 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.6-69.2
+ update to 3.6.6-69.2
- modified freq. for nrjQL-desktop from 1500 to 2000 to test VBox
- drop cpufreq_ondemand_performance_optimise_default_settings.patch
- to test if removing this patch the p4-clockmod can works again...
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Mon Nov 05 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.6-69
+ update to 3.6.6-69
- drop FX01_fs-ext4-fix-unjournaled-inode-bitmap-modification.patch,
- because that's already inside patch-3.6.6.bz2
- modify configuration for -server flavour to DEFAULT_GOV_ONDEMAND=y
- add nrjQL-desktop-vm - experimentally tuned for virtual machines
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Nov 02 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.5-69
+ update to 3.6.5-69
- updated QL patches
- add FX01_fs-ext4-fix-unjournaled-inode-bitmap-modification.patch
- drop FX01_fix-serious-progressive-ext4-data-corruption-bug.patch
- add video4linux vloopback support
- http://www.lavrsen.dk/foswiki/bin/view/Motion/VideoFourLinuxLoopbackDevice
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Oct 28 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.4-69
+ update to 3.6.4-69
+ about the ext4 problem discussed > https://lwn.net/Articles/521022/
- added FX01-fix-serious-progressive-ext4-data-corruption-bug.patch
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- The rel -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Oct 23 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.3-69
+ update to 3.6.3 (85 fixes all over)
- added OverlayFS v. 3.6
- fixed problems with CK1
- updated TOI to v. 3.6.3
- some small scripts cleanups
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- This is -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Mon Oct 22 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.3-1
+ update to 3.6.3 (85 fixes all over)
- add OverlayFS 
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- This is -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Tue Oct 16 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.2-69
+ update to 3.6.2 (135 fixes all over)
+ For development serie we have now the following kernel flavours
- this serie include the following flavours with: CK1, BFS, BFQ, TOI
- & since now also UKSM > For Data Deduplication Of The Linux Kernel:
- http://www.phoronix.com/scan.php?page=news_item&px=MTEzMTI
+ We changed the codename of this experimental from nrjEvo to nrjQL
- kernel-nrjQL-desktop
- kernel-nrjQL-realtime
- kernel-nrjQL-laptop
- kernel-nrjQL-netbook
- kernel-nrjQL-server
- kernel-nrjQL-server-games
- kernel-nrjQL-server-computing
- kernel-nrjQL-desktop-pae
- kernel-nrjQL-realtime-pae
- kernel-nrjQL-laptop-pae
- kernel-nrjQL-netbook-pae
- kernel-nrjQL-desktop-core2,
- kernel-nrjQL-desktop-core2-pae
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- This is -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sat Oct 13 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.2-1
+ update to 3.6.2 (135 fixes all over)
- now CPU_FREQ_GOV_ONDEMAND is the predefined for -laptop and -netbook
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- This is -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sat Oct 13 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.5.7-1
+ update to 3.5.7 (136 fixes all over, this is the EOL version!)
- "Note, this is the LAST 3.5.y kernel release, it is now end-of-life.
- Please move to the 3.6 kernel branch at this time."
- now CPU_FREQ_GOV_ONDEMAND is the predefined for -laptop and -netbook
- ---------------------------------------------------------------------
- Kernel 3.5 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- This is -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Oct 12 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.6.1-1
+ update to 3.6.1 
- first attempt with new kernel 3.6 serie
- ---------------------------------------------------------------------
- Kernel 3.6 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- This is -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sun Oct 07 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.5.6-1
+ update to 3.5.6 (57 fixes all over)
-fixed a version require problem with cpupower install
- ---------------------------------------------------------------------
- Kernel 3.5 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- This is -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Oct 05 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.5.5-69
+ update to 3.5.5 (283 fixes all over)
- Improved the "nrj" mode and fixed all remaining script build warnings
- Changed CONFIG_NLS_CODEPAGE_437=m to y, enabling UEFI boot for 2012.1
- Starting only from RM 2012 and greater:
- it's enabled the build of "cpupower" config and systemd service files 
- it's enabled the build of perf tools and the supporting documentation 
  * userspace utilities are designed to assist with CPU frequency scaling
  * Some info:
  * http://lwn.net/Articles/433002/
  * https://wiki.archlinux.org/index.php/CPU_Frequency_Scaling
- Obsoled cpufreq / cpufrequtils when cpupower / perf tools replace them
+ For development serie we have now the following kernel flavours
- this serie include the following flavours with: CK1, BFS, BFQ, TOI
- kernel-nrjEvo-desktop
- kernel-nrjEvo-realtime
- kernel-nrjEvo-laptop
- kernel-nrjEvo-netbook
- kernel-nrjEvo-server
- kernel-nrjEvo-server-games
- kernel-nrjEvo-server-computing
- kernel-nrjEvo-desktop-pae
- kernel-nrjEvo-realtime-pae
- kernel-nrjEvo-laptop-pae
- kernel-nrjEvo-netbook-pae
- kernel-nrjEvo-desktop-core2,
- kernel-nrjEvo-desktop-core2-pae
+ Added a critical patch for ck1 patchset to work with 3.5.5: 
- unfuck_sched_fix_race_in_task_group_function.patch
- ---------------------------------------------------------------------
- Kernel 3.5 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- This is -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Fri Oct 05 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.5.5-1
+ update to 3.5.5 (283 fixes all over)
- Improved the "nrj" mode and fixed all remaining script build warnings
- Changed CONFIG_NLS_CODEPAGE_437=m to y, enabling UEFI boot for 2012.1
- Starting only from RM 2012 and greater:
- it's enabled the build of "cpupower" config and systemd service files 
- it's enabled the build of perf tools and the supporting documentation 
  * userspace utilities are designed to assist with CPU frequency scaling
  * Some info:
  * http://lwn.net/Articles/433002/
  * https://wiki.archlinux.org/index.php/CPU_Frequency_Scaling
- Obsoled cpufreq / cpufrequtils when cpupower / perf tools replace them
- Added new kernel flavours, taken from development evolution:
- kernel-nrj-laptop, kernel-nrj-realtime and their pae versions
- ---------------------------------------------------------------------
- Kernel 3.5 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- This is -1 (mainline serie), with official kernel sources and addons,
- instead (-69) will be used for development and experimental flavours
- Yin & Yang (69) release - a very complete but experimental flavours...
- ---------------------------------------------------------------------

* Sat Sep 22 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.5.4-69.0mib
- update to 3.5.4
+ From now we use different release number (69) for development kernel
- this serie include many experimental features: CK1, BFS, BFQ, TOI
+ For development serie we have the following kernel flavours
- this serie include the following flavours with: CK1, BFS, BFQ, TOI
+ For some test about (NO_HZ=y/n) to compare tickless enable/disable 
- now we have -69.1 > Tickless enabled flavours & -69.0 No Tickless
- kernel-nrj-workstation,
- kernel-nrj-multimedia,
- kernel-nrj-studio,
- kernel-nrj-realtime,
- kernel-nrj-laptop,
- kernel-nrj-server,
- kernel-nrj-gameserver,
- kernel-nrj-workstation-pae,
- kernel-nrj-multimedia-pae,
- kernel-nrj-studio-pae,
- kernel-nrj-laptop-pae,
- kernel-nrj-workstation-core2,
- kernel-nrj-workstation-core2-pae
- ---------------------------------------------------------------------
+ Yin & Yang (69) release - a very complete kernel flavour serie
- Kernel 3.5 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- ---------------------------------------------------------------------

* Mon Sep 17 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.5.4-1
+ update to 3.5.4
- fixed a key value for nrj, to avoid a build warning
- added some patches for
  * overlayfs support (from ubuntu)
- updated defconfigs for overlayfs
- dropped broken unionfs patches
- disabled broken unionfs from defconfigs
- ---------------------------------------------------------------------
- Kernel 3.5 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- ---------------------------------------------------------------------

* Mon Sep 10 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.5.3-69mib
- update to 3.5.3
+ From now we use different release number (69) for development kernel
- this serie include: CK1, BFS, BFQ, TOI
- added patches for
+ Con Kolivas desktop patches with BFS
  * 3.5-sched-bfs-424.patch
  * mm-minimal_swappiness.patch
  * mm-drop_swap_cache_aggressively.patch
  * mm-kswapd_inherit_prio-1.patch
  * mm-idleprio_prio-1.patch
  * mm-decrease_default_dirty_ratio-1.patch
  * kconfig-expose_vmsplit_option.patch
  * hz-default_1000.patch
  * hz-no_default_250.patch
  * hz-raise_max.patch
  * preempt-desktop-tune.patch
  * ck1-version.patch
  * urw-locks.patch
  * bfs424-grq_urwlocks.patch
+ BFQ I/O disk scheduler
  * 0001-block-cgroups-kconfig-build-bits-for-BFQ-v4-3.5.patch
  * 0002-block-introduce-the-BFQ-v4-I-O-sched-for-3.5.patch
+ Tux On Ice
   * KP01_TuxOnIce-3.3-for-3.5.patch
+ For development serie we have the following kernel flavours
- this serie include the following flavours with: CK1, BFS, BFQ, TOI
- kernel-nrj-workstation,
- kernel-nrj-multimedia,
- kernel-nrj-studio,
- kernel-nrj-realtime,
- kernel-nrj-laptop,
- kernel-nrj-server,
- kernel-nrj-gameserver,
- kernel-nrj-workstation-pae,
- kernel-nrj-multimedia-pae,
- kernel-nrj-studio-pae,
- kernel-nrj-laptop-pae,
- kernel-nrj-workstation-core2,
- kernel-nrj-workstation-core2-pae
- ---------------------------------------------------------------------
+ Yin & Yang (69) release - a very complete kernel flavour serie
- Kernel 3.5 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- ---------------------------------------------------------------------

* Mon Aug 27 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.5.3-1mib
- update to 3.5.3
- ---------------------------------------------------------------------
- Kernel 3.5 for mdv 2010.2, 2011.0, cooker, rosa.lts2012.0, rosa2012.1
- MIB (Mandriva International Backports) - http://mib.pianetalinux.org/
- ---------------------------------------------------------------------

* Sat Aug 11 2012 Nicolo' Costanza <abitrules@yahoo.it> 3.5.1-1mib
- First version of kernel 3.5 adapted by MIB for Mandriva & ROSA linux
- update to 3.5.1


------------------
--- a/kernel-3.10.24-69.spec    2013-12-19 16:07:45.150915258 +0400
+++ b/kernel-3.10.24-69.spec    2013-12-19 16:08:46.673915978 +0400
@@ -252,3 +252,3 @@
  %{?_with_nrjQL_laptop: %global build_nrjQL_laptop 1}
-%{?_with_nrjQL_laptop: %global build_nrjQL_netbook 1}
+%{?_with_nrjQL_netbook: %global build_nrjQL_netbook 1}

@@ -259,3 +259,3 @@
  %{?_with_nrjQL_desktop_pae: %global build_nrjQL_desktop_pae 1}
-%{?_with_nrjQL_desktop_pae: %global build_nrjQL_realtime_pae 1}
+%{?_with_nrjQL_realtime_pae: %global build_nrjQL_realtime_pae 1}
------------------

