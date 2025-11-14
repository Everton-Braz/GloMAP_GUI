# Guia de Instalação do 3D GRUT: Do Zero aos Seus Primeiros Resultados

## Introdução: O Que é 3D GRUT e Por Que é Revolucionário?

Imagine criar uma cena 3D completa e detalhada usando uma câmera olho de peixe, capturando tudo com apenas um terço do número de imagens que você normalmente precisaria. Essa é a magia do **3D GRUT** da NVIDIA, um avanço revolucionário na tecnologia de Splatting Gaussiano.

Para um iniciante, o benefício é imenso e imediato:
- ✅ Capture cenas inteiras com **muito menos imagens**
- ✅ Suporte nativo para **lentes olho de peixe** (180-220° FOV)
- ✅ Correção inteligente de **distorção e rolling shutter**
- ✅ **Ray tracing** para qualidade superior

Este guia irá acompanhá-lo em cada etapa do processo, desde a configuração do seu ambiente até o treinamento e a visualização do seu primeiro modelo.

---

## 1. Preparando o Ambiente: Pré-requisitos Essenciais

### Sistema Operacional

**Linux** é a plataforma oficialmente suportada. 

> ⚠️ **Nota para Usuários Windows**: O suporte oficial está "chegando em breve". A comunidade já conseguiu instalar e executar no Windows de forma não oficial (veja Issues no GitHub), mas com limitações:
> - ✅ Treinamento funciona (especialmente com fisheye)
> - ❌ Visualizador interativo pode não funcionar
> - ❌ Playground definitivamente não funciona

### Requisitos de Sistema

Antes de começar, certifique-se de que seu sistema atende aos seguintes requisitos:

#### 1. **CUDA Toolkit 11.8 ou superior**
```bash
nvcc --version
```

Saída esperada:
```
Cuda compilation tools, release 11.8, V11.8.89
```

#### 2. **Compilador GCC 11 ou 12**
```bash
gcc --version
```

Saída esperada:
```
gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
```

#### 3. **Hardware Recomendado**
- **GPU**: NVIDIA RTX 3080 ou superior (16GB+ VRAM recomendado)
- **RAM**: 32GB+ para conjuntos grandes de imagens
- **Storage**: SSD com espaço suficiente para datasets

---

## 2. Instalação do 3D GRUT: Escolha o Seu Caminho

### 2.1. O Caminho Fácil: Para CUDA 11.8 ou 12.8 ✅ RECOMENDADO

Este é o método mais simples se você tiver **exatamente** CUDA 11.8 ou 12.8.

```bash
# 1. Clone o repositório
git clone https://github.com/nv-tlabs/3dgrut.git
cd 3dgrut

# 2. Execute o instalador automático
./install.sh
```

O script cuidará de tudo automaticamente!

### 2.2. O Caminho Manual: Para Outras Versões do CUDA (ex: 12.4)

Se você possui uma versão diferente do CUDA (como 12.4), use este método que força a compilação com o toolkit 11.8:

```bash
# 1. Clone e entre no diretório
git clone https://github.com/nv-tlabs/3dgrut.git
cd 3dgrut

# 2. Defina a variável de ambiente do CUDA
export CUDA_HOME=/usr/local/cuda-11.8

# 3. Crie e ative um ambiente Conda
conda create -n 3dgrut python=3.10
conda activate 3dgrut

# 4. Exporte o caminho para as ferramentas de compilação
export PATH=/usr/local/cuda-11.8/bin:$PATH

# 5. Execute a instalação
./install.sh
```

> 💡 **Por que isso funciona?** O script install.sh é configurado especificamente para CUDA 11.8/12.8. Ao definir `CUDA_HOME`, forçamos a compilação a usar o toolkit correto.

### 2.3. O Caminho do Docker: Para Amantes de Contêineres 🐳

Para usuários familiarizados com Docker:

```bash
# 1. Construa a imagem
docker build -t 3dgrut .

# 2. Execute o contêiner
docker run --gpus all -it 3dgrut
```

**Pré-requisito**: NVIDIA Docker Toolkit instalado.

---

## 3. Preparando Seus Dados com o COLMAP

Antes do treinamento, suas imagens precisam ser processadas pelo **COLMAP** para estimar posições de câmera e criar uma nuvem de pontos 3D inicial.

### 3.1. Estrutura de Pastas

Organize seus arquivos assim:

```
meu_projeto/
├── images/              # Suas fotos aqui
│   ├── IMG_001.jpg
│   ├── IMG_002.jpg
│   └── ...
├── database.db          # Será criado pelo COLMAP
└── sparse/
    └── 0/               # Modelo 3D será salvo aqui
```

### 3.2. Processamento no COLMAP GUI

#### Passo 1: Inicie o COLMAP
```bash
colmap gui
```

#### Passo 2: Crie um Novo Projeto
1. Menu: **Arquivo → Novo projeto**
2. **Banco de Dados**: Clique em **Selecionar** → Salve `database.db` na pasta do projeto
3. **Imagens**: Clique em **Selecionar** → Aponte para a pasta `images`
4. Clique em **Salvar**

#### Passo 3: Extraia as Características
1. Menu: **Processamento → Extração de características**
2. **CRUCIAL**: Selecione o modelo de câmera correto:
   - Para **lentes olho de peixe**: `OPENCV_FISHEYE`
   - Para **lentes padrão**: `PINHOLE`
3. Clique em **Extrair**

#### Passo 4: Combine as Características
1. Menu: **Processamento → Casamento de características**
2. Escolha o método:
   - **Exaustivo**: Para fotos não sequenciais (melhor qualidade)
   - **Sequencial**: Para quadros de vídeo (mais rápido)
3. Clique em **Executar**

#### Passo 5: Reconstrução 3D
1. Menu: **Processamento → Reconstrução → Iniciar reconstrução**
2. Aguarde o processo (você verá a nuvem de pontos sendo construída em tempo real)

#### Passo 6: Exporte o Modelo
1. Menu: **Arquivo → Exportar modelo como texto**
2. Salve em: `meu_projeto/sparse/0/`
3. Arquivos gerados: `cameras.txt`, `points3D.txt`, `images.txt`

> 💡 **Dica**: O COLMAP pode levar de minutos a horas dependendo do número de imagens e da resolução.

---

## 4. Treinando o Seu Primeiro Modelo 3D GRUT

### 4.1. Comando Básico de Treinamento

```bash
python train.py \
    --config_name colmap \
    --data.path /caminho/para/meu_projeto \
    --output_dir runs/meu_primeiro_modelo \
    --down_sample_factor 2 \
    --with_gui true \
    --export_ply_enabled true
```

### 4.2. Parâmetros Explicados

| Parâmetro | Descrição | Valores Comuns |
|-----------|-----------|----------------|
| `--config_name` | Tipo de configuração | `colmap`, `mcmc` |
| `--data.path` | Pasta do projeto (contém `images` e `sparse`) | `/path/to/project` |
| `--output_dir` | Onde salvar o modelo treinado | `runs/meu_modelo` |
| `--down_sample_factor` | Redução de resolução (2 = metade) | `1` (full), `2` (rápido), `4` (muito rápido) |
| `--with_gui` | Abre visualizador em tempo real | `true` / `false` |
| `--export_ply_enabled` | Exporta arquivo PLY ao final | `true` / `false` |

### 4.3. Exemplo para Câmera Olho de Peixe

```bash
python train.py \
    --config_name colmap \
    --data.path /dados/sala_fisheye \
    --output_dir runs/sala_fisheye_modelo \
    --down_sample_factor 1 \
    --with_gui true \
    --export_ply_enabled true
```

### 4.4. ⚠️ IMPORTANTE: Iniciando o Treinamento

Ao usar `--with_gui true`:
1. A janela do visualizador abrirá
2. **O treinamento NÃO inicia automaticamente!**
3. Você DEVE marcar a caixa **"Train"** no canto superior direito
4. Apenas então o treinamento começará

### 4.5. Monitorando o Progresso

Durante o treinamento, você verá:
- Número de iterações
- Perda (loss) - deve diminuir com o tempo
- FPS de renderização
- Visualização em tempo real da cena

**Tempo esperado**: 30-90 minutos em RTX 4090 para ~100 imagens

---

## 5. Visualizando Seus Resultados

### 5.1. Carregando um Modelo Treinado

Após o treinamento (ou ao interrompê-lo), um checkpoint é salvo. Para visualizar:

```bash
python train.py \
    --config_name colmap \
    --data.path /caminho/para/meu_projeto \
    --eval \
    --gui.on \
    --resume_from runs/meu_primeiro_modelo/checkpoint_latest.pth
```

### 5.2. Navegação no Visualizador

1. **Mude o estilo da câmera**: Em "Camera Style", selecione **"First Person"**
2. **Controles**:
   - **W/A/S/D**: Mover para frente/esquerda/trás/direita
   - **Q/E**: Subir/descer
   - **Mouse**: Rotacionar a visão
   - **Scroll**: Zoom

### 5.3. Renderizando Imagens

Para gerar imagens de alta qualidade:

```bash
python render.py \
    --config_name colmap \
    --data.path /caminho/para/meu_projeto \
    --checkpoint runs/meu_primeiro_modelo/checkpoint_latest.pth \
    --output_dir renders/
```

---

## 6. Integração com a GUI do GloMAP

Esta GUI do GloMAP já possui **integração completa** com 3D GRUT!

### 6.1. Configurando o Caminho

Edite o arquivo `core/dgut_wrapper.py`:

```python
def __init__(self, dgut_path=None):
    if dgut_path is None:
        dgut_path = "/caminho/para/3dgrut"  # Ajuste aqui
    self.dgut_path = dgut_path
```

### 6.2. Usando a Interface

1. **Execute a GUI**: `python main.py`
2. **Selecione imagens e projeto**
3. **Para fisheye**:
   - Marque "Enable Fisheye Camera Mode"
   - Selecione "OPENCV_FISHEYE"
4. **Para 3D GRUT**:
   - Execute primeiro "Run Complete Pipeline" (cria sparse com COLMAP)
   - Marque "Enable 3DGUT"
   - Configure iterações (30000 recomendado)
   - Clique "Run 3DGUT"

---

## 7. Solução de Problemas Comuns

### Erro: "Config name mismatch"
**Causa**: O config usado na visualização difere do treinamento.
**Solução**: Use o mesmo `--config_name` em ambos os comandos.

### Erro: "CUDA out of memory"
**Causa**: GPU sem memória suficiente.
**Soluções**:
- Aumente `--down_sample_factor` para 2 ou 4
- Reduza o número de imagens
- Use uma GPU com mais VRAM

### Visualizador não abre no Windows
**Causa**: Suporte Windows ainda não oficial.
**Solução**: 
- Use WSL2 (Windows Subsystem for Linux)
- Ou treine sem GUI: `--with_gui false`

### Treinamento muito lento
**Soluções**:
- Use `--down_sample_factor 2` para reduzir resolução
- Certifique-se de que CUDA está instalado corretamente
- Verifique se a GPU está sendo usada: `nvidia-smi`

---

## 8. Dicas e Truques Avançados

### 8.1. Otimizando para Fisheye

Para obter os melhores resultados com câmeras olho de peixe:

1. **No COLMAP**: Use `OPENCV_FISHEYE` (melhor para >180° FOV)
2. **Capture com sobreposição**: 80-90% de overlap entre imagens
3. **Evite extremidades**: Não coloque objetos importantes nas bordas extremas

### 8.2. Configuração MCMC (Melhor Qualidade)

Para qualidade superior (mas mais lento):

```bash
python train.py \
    --config_name mcmc \
    --data.path /caminho/projeto \
    --output_dir runs/mcmc_modelo \
    --with_gui true
```

MCMC usa otimização estocástica para melhor distribuição de Gaussianas.

### 8.3. Exportando para Outros Softwares

O arquivo PLY gerado pode ser importado em:
- **CloudCompare**: Visualização de nuvens de pontos
- **MeshLab**: Processamento de malhas
- **Blender**: Modelagem 3D
- **Unity/Unreal**: Engines de jogos

---

## 9. Comparação de Performance

### Tempo de Processamento (100 imagens fisheye, RTX 4090)

| Etapa | COLMAP Tradicional | GloMAP + 3D GRUT |
|-------|-------------------|------------------|
| Feature Extraction | 5-10 min | 5-10 min |
| Feature Matching | 10-20 min | 10-20 min |
| Sparse Reconstruction | 30-60 min | **2-5 min** ⚡ |
| Dense/3D GRUT | 2-3 horas | **30-60 min** ⚡ |
| **TOTAL** | **~3-4 horas** | **~50-90 min** ⚡ |

**Economia de tempo: 3-5x mais rápido!**

### Qualidade (métricas em dataset fisheye 200°)

| Método | PSNR | SSIM | LPIPS |
|--------|------|------|-------|
| Fisheye-GS | 20.05 | 0.72 | 0.39 |
| **3D GRUT** | **22.16** | **0.81** | **0.32** |

**Melhor qualidade em todos os aspectos!**

---

## 10. Recursos Adicionais

### Links Úteis

- 📄 **Paper**: https://research.nvidia.com/labs/toronto-ai/3DGUT/
- 💻 **Código**: https://github.com/nv-tlabs/3dgrut
- 📚 **COLMAP Docs**: https://colmap.github.io/
- 🎥 **Tutorial em Vídeo**: (procure no YouTube por "3D GRUT tutorial")

### Comunidade

- **Issues GitHub**: Reporte bugs ou peça ajuda
- **Discussions**: Compartilhe seus modelos e dicas

---

## Conclusão

Parabéns! 🎉 Você agora domina o fluxo de trabalho completo do 3D GRUT:

✅ Instalação e configuração do ambiente
✅ Processamento de dados com COLMAP
✅ Treinamento de modelos com fisheye
✅ Visualização e renderização
✅ Integração com a GUI do GloMAP

Você está pronto para criar cenas 3D incríveis com a flexibilidade de lentes grande-angulares e a velocidade do GloMAP!

### Próximos Passos

1. **Experimente com seus próprios dados**
2. **Teste diferentes configurações** (MCMC, diferentes resoluções)
3. **Compare resultados** entre métodos tradicionais e 3D GRUT
4. **Compartilhe seus resultados** com a comunidade!

**Boas criações! 🚀**

---

*Última atualização: Outubro 2025*
*Versão GUI: 1.0 com suporte completo a fisheye e 3D GRUT*
