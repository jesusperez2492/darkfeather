# 🦅 DarkFeather - Wireless Connection PRO

DarkFeather é uma ferramenta gráfica desenvolvida em Python com Tkinter para visualizar e extrair informações detalhadas das redes Wi-Fi salvas no sistema Windows.

## 📋 Funcionalidades

- Visualização de todas as redes Wi-Fi salvas no Windows.
- Extração da senha (ASCII e HEX), autenticação, criptografia e tipo de conexão.
- Identificação do nome do adaptador de rede e seu GUID.
- Exibição do caminho do arquivo de perfil e data da última modificação.
- Interface gráfica moderna em modo escuro.
- Janela de cópia rápida com botão **📋 Copiar** para facilitar o compartilhamento das informações.
- Botão "🔍 Buscar e Atualizar" para escanear e exibir as redes.
- Botão "🧹 Resetar UI" para limpar a exibição.

## 💻 Requisitos

- **Sistema Operacional**: Windows
- **Python**: 3.7 ou superior
- **Bibliotecas Python**:
  - `tkinter` (padrão no Python)
  - `wmi`

Para instalar o `wmi`, execute:
```bash
pip install wmi
````

## 🚀 Como Usar

1. **Clone o repositório** ou copie os arquivos para sua máquina:

```bash
git clone https://github.com/seu-usuario/darkfeather.git
cd darkfeather
```

2. **Execute o script principal** como administrador:

```bash
python darkfeather.py
```

> O script exige privilégios administrativos para acessar os perfis de rede do sistema (`netsh` e arquivos XML do Windows).

3. Clique em **🔍 Buscar e Atualizar** para listar todas as redes salvas.
4. Dê **duplo clique** em qualquer campo para abrir uma janela com botão de copiar.

## 📂 Estrutura do Projeto

```
darkfeather/
├── darkfeather.py         # Script principal com a interface e lógica
├── README.md              # Este arquivo
```

## 🔒 Segurança

Esta ferramenta **não invade redes**, apenas exibe dados salvos **localmente no seu próprio sistema**. Ideal para técnicos, profissionais de suporte ou curiosos sobre redes que já foram conectadas.

## 🧠 Motivação

Inspirado por ferramentas como *WirelessKeyView*, o **DarkFeather** visa fornecer uma alternativa moderna, open-source, e em português — com visual agradável e controle total das informações.

## 🐍 Autor

**Eduardo dos Santos Ferreira**
Desenvolvedor Python | Cibersegurança | Sistemas e Automação
[LinkedIn](https://linkedin.com/in/eduardo-dos-santos-ferreira) • GitHub: [@eduardodossantosferreira](https://github.com/eduardodossantosferreira)

## 📜 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```

---

Você pode salvar esse conteúdo em um arquivo chamado `README.md` e colocá-lo junto do seu `darkfeather.py`.

Quer que eu gere também uma [versão com imagem e badges do GitHub](f), um [modelo LICENSE MIT](f), ou um [executável `.exe` com ícone e tudo](f)?
```
