%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from coffee-script-2.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name coffee-script

Summary: Ruby CoffeeScript Compiler
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.2.0
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/josh/ruby-coffee-script
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# To get the tests:
# git clone https://github.com/josh/ruby-coffee-script && cd ruby-coffee-script
# git checkout v2.2.0 && tar czf coffee-script-tests-2.2.0.tgz test/
Source1: coffee-script-tests-%{version}.tgz
# Proposed upstream https://github.com/josh/ruby-coffee-script/pull/16
# For initial report see https://github.com/josh/ruby-coffee-script/issues/15
#Patch0: coffee-script-fix-newlines-in-tests.patch

# Minitest 5.x compatibility fixes.
# https://github.com/josh/ruby-coffee-script/commit/60900187617ce7dcbb6ccd94fbdfddaa8022bd0a
Patch0: rubygem-coffee-script-2.2.0-Condition-minitest.patch
# https://github.com/josh/ruby-coffee-script/commit/9b34e37d7ecfa750f5185a0e16df1c131732e318
Patch1: rubygem-coffee-script-2.2.0-Fix-assertions.patch
# https://github.com/josh/ruby-coffee-script/commit/eeee9a0cf4c092c034d49be531678fb2f6d1acd8
Patch2: rubygem-coffee-script-2.2.0-Export-generic-CoffeeScript-Error.patch
# https://github.com/josh/ruby-coffee-script/commit/62abd5a9522b50e75f1756d550d4845c49b4a29f
Patch3: rubygem-coffee-script-2.2.0-Test-error-messages-across-versions.patch
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(coffee-script-source)
Requires: %{?scl_prefix}rubygem(execjs)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(coffee-script-source)
BuildRequires: %{?scl_prefix}rubygem(execjs)
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(therubyracer)
BuildRequires: v8314-v8
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Ruby CoffeeScript is a bridge to the JS CoffeeScript compiler.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %scl - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# unpack and patch the tests
tar xzf %{SOURCE1}
patch -p1 < %{PATCH0}
patch -p1 < %{PATCH1}
patch -p1 < %{PATCH2}
patch -p1 < %{PATCH3}

%{?scl:scl enable %scl v8314 - << \EOF}
ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Mon Jan 26 2015 Josef Stribny <jstribny@redhat.com> - 2.2.0-6
- rebuilt for rh-ror41

* Mon Feb 17 2014 Josef Stribny <jstribny@redhat.com> - 2.2.0-5
- Depend on scldevel(v8) virtual provide

* Tue Nov 26 2013 Josef Stribny <jstribny@redhat.com> - 2.2.0-4
- Use v8 scl macro

* Wed Jun 12 2013 Josef Stribny <jstribny@redhat.com> - 2.2.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Jul 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.2.0-2
- Introduce test suite.
- Specfile cleanup

* Tue Jul 17 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.2.0-1
- Initial package
