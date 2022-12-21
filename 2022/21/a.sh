sed -e 's/:/=/' -e 's,/, `div` ,' < example > ex.hs
cat end.hs >> ex.hs

sed -e 's/:/=/' -e 's,/, `div` ,' < input > a.hs
cat end.hs >> a.hs

runhaskell ex.hs
runhaskell a.hs
