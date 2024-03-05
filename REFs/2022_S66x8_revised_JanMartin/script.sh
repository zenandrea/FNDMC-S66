echo Structures
awk '{if (NR%9==1) print }' tab1.txt
echo
echo Equilibrium Eb
awk '{if (NR%9==4) print }' tab1.txt
