# -*- coding: utf-8 -*-
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import numpy as np
import argparse
import torch
import torch.nn.functional as F
import faiss
res = faiss.StandardGpuResources()
KNN_index = faiss.GpuIndexFlatL2(res, 768)
from torch.distributions import MultivariateNormal
from KNN import generate_outliers


parser = argparse.ArgumentParser(description='Tunes a CIFAR Classifier with OE',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# generation hyperparameters.
parser.add_argument('--inlier', type=int, default=0)
parser.add_argument('--gaussian_mag_ood_det', type=float, default=0.03)
parser.add_argument('--gaussian_mag_ood_gene', type=float, default=0.01)
parser.add_argument('--K_in_knn', type=int, default=300)
parser.add_argument('--ood_det_select', type=int, default=200)
parser.add_argument('--ood_gene_select', type=int, default=1000)
parser.add_argument('--gpu', type=int, default=0)
parser.add_argument('--shift', type=bool, default=False)
args = parser.parse_args()



# anchor = torch.from_numpy(np.load('./token_embed_in100.npy')).cuda()
num_classes = 100
sum_temp = 0


# data_dict = torch.from_numpy(np.load('./id_feat_in100_99epoch.npy')).cuda()
data_dict = torch.randn(num_classes, 1000, 768).cuda()
for index in range(100):
    sum_temp += 1000  # number_dict[index]
# breakpoint()
if sum_temp == num_classes * 1000:  # true
    for index in range(num_classes):  # get ood emb by class
        ID = F.normalize(data_dict[index], p=2, dim=1)  # [1000, 768], norm 768 dim
        if True:
            if args.shift:  # None
                print(index)
                for index1 in range(100):
                    new_dis = MultivariateNormal(torch.zeros(768).cuda(), torch.eye(768).cuda())
                    negative_samples = new_dis.rsample((1500,))
                    sample_point1, boundary_point = generate_outliers(ID,
                                                                      input_index=KNN_index,
                                                                      negative_samples=negative_samples,
                                                                      ID_points_num=1,
                                                                      K=args.K_in_knn,
                                                                      select=args.ood_gene_select,
                                                                      cov_mat=args.gaussian_mag_ood_gene,
                                                                      sampling_ratio=1.0,
                                                                      pic_nums=100,
                                                                      depth=768, shift=1)
                    if index1 == 0:
                        sample_point = sample_point1
                    else:
                        sample_point = torch.cat([sample_point, sample_point1], 0)
            else:  # true
                print(index)
                for index1 in range(100):
                    # 均值方差直接放cuda会采样出nan
                    # new_dis = MultivariateNormal(torch.zeros(768).cuda(), torch.eye(768).cuda())
                    new_dis = MultivariateNormal(torch.zeros(768), torch.eye(768))
                    negative_samples = new_dis.rsample((1500,)).cuda()
                    sample_point1, boundary_point = generate_outliers(ID,
                                                                      input_index=KNN_index,
                                                                      negative_samples=negative_samples,
                                                                      ID_points_num=2,
                                                                      K=args.K_in_knn,  # 300
                                                                      select=args.ood_det_select,  # 200
                                                                      cov_mat=args.gaussian_mag_ood_det,  # 0.03
                                                                      sampling_ratio=1.0, pic_nums=50,
                                                                      depth=768 ,shift=0)
                    if index1 == 0:
                        sample_point = sample_point1
                    else:
                        sample_point = torch.cat([sample_point, sample_point1], 0)

            if index == 0:
                ood_samples = [sample_point * anchor[index].norm()]
            else:
                ood_samples.append(sample_point * anchor[index].norm())



if args.inlier:
    np.save \
        ('./inlier_npos_embed'+ '_noise_' + str(args.gaussian_mag_ood_gene)  + '_select_'+ str(
        args.ood_gene_select) + '_KNN_'+ str(args.K_in_knn) + '.npy', torch.stack(ood_samples).cpu().data.numpy())
else:
    np.save \
        ('./outlier_npos_embed' + '_noise_' + str(args.gaussian_mag_ood_det) + '_select_' + str(
        args.ood_det_select) + '_KNN_' + str(args.K_in_knn) + '.npy', torch.stack(ood_samples).cpu().data.numpy())
