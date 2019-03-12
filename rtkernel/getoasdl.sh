#!/bin/sh

notfound=""
for i in wget tar quilt gunzip
do
    if ! which $i >/dev/null 2>&1
    then
	notfound="$notfound $i"
    fi
done

if test "$notfound"

then
    if which yum >/dev/null 2>&1
    then
	/bin/echo -en 1>&2 "Please run\n  yum install"
    elif which apt-get >/dev/null 2>&1
    then
	/bin/echo -en 1>&2 "Please run\n  apt-get install"
    else
	/bin/echo -en 1>&2 "Please install\n "
    fi
    echo 1>&2 "$notfound"
    echo 1>&2 before executing this script.
    exit 1
fi

wget http://www.kernel.org/pub/linux/kernel/v4.x/linux-4.6.5.tar.xz
tar -Jxvf linux-4.6.5.tar.xz
mv linux-4.6.5 linux-4.6.5-rt10
cd linux-4.6.5-rt10
mkdir patches
cd patches
wget https://www.osadl.org/monitoring/patches/rbs3/series
for i in `cat series`
do
    wget https://www.osadl.org/monitoring/patches/rbs3/$i
done

cd ..

quilt push -a

wget https://www.osadl.org/monitoring/configs/rbs3.config.gz
gunzip rbs3.config.gz
mv rbs3.config .config

echo The kernel linux-4.6.5-rt10 is now ready to 
