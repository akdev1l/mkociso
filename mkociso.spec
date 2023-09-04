%global debug_package %{nil}

Name:       {{{ git_dir_name }}}
Version:    {{{ git_dir_version }}}
Release:    1%{?dist}
Summary:    Tool to create installer ISO for OSTree based containers.

License:    GPLv2+
URL:        https://github.com/ublue-os/lorax-compose
VCS:        {{{ git_dir_vcs }}}

Source: {{{ git_dir_pack }}}
Requires: python3-boto3
Requires: lorax
Requires: skopeo
BuildArch: noarch
BuildRequires: poetry
BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: python3-poetry
BuildRequires: python3-boto3

%generate_buildrequires
%pyproject_buildrequires


%description
Tool to create installer ISO for OSTree based containers.

%prep
{{{ git_dir_setup_macro }}}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %name

%files -f %pyproject_files
%{_bindir}/%name

%changelog
%autochangelog
{{{ git_dir_changelog }}}
