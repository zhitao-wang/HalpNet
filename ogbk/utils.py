# -*- coding: utf-8 -*-
import torch
from ogbk.negative_sample import *


def get_pos_neg_edges(split, split_edge, edge_index=None, num_nodes=None, neg_sampler_name=None, num_neg=None):
    if 'edge' in split_edge['train']:
        pos_edge = split_edge[split]['edge'].t()
        if split == 'train':
            if neg_sampler_name == 'local':
                neg_edge = local_random_neg_sample(
                    pos_edge,
                    num_nodes=num_nodes,
                    num_neg=num_neg)
            elif neg_sampler_name == 'global':
                neg_edge = global_neg_sample(
                    edge_index,
                    num_nodes=num_nodes,
                    num_samples=pos_edge.size(0),
                    num_neg=num_neg)
            else:
                neg_edge = global_perm_neg_sample(
                    edge_index,
                    num_nodes=num_nodes,
                    num_samples=pos_edge.size(0),
                    num_neg=num_neg)
        else:
            neg_edge = split_edge[split]['edge_neg'].t()

    elif 'source_node' in split_edge['train']:
        source = split_edge[split]['source_node']
        target = split_edge[split]['target_node']
        if split == 'train':
            target_neg = torch.randint(0, num_nodes, [target.size(0), 1],
                                       dtype=torch.long)
        else:
            target_neg = split_edge[split]['target_node_neg']

        pos_edge = torch.stack([source, target])
        neg_per_target = target_neg.size(1)
        neg_edge = torch.stack([source.repeat_interleave(neg_per_target),
                                target_neg.view(-1)])
    return pos_edge, neg_edge


def evaluate_hits(evaluator, pos_val_pred, neg_val_pred,
                  pos_test_pred, neg_test_pred):
    results = {}
    for K in [20, 50, 100]:
        evaluator.K = K
        valid_hits = evaluator.eval({
            'y_pred_pos': pos_val_pred,
            'y_pred_neg': neg_val_pred,
        })[f'hits@{K}']
        test_hits = evaluator.eval({
            'y_pred_pos': pos_test_pred,
            'y_pred_neg': neg_test_pred,
        })[f'hits@{K}']

        results[f'Hits@{K}'] = (valid_hits, test_hits)

    return results


def evaluate_mrr(evaluator, pos_val_pred, neg_val_pred,
                 pos_test_pred, neg_test_pred):
    neg_val_pred = neg_val_pred.view(pos_val_pred.shape[0], -1)
    neg_test_pred = neg_test_pred.view(pos_test_pred.shape[0], -1)
    results = {}
    valid_mrr = evaluator.eval({
        'y_pred_pos': pos_val_pred,
        'y_pred_neg': neg_val_pred,
    })['mrr_list'].mean().item()

    test_mrr = evaluator.eval({
        'y_pred_pos': pos_test_pred,
        'y_pred_neg': neg_test_pred,
    })['mrr_list'].mean().item()

    results['MRR'] = (valid_mrr, test_mrr)

    return results