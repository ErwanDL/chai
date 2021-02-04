#! /bin/bash

if [ ! -d $data_path ]; then
    data_path="/home/z/zimin/pfs/deepmutation_OpenNMT/data/50"
    if [ ! -d $data_path ]; then
        # For now, choose between 2 hard coded paths - Zimin's and Steve's
        data_path="/s/chopin/l/grad/steveko/p/codrep/deepmutation_OpenNMT/data/50"
    fi
fi
onmt_preprocess -train_src $data_path/src-train.txt -train_tgt $data_path/tgt-train.txt -valid_src $data_path/src-val.txt -valid_tgt $data_path/tgt-val.txt -src_seq_length 1010 -tgt_seq_length 100 -src_vocab_size 1000 -tgt_vocab_size 1000 -dynamic_dict -share_vocab -save_data $data_path/final 2>&1 > $data_path/preprocess.out
