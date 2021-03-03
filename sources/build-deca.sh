#!/bin/sh
set -e
#source ../env/bin/activate

ttDir=../fonts/ttf

echo ".
GENERATING DECA STATICS
."

gftools builder config.yaml

echo ".
SUBSETTING DECA STATICS
."

ttfs=$(ls $ttDir/*.ttf)
for font in $ttfs
do
	pyftsubset $font --unicodes="0-3c0,1e08-fb02" --layout-scripts=latn,grek --layout-features='*' --output-file=$font.subset
	mv $font.subset $font
done 

echo ".
COMPLETE!
."
