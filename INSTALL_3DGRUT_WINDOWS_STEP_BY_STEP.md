# 3D GRUT - Instalação Windows Passo a Passo

## ⚠️ Aviso Importante

O 3D GRUT tem **suporte experimental** no Windows. A instalação é complexa e pode não funcionar completamente.

**Recomendação**: Use WSL2 (Windows Subsystem for Linux) para melhor compatibilidade.

---

## 📋 Pré-Requisitos

### Verificar Instalados
Execute estes comandos no PowerShell:

```powershell
# 1. Python
python --version
# ✓ Precisa ser 3.10 ou 3.11 (não 3.12+)

# 2. NVIDIA GPU
nvidia-smi
# ✓ Deve mostrar sua GPU

# 3. CUDA Toolkit
nvcc --version
# ✓ Precisa ser CUDA 11.8 ou 12.x

# 4. Visual Studio
where cl
# ✓ Deve encontrar compilador C++

# 5. Conda
conda --version
# ✓ Deve mostrar versão do conda
```

### Resultados Esperados
```
✓ Python 3.10.x ou 3.11.x
✓ CUDA 11.8+ ou 12.x
✓ Visual Studio 2019/2022 com C++ tools
✓ Conda instalado
✓ GPU NVIDIA com driver atualizado
```

---

## 🚀 Instalação Manual - Passo a Passo

### Passo 1: Criar Ambiente Conda
```powershell
# Criar ambiente Python 3.10
conda create -n 3dgrut python=3.10 -y

# Ativar ambiente
conda activate 3dgrut

# Verificar
python --version
# Deve mostrar: Python 3.10.x
```

**Status**: [ ] Concluído

---

### Passo 2: Instalar PyTorch com CUDA
```powershell
# Ativar ambiente
conda activate 3dgrut

# Instalar PyTorch (CUDA 11.8)
pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu118

# OU para CUDA 12.1
# pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu121

# Verificar instalação
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"
```

**Resultado esperado**:
```
PyTorch: 2.1.0+cu118
CUDA available: True
```

**Status**: [ ] Concluído

---

### Passo 3: Instalar Dependências Python
```powershell
cd C:\Users\User\3dgrut

# Instalar requirements
pip install -r requirements.txt

# Instalar pacotes adicionais
pip install ninja pycolmap opencv-python matplotlib pillow tqdm
```

**Status**: [ ] Concluído

---

### Passo 4: Instalar tiny-cuda-nn (Compilação Necessária)
```powershell
# Ativar ambiente
conda activate 3dgrut

# Opção A: Tentar pip (pode falhar)
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

# Opção B: Compilar manualmente
git clone --recursive https://github.com/NVlabs/tiny-cuda-nn
cd tiny-cuda-nn/bindings/torch
python setup.py install
cd ../../..
```

**⚠️ Nota**: Este passo pode falhar. Se falhar, veja seção "Troubleshooting" abaixo.

**Status**: [ ] Concluído

---

### Passo 5: Instalar nerfstudio (Dependência)
```powershell
conda activate 3dgrut

pip install nerfstudio
```

**Status**: [ ] Concluído

---

### Passo 6: Instalar 3D GRUT em Modo Desenvolvimento
```powershell
cd C:\Users\User\3dgrut

# Instalar em modo editável
pip install -e .

# Verificar importação
python -c "import threedgrut; print('3D GRUT OK!')"
```

**Status**: [ ] Concluído

---

### Passo 7: Testar Instalação
```powershell
cd C:\Users\User\3dgrut

# Verificar scripts existem
Test-Path train.py
Test-Path render.py

# Testar help do script
python train.py --help
```

**Resultado esperado**: Deve mostrar opções de comando do train.py

**Status**: [ ] Concluído

---

## 🧪 Teste Rápido

### Preparar Dados de Teste
```powershell
# Criar estrutura
New-Item -ItemType Directory -Path "C:\Users\User\test_3dgrut\images" -Force
New-Item -ItemType Directory -Path "C:\Users\User\test_3dgrut\sparse\0" -Force

# Copiar algumas imagens para test_3dgrut\images\
# (use 10-20 imagens de teste)
```

### Gerar Sparse Model (usando GloMAP GUI ou COLMAP)
1. Abra GloMAP GUI
2. Selecione pasta `C:\Users\User\test_3dgrut`
3. Execute pipeline completo
4. Verifique `sparse\0\` contém: cameras.bin, images.bin, points3D.bin

### Treinar Modelo 3D GRUT
```powershell
conda activate 3dgrut
cd C:\Users\User\3dgrut

python train.py `
  --config_name colmap `
  --data.path C:\Users\User\test_3dgrut `
  --output_dir C:\Users\User\test_3dgrut\output `
  --down_sample_factor 4 `
  --iterations 1000
```

**Tempo esperado**: 5-10 minutos  
**Status**: [ ] Concluído

---

## 🐛 Troubleshooting

### Erro: "tiny-cuda-nn não compila"

**Solução 1**: Usar versão pré-compilada (se disponível)
```powershell
pip install tiny-cuda-nn
```

**Solução 2**: Configurar Visual Studio
```powershell
# Encontrar Visual Studio
$vsPath = "C:\Program Files\Microsoft Visual Studio\2022\Community"
if (Test-Path $vsPath) {
    & "$vsPath\Common7\Tools\VsDevCmd.bat"
}

# Tentar compilar novamente
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
```

**Solução 3**: Pular este componente (3D GRUT pode não funcionar completamente)

---

### Erro: "CUDA out of memory"
```powershell
# Usar menor resolução
--down_sample_factor 8  # Em vez de 4 ou 2
```

---

### Erro: "cl.exe not found"
```powershell
# Instalar Visual Studio Build Tools
# Baixar de: https://visualstudio.microsoft.com/downloads/
# Selecionar: "Desktop development with C++"
```

---

### Erro: "No module named 'torch'"
```powershell
# Reinstalar PyTorch
conda activate 3dgrut
pip uninstall torch torchvision -y
pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu118
```

---

## 🔄 Alternativa: Instalar via WSL2 (Recomendado)

Se a instalação Windows nativa falhar, use WSL2:

### Passo 1: Instalar WSL2
```powershell
# Em PowerShell (Administrador)
wsl --install -d Ubuntu-22.04

# Reiniciar computador
# Após reiniciar, abrir Ubuntu pela primeira vez
```

### Passo 2: Configurar WSL2
```bash
# Dentro do Ubuntu (WSL2)
sudo apt update
sudo apt upgrade -y

# Instalar CUDA (WSL2 tem suporte especial)
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-8
```

### Passo 3: Instalar 3D GRUT no WSL2
```bash
# Instalar Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
~/miniconda3/bin/conda init bash
source ~/.bashrc

# Clonar repositório
cd ~
git clone https://github.com/nv-tlabs/3dgrut
cd 3dgrut

# Instalar
chmod +x install_env.sh
./install_env.sh 3dgrut
conda activate 3dgrut
```

---

## 📊 Checklist de Instalação

### Pré-requisitos
- [ ] Python 3.10 ou 3.11
- [ ] CUDA 11.8 ou 12.x
- [ ] Visual Studio com C++ tools
- [ ] Conda instalado
- [ ] GPU NVIDIA

### Instalação
- [ ] Ambiente conda criado
- [ ] PyTorch + CUDA instalado
- [ ] Requirements.txt instalado
- [ ] tiny-cuda-nn compilado
- [ ] nerfstudio instalado
- [ ] 3D GRUT instalado (pip install -e .)

### Teste
- [ ] Import threedgrut funciona
- [ ] train.py --help funciona
- [ ] Teste com dataset pequeno completa

### Integração com GloMAP GUI
- [ ] GUI reconhece instalação (mostra ✓)
- [ ] Botão "Run 3DGUT" funciona
- [ ] Treinamento completa

---

## 📞 Suporte

Se encontrar problemas:

1. **Verifique logs**: Procure mensagens de erro específicas
2. **Verifique GPU**: `nvidia-smi` deve funcionar
3. **Verifique CUDA**: `nvcc --version` deve funcionar
4. **Considere WSL2**: Instalação mais estável

### Recursos
- GitHub Issues: https://github.com/nv-tlabs/3dgrut/issues
- GUIA_3DGRUT_INSTALACAO.md (guia em português)
- INSTALL_3DGRUT_QUICKSTART.md (guia rápido)

---

**Dificuldade**: Alta (Windows nativo) | Média (WSL2)  
**Tempo Estimado**: 1-3 horas (Windows) | 30-60 minutos (WSL2)  
**Taxa de Sucesso**: ~60% (Windows) | ~90% (WSL2)

---

*Última atualização: 2025-01-15*
