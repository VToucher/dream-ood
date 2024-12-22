## 环境配置
1. 修改`environment.yaml`
   - pytorch=1.12.1
   - torchvision=0.13.1
2. conda env create -f environment.yaml
3. pip install xformers==0.13.0
4. pip install triton==2.0.0

## 提高推理效率
1. ldm/modules/encoders/modules.py
   - CLIP使用`FrozenCLIPEmbedder`类提取text-emb
 - 提高模型加载效率
   - `CLIPTokenizer.from_pretrained`增加`local_files_only=True`参数
   - `CLIPTextModel.from_pretrained`增加`local_files_only=True`参数
 - 提高数据加载效率
   - `FrozenCLIPEmbedder.encode`函数减少不必要的`self.outlier_embedding`属性加载