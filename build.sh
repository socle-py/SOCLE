nameScript=socle.py
nameBinary=socle
nameLink=socle
[[ $1 == "" ]] && { echo need version as '$1' ; exit 1 ; }
mkdir -p ./build
rm -rf ./build/*
cxfreeze -c $nameScript --target-dir ./build/$nameBinary
cd ./build/ && tar -zcvf $nameBinary.tar.gz $nameBinary && cd -
ln -sf ./build/$nameBinary/$nameBinary ~/.local/bin/$nameLink





# 4,5M	/home/throc/build/starterTree/lib/libpython3.6m.so
# 4,5M	/home/throc/build/starterTree/lib/libpython3.6m.so.1.0
# 1,1M	/home/throc/build/starterTree/lib/library.zip
# 1,4M	/home/throc/build/starterTree/lib/prompt_toolkit
# 3,1M	/home/throc/build/starterTree/lib/pygments

