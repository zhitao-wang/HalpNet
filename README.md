# HalpNet
This repository provides codes of our paper:
>**Hierarchical Attention Link Prediction Neural Network (https://www.sciencedirect.com/science/article/abs/pii/S0950705121006936)**

## Environment
The code is implemented with Tensorflow. Requirments:  
&emsp;1. python=3.6  
&emsp;2. tensorflow=1.13.2  
&emsp;3. networkx=2.4  

## Usage
Defalut:  

    python train.py  
    
Or run with optional arguments:  

    python train.py -d ceg -l 0.001 -x 64 -b 32 -n 1
    
Check the arguments as:  

    python train.py -h
    "-l", "--lr", type=float, help="learning rate"
    "-x", "--hidden_size", type=int, help="hidden dimension"
    "-d", "--data", help="data name"
    "-g", "--gpu", help="gpu id"
    "-b", "--batch_size", type=int, help="batch size"
    "-n", "--num_hops", type=int, help="number of hops"

* data names should be consistent with the folder names in the data folder.

## Data Format
We provide data for 5 runs, please refer to the data folder.

## Citing
    @article{WANG2021halpnet,
            title = {Hierarchical Attention Link Prediction Neural Network},
            journal = {Knowledge-Based Systems},
            volume = {232},
            pages = {107431},
            year = {2021},
            issn = {0950-7051},
            doi = {https://doi.org/10.1016/j.knosys.2021.107431},
            url = {https://www.sciencedirect.com/science/article/pii/S0950705121006936},
            author = {Zhitao Wang and Wenjie Li and Hanjing Su},
            keywords = {Hierarchical attention, Neural network, Link prediction}
            }
