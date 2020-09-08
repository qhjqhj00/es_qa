time=$(date "+%Y%m%d")

python preprocess.py  \
--source "data/${time}_source.txt" \
--save "data/${time}_faq.txt"

python build.py \
--file "data/${time}_faq.txt"
