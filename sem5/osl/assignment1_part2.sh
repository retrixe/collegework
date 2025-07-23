#!/bin/bash
mkdir -p abc/xyz/

cat > abc/xyz/test1.txt <<EOF
abc
xyz
EOF

cp abc/xyz/test1.txt abc/

mv abc/test1.txt abc/xyz/test2.txt

chmod 744 abc/xyz/test1.txt abc/xyz/test2.txt

ls -lah abc/xyz/
