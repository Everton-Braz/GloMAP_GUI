# 3D GRUT - Instalação WSL2 (Guia Rápido)

## ✅ Status: Ubuntu 22.04 LTS instalando...

A instalação do Ubuntu no WSL2 está em andamento. Após concluir, siga os passos abaixo.

---

## 📋 Passos Pós-Instalação

### Passo 1: Configurar Ubuntu (Primeira Execução)
Após a instalação terminar, uma janela do Ubuntu vai abrir pedindo:
- **Username**: escolha um nome de usuário (ex: `user`)
- **Password**: escolha uma senha (vai precisar dela para `sudo`)

```
UNIX username: user
New password: [digite sua senha]
Retype new password: [digite novamente]
```

**Status**: [ ] Concluído

---

### Passo 2: Atualizar Sistema
```bash
# Atualizar pacotes
sudo apt update
sudo apt upgrade -y

# Instalar ferramentas básicas
sudo apt install -y build-essential git wget curl
```

**Status**: [ ] Concluído

---

### Passo 3: Verificar GPU NVIDIA (WSL2)
```bash
# Verificar se GPU é detectada
nvidia-smi
```

**Resultado esperado**: Deve mostrar sua GPU NVIDIA

**Se falhar**: Os drivers NVIDIA para WSL2 são instalados no Windows, não no Linux. Certifique-se de ter o driver NVIDIA atualizado no Windows.

**Status**: [ ] Concluído

---

### Passo 4: Instalar CUDA Toolkit (WSL2)
```bash
# Adicionar repositório CUDA WSL2
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update

# Instalar CUDA 12.8
sudo apt-get -y install cuda-toolkit-12-8

# Adicionar ao PATH
echo 'export PATH=/usr/local/cuda-12.8/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Verificar
nvcc --version
```

**Resultado esperado**: `nvcc: NVIDIA (R) Cuda compiler driver ... release 12.8`

**Status**: [ ] Concluído

---

### Passo 5: Instalar Miniconda
```bash
# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Instalar
bash Miniconda3-latest-Linux-x86_64.sh -b

# Inicializar
~/miniconda3/bin/conda init bash
source ~/.bashrc

# Verificar
conda --version
```

**Status**: [ ] Concluído

---

### Passo 6: Clonar 3D GRUT
```bash
# Ir para home
cd ~

# Clonar repositório
git clone https://github.com/nv-tlabs/3dgrut
cd 3dgrut

# Verificar arquivos
ls -la
```

**Deve ver**: `install_env.sh`, `train.py`, `render.py`, etc.

**Status**: [ ] Concluído

---

### Passo 7: Instalar 3D GRUT
```bash
cd ~/3dgrut

# Dar permissão de execução
chmod +x install_env.sh

# Instalar (vai levar 10-20 minutos)
./install_env.sh 3dgrut

# Ativar ambiente
conda activate 3dgrut

# Verificar
python -c "import threedgrut; print('3D GRUT OK!')"
```

**Status**: [ ] Concluído

---

### Passo 8: Testar Instalação
```bash
# Ativar ambiente
conda activate 3dgrut

# Testar comando help
python ~/3dgrut/train.py --help
```

**Deve mostrar**: Opções do comando de treinamento

**Status**: [ ] Concluído

---

## 🔗 Conectar com Windows

### Acessar Arquivos do Windows no WSL
```bash
# Ir para drive C:
cd /mnt/c/

# Ir para pasta do usuário
cd /mnt/c/Users/User/

# Ir para pasta de projetos
cd /mnt/c/Users/User/Documents/APLICATIVOS/GloMAP_GUI/
```

### Acessar Arquivos do WSL no Windows
No Windows Explorer, digite na barra de endereços:
```
\\wsl$\Ubuntu-22.04\home\user\3dgrut
```

---

## 🧪 Teste Completo

### 1. Preparar Dados de Teste no Windows
```powershell
# No PowerShell (Windows)
New-Item -ItemType Directory -Path "C:\Users\User\test_3dgrut\images" -Force
New-Item -ItemType Directory -Path "C:\Users\User\test_3dgrut\sparse\0" -Force

# Copiar algumas imagens para C:\Users\User\test_3dgrut\images\
```

### 2. Rodar COLMAP/GloMAP no Windows
Use o GloMAP GUI para gerar o sparse model em `C:\Users\User\test_3dgrut\`

### 3. Treinar com 3D GRUT no WSL
```bash
# No WSL Ubuntu
conda activate 3dgrut

# Treinar (apontando para pasta do Windows)
python ~/3dgrut/train.py \
  --config_name colmap \
  --data.path /mnt/c/Users/User/test_3dgrut \
  --output_dir /mnt/c/Users/User/test_3dgrut/output \
  --down_sample_factor 4 \
  --iterations 1000
```

**Tempo estimado**: 5-10 minutos

**Status**: [ ] Concluído

---

## 🎯 Integrar com GloMAP GUI

### Opção 1: GUI Detecta Automaticamente
A GUI do GloMAP vai procurar 3D GRUT em:
- `~/3dgrut/` (no WSL)
- `/mnt/c/Users/User/3dgrut/` (se instalado no Windows)

**Como testar**:
```powershell
# No PowerShell (Windows)
cd C:\Users\User\Documents\APLICATIVOS\GloMAP_GUI
python main.py

# Verificar log de startup - deve mostrar: "3DGUT: ✓"
```

### Opção 2: Configurar Path Manualmente
Se a GUI não detectar, edite `core/dgut_wrapper.py`:

```python
def _locate_dgut(self):
    # Adicionar path do WSL
    wsl_path = Path("/mnt/c/Users/User/3dgrut")  # Se instalado em C:\Users\User\3dgrut
    # OU
    wsl_path = Path.home() / "3dgrut"  # Se ~/3dgrut no WSL
    
    if wsl_path.exists():
        return wsl_path
    # ... resto do código
```

---

## 📊 Verificação Final

### Checklist Completo
- [ ] Ubuntu 22.04 instalado no WSL2
- [ ] Sistema atualizado (`sudo apt upgrade`)
- [ ] NVIDIA GPU detectada (`nvidia-smi`)
- [ ] CUDA 12.8 instalado (`nvcc --version`)
- [ ] Miniconda instalado (`conda --version`)
- [ ] 3D GRUT clonado (`~/3dgrut/`)
- [ ] 3D GRUT instalado (`./install_env.sh`)
- [ ] Import funciona (`import threedgrut`)
- [ ] Teste completo executado
- [ ] GloMAP GUI reconhece instalação

---

## 🐛 Troubleshooting WSL2

### GPU não detectada no WSL
```bash
# Verificar driver no Windows
# No PowerShell:
nvidia-smi
```
**Solução**: Atualizar driver NVIDIA no Windows para versão compatível com WSL2 (driver 470+)

### "CUDA not found" no WSL
```bash
# Verificar instalação
ls /usr/local/cuda-12.8/

# Adicionar ao PATH manualmente
export PATH=/usr/local/cuda-12.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH
```

### Conda muito lento
```bash
# Usar mamba (mais rápido)
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
```

### "Permission denied" ao executar script
```bash
chmod +x install_env.sh
./install_env.sh 3dgrut
```

---

## 🚀 Comandos Rápidos

### Abrir WSL Ubuntu
```powershell
# No PowerShell
wsl
# OU
wsl -d Ubuntu-22.04
```

### Sair do WSL
```bash
exit
# OU Ctrl+D
```

### Ver distribuições instaladas
```powershell
wsl --list --verbose
```

### Parar WSL
```powershell
wsl --shutdown
```

---

## 📞 Próximos Passos

1. **Aguarde instalação do Ubuntu terminar** (5-10 minutos)
2. **Configure username/password** quando solicitado
3. **Siga os passos 2-8** acima em sequência
4. **Teste com dados de amostra**
5. **Integre com GloMAP GUI**

---

**Tempo Total Estimado**: 30-60 minutos  
**Dificuldade**: Média  
**Taxa de Sucesso**: ~90%  

---

## 📚 Documentação Adicional

- `GUIA_3DGRUT_INSTALACAO.md` - Guia completo em português
- `INSTALL_3DGRUT_QUICKSTART.md` - Guia rápido em inglês
- `INSTALL_3DGRUT_WINDOWS_STEP_BY_STEP.md` - Instalação Windows nativa

---

*Última atualização: 2025-01-15*  
*Plataforma: WSL2 (Windows Subsystem for Linux)*
