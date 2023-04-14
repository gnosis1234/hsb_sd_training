for VARIABLE in {26..34}
do
    nohup python training/tools/dataset_make.py $VARIABLE &
done