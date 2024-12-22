CUDA_VISIBLE_DEVICES=7 \
python scripts/dream_ood.py --plms \
--n_iter 2500 --n_samples 4 \
--outdir saved_data/txt2img-samples-in100/ \
--loaded_embedding saved_data/outlier_npos_embed.npy \
--ckpt checkpoints/sd-v1-4.ckpt \
--id_data in100 \
--skip_grid