# 3D GRUT Installation Checklist

Use esta checklist para instalar e testar o 3D GRUT no seu sistema.

---

## 📋 Pré-Requisitos

### Verificar Sistema
- [ ] Sistema operacional: Linux ou WSL2 (Windows)
- [ ] Placa NVIDIA instalada
- [ ] Driver NVIDIA atualizado

### Verificar Comandos (Linux/WSL2)
```bash
# 1. Verificar GPU NVIDIA
nvidia-smi
# ✓ Deve mostrar informações da GPU (nome, memória, driver)

# 2. Verificar CUDA
nvcc --version
# ✓ Deve mostrar CUDA 11.8 ou superior

# 3. Verificar GCC
gcc --version
# ✓ Deve mostrar GCC 11 ou 12

# 4. Verificar Python
python --version
# ✓ Deve mostrar Python 3.10 ou superior
```

### Resultado dos Comandos Acima:
```
[ ] nvidia-smi: _________________ (escreva o modelo da GPU)
[ ] nvcc: CUDA versão _________ (ex: 12.8)
[ ] gcc: versão _________
[ ] python: versão _________
```

---

## 🚀 Instalação do 3D GRUT

### Passo 1: Clone o Repositório
```bash
cd ~
git clone https://github.com/nv-tlabs/3dgrut
cd 3dgrut
```
- [ ] Repositório clonado com sucesso
- [ ] Diretório `~/3dgrut` existe

### Passo 2: Configurar CUDA (se necessário)
```bash
# Apenas se sua versão CUDA não for 11.8 ou 12.8
export CUDA_HOME=/usr/local/cuda-XX.X  # Substitua XX.X pela sua versão
echo 'export CUDA_HOME=/usr/local/cuda-XX.X' >> ~/.bashrc
source ~/.bashrc
```
- [ ] CUDA_HOME configurado (se necessário)
- [ ] Variável persiste após reabrir terminal

### Passo 3: Instalar 3D GRUT
```bash
cd ~/3dgrut
./install.sh
```
- [ ] Script executou sem erros
- [ ] Instalação concluída (veja mensagem de sucesso)

### Passo 4: Verificar Instalação
```bash
# Verificar pacote Python
python -c "import dgut; print('3D GRUT OK!')"

# Verificar scripts
ls ~/3dgrut/train.py
ls ~/3dgrut/render.py
ls ~/3dgrut/viewer.py
```
- [ ] Importação Python funcionou
- [ ] Arquivos `train.py`, `render.py`, `viewer.py` existem

---

## 🧪 Teste Rápido

### Passo 5: Preparar Dados de Teste
```bash
# Criar estrutura
mkdir -p ~/test_3dgrut/images
mkdir -p ~/test_3dgrut/sparse/0

# Copiar imagens de teste (20-50 imagens recomendado)
# Você pode usar imagens de qualquer projeto
```
- [ ] Pasta de teste criada
- [ ] Imagens copiadas para `~/test_3dgrut/images/`

### Passo 6: Gerar Sparse Model (COLMAP/GloMAP)
**Opção A: Via GloMAP GUI**
1. Abra o GloMAP GUI: `python main.py`
2. Selecione pasta `~/test_3dgrut`
3. Coloque imagens em `~/test_3dgrut/images/`
4. Clique "Run Complete Pipeline"
5. Aguarde sparse reconstruction

**Opção B: Via COLMAP direto**
```bash
colmap feature_extractor --database_path ~/test_3dgrut/database.db --image_path ~/test_3dgrut/images
colmap exhaustive_matcher --database_path ~/test_3dgrut/database.db
colmap mapper --database_path ~/test_3dgrut/database.db --image_path ~/test_3dgrut/images --output_path ~/test_3dgrut/sparse
```
- [ ] Sparse model gerado em `~/test_3dgrut/sparse/0/`
- [ ] Arquivos `cameras.bin`, `images.bin`, `points3D.bin` existem

### Passo 7: Treinar Modelo 3D GRUT (Teste Rápido)
```bash
cd ~/3dgrut
python train.py \
  --config_name colmap \
  --data.path ~/test_3dgrut \
  --output_dir ~/test_3dgrut/output \
  --down_sample_factor 4 \
  --iterations 1000
```
**Tempo estimado**: 2-5 minutos  
**Observações durante treinamento**:
- [ ] Treinamento iniciou sem erros
- [ ] Log mostra progresso (iterations, loss, etc.)
- [ ] GPU sendo utilizada (verificar com `nvidia-smi` em outro terminal)

### Passo 8: Verificar Resultados
```bash
# Verificar arquivos gerados
ls ~/test_3dgrut/output/

# Deve conter:
# - *.ply (nuvem de pontos)
# - checkpoints/ (modelo salvo)
# - logs/ (registros de treinamento)
```
- [ ] Arquivo PLY gerado
- [ ] Pasta checkpoints/ existe
- [ ] Logs de treinamento salvos

---

## 🎨 Teste na GloMAP GUI

### Passo 9: Abrir GloMAP GUI
```bash
cd /caminho/para/GloMAP_GUI
python main.py
```
- [ ] GUI abriu sem erros
- [ ] Log inicial mostra "3DGUT: ✓" (não "✗")

### Passo 10: Testar 3D GRUT na GUI
1. **Carregar Projeto**:
   - [ ] Clique "Select Folder"
   - [ ] Escolha `~/test_3dgrut`

2. **Configurar 3D GRUT**:
   - [ ] Marque checkbox "Enable 3D GRUT"
   - [ ] Selecione "Use MCMC" (para melhor qualidade)
   - [ ] Defina "Iterations": 10000 (teste rápido)
   - [ ] Marque "Export PLY"

3. **Executar**:
   - [ ] Clique "✨ Run 3DGUT"
   - [ ] Confirme na caixa de diálogo
   - [ ] Observe progresso no log em tempo real

4. **Verificar Resultados**:
   - [ ] Treinamento concluiu sem erros
   - [ ] Mensagem "✓ 3DGUT TRAINING COMPLETED!" apareceu
   - [ ] Arquivo PLY gerado em `~/test_3dgrut/dgut/`

---

## 🔍 Solução de Problemas

### Se "3D GRUT not found" na GUI
1. Verificar instalação:
   ```bash
   ls ~/3dgrut/train.py
   ls ~/3DGUT/train.py  # Alternativa
   ```
2. Se não encontrar, reinstalar:
   ```bash
   cd ~/3dgrut
   ./install.sh
   ```

### Se "CUDA out of memory"
1. Aumentar `down_sample_factor`:
   - Na GUI: editar código (não tem UI para isso ainda)
   - No terminal: usar `--down_sample_factor 8`

2. Fechar outros programas que usam GPU

### Se treinamento trava
1. Verificar driver:
   ```bash
   nvidia-smi
   dmesg | tail -20  # Ver erros recentes
   ```

2. Tentar com menos imagens (10-20 inicialmente)

### Se qualidade ruim
1. Verificar sparse model no COLMAP GUI
2. Aumentar iterations (30000+)
3. Usar MCMC config
4. Usar resolução maior (down_sample_factor 2 ou 1)

---

## ✅ Checklist Final

### Instalação
- [ ] 3D GRUT instalado em `~/3dgrut/`
- [ ] Pacote Python importa sem erro
- [ ] Scripts `train.py`, `render.py`, `viewer.py` existem

### Teste Terminal
- [ ] Treinamento rápido (1000 iter) funcionou
- [ ] PLY gerado corretamente
- [ ] Logs mostram progresso

### Teste GUI
- [ ] GUI reconhece 3D GRUT (mostra ✓)
- [ ] Botão "✨ Run 3DGUT" funciona
- [ ] Treinamento completa sem travar
- [ ] Resultados salvos corretamente

### Produção
- [ ] Testado com dataset completo (50+ imagens)
- [ ] MCMC produz resultados de qualidade
- [ ] PLY visualiza corretamente no CloudCompare/MeshLab

---

## 📚 Documentação de Referência

| Arquivo | Propósito |
|---------|-----------|
| `INSTALL_3DGRUT_QUICKSTART.md` | Guia rápido (inglês) |
| `GUIA_3DGRUT_INSTALACAO.md` | Guia completo (português) |
| `3DGRUT_IMPLEMENTATION_COMPLETE.md` | Detalhes técnicos |
| `IMPLEMENTATION_SUMMARY.md` | Resumo executivo |

---

## 🎯 Próximos Passos

Após completar esta checklist:

1. **Teste com seus próprios dados**:
   - Use um dataset pequeno primeiro (20-50 imagens)
   - Verifique qualidade dos resultados
   - Ajuste parâmetros conforme necessário

2. **Explore funcionalidades**:
   - Viewer interativo: `python viewer.py --model path/to/model`
   - Renderização customizada: `python render.py --model path/to/model`
   - Exportar diferentes formatos

3. **Otimize workflow**:
   - Determine melhores parâmetros para seus casos
   - Configure presets na GUI
   - Documente seu pipeline

---

**Data**: ___/___/2025  
**Testado por**: _________________  
**Sistema**: Linux / WSL2 (circule)  
**GPU**: _________________  
**Status Final**: ✅ Funcionando / ⚠️ Parcial / ❌ Não funcionou

---

*Checklist v1.0 - Use este documento para rastrear seu progresso de instalação*
