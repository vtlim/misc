
# Loop over set of PDB IDs pertaining to BACE1, and open pertaining information in the PDBbind website.
# PDB IDs ordered from http://onlinelibrary.wiley.com/doi/10.1002/jcc.24839/full

# Before using, open a Chromium browser and log into PDBbind in an incognito window. Or standard window, but chg command below.

BASE='http://www.pdbbind.org.cn/quickpdb.asp?quickpdb='

set1=( "4gid" "1m4h" "2g94" "2qmg" "3lpk" "4h3f" "2p4j" "1fkn" "4frs" "3lpi" )
set2=( "4h1e" "4h3i" "3i25" "4djy" "4h3g" "2q15" "4r93" "4fsl" "4r95" "2fdp" )
set3=( "4b05" "4r92" "4ha5" "4djx" "4h3j" "4djv" "4fs4" "4r91" "3ckp" "4djw" )
set4=( "4r8y" "2q11" "4dju" "3ru1" "3kmx" "3wb5" "3kmy" "3wb4" "3rsx" "3l5b" )
set5=( "3l59" "3buh" "3bug" "3buf" "3udh" "3bra" )

for pdbid in "${set4[@]}"
do
    echo $pdbid
    chromium-browser --incognito $BASE$pdbid
#    firefox --new-tab $BASE$pdbid
done
