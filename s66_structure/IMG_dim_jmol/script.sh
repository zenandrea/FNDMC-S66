
https://gist.github.com/protrolium/21ab48468470ea8e3a72567fd8938abe

convert dimers.00.png  -gravity North -pointsize 30 -annotate +0+100 'dimer' temp1.png

convert -background white -alpha remove -alpha off -delay 11 -loop 0 dimers*.png  animation.gif


for i in `seq 0 9`; do name=`awk -v i=$i '{ if (NR==i+1) print }' lista`; echo $i $name;  convert dimers.0${i}.png -gravity North -pointsize 30 -annotate +0+100 "$name" new_0${i}.png; done

for i in `seq 10 65`; do name=`awk -v i=$i '{ if (NR==i+1) print }' lista`; echo $i $name;  convert dimers.${i}.png -gravity North -pointsize 30 -annotate +0+100 "$name" new_${i}.png; done


convert -background white -alpha remove -alpha off -delay 1x3 -loop 0 new_*.png  animation.gif

# a frame each 1/3 second
