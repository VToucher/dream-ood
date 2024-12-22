CUDA_VISIBLE_DEVICES=1,2,3,4,5,6 \
python scripts/train_ood_det_in100.py \
--my_info '' \
--load checkpoints/in100_initialized_model_for_ood_det.pt \
--epochs 100 \
--batch_size 160 \
--oe_batch_size 160 \
--learning_rate 0.1 \
--ngpu 6