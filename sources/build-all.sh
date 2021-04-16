#!/bin/sh
set -e
#source ../env/bin/activate


echo ".
GENERATING NEW DECA VF + STATICS
."

#gftools builder build-deca.yaml

echo ".
GENERATING OLD 7 FAMILIES
."

gftools builder build-families.yaml

oldTT=$(ls ../fonts/7families/*.ttf)
for font in $ttfs
do
	gftools fix-weightclass $font
	mv $font.fix $font
done

echo ".
COMPLETE!
."
