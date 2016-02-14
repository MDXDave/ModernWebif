#!/bin/bash

D=$(pushd $(dirname $0) &> /dev/null; pwd; popd &> /dev/null)
P=${D}/ipkg.tmp.$$
B=${D}/ipkg.build.$$

pushd ${D} &> /dev/null
VER=$(head -n 3 CHANGES.md | grep -i '## Version' | sed 's/^## Version \([[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+\)/\1/')
GITVER=GIT$(git log -1 --format="%ci" | awk -F" " '{ print $1 }' | tr -d "-")
PKG=${D}/enigma2-plugin-extensions-modernwebif_${VER}-${GITVER}_all.ipk
popd &> /dev/null

mkdir -p ${P}
mkdir -p ${P}/CONTROL
mkdir -p ${B}

cat > ${P}/CONTROL/control << EOF
Package: enigma2-plugin-extensions-modernwebif
Version: ${VER}-${GITVER}-r0
Description: Webinterface for controlling your receiver
Architecture: all
Section: extra
Priority: optional
Maintainer: E2OpenPlugins members, MDXDave
Homepage: https://github.com/MDXDave/ModernWebIf
Depends: python-json, python-cheetah, python-pyopenssl, python-unixadmin, python-misc, python-twisted-web, python-pprint, python-compression
Source: https://github.com/MDXDave/ModernWebIf
EOF

mkdir -p ${P}/usr/lib/enigma2/python/Plugins/Extensions/ModernWebif/
cp -rp ${D}/plugin/* ${P}/usr/lib/enigma2/python/Plugins/Extensions/ModernWebif/
for f in $(find ./locale -name *.po ); do
	l=$(echo ${f%} | sed 's/\.po//' | sed 's/.*locale\///')
	mkdir -p ${P}/usr/lib/enigma2/python/Plugins/Extensions/ModernWebif/locale/${l%}/LC_MESSAGES
	msgfmt -o ${P}/usr/lib/enigma2/python/Plugins/Extensions/ModernWebif/locale/${l%}/LC_MESSAGES/ModernWebif.mo ./locale/$l.po
done

tar -C ${P} -czf ${B}/data.tar.gz . --exclude=CONTROL
tar -C ${P}/CONTROL -czf ${B}/control.tar.gz .

echo "2.0" > ${B}/debian-binary

cd ${B}
ls -la
ar -r ${PKG} ./debian-binary ./data.tar.gz ./control.tar.gz 
cd -

rm -rf ${P}
rm -rf ${B}
