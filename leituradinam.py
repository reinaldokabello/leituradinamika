import time
import os
import sys
import PyPDF2

def limpar_tela():
    os.system('clear' if os.name == 'posix' else 'cls')

def centralizar_texto(texto):
    """Centraliza a palavra no terminal."""
    try:
        linhas_terminal = os.get_terminal_size().lines
        colunas_terminal = os.get_terminal_size().columns
    except OSError:
        linhas_terminal, colunas_terminal = 24, 80  # Valores padrão caso `os.get_terminal_size()` falhe
    
    linhas_espaco = linhas_terminal // 2
    texto_formatado = f'\033[1m\033[4m{texto.upper()}\033[0m'  # Negrito e sublinhado
    texto_centralizado = '\n' * linhas_espaco + texto_formatado.center(colunas_terminal)
    return texto_centralizado

def ler_texto(arquivo):
    """Lê arquivos TXT ou PDF e retorna o conteúdo como string."""
    if not os.path.exists(arquivo):
        print("Arquivo não encontrado. Verifique o caminho.")
        sys.exit(1)
    
    if arquivo.lower().endswith('.pdf'):
        return ler_pdf(arquivo)
    else:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return f.read()

def ler_pdf(arquivo):
    """Extrai texto de um arquivo PDF."""
    texto = ""
    with open(arquivo, 'rb') as f:
        leitor = PyPDF2.PdfReader(f)
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""  # Garante que não retorne None
    return texto.strip()

def mostrar_palavras(texto, velocidade):
    """Mostra as palavras no terminal no ritmo especificado."""
    palavras = texto.split()
    intervalo = 60.0 / velocidade  # Tempo entre palavras em segundos

    for palavra in palavras:
        limpar_tela()
        print(centralizar_texto(palavra))
        try:
            time.sleep(intervalo)
        except KeyboardInterrupt:
            print("\nLeitura pausada. Pressione Enter para continuar ou Ctrl+C para sair.")
            input()
    
def main():
    """Função principal do programa."""
    if len(sys.argv) < 2:
        arquivo = input("Digite o caminho do arquivo TXT ou PDF: ").strip()
    else:
        arquivo = sys.argv[1]
    
    try:
        velocidade = int(input("Digite a velocidade (palavras por minuto): "))
        if velocidade <= 0:
            raise ValueError
    except ValueError:
        print("Entrada inválida! Usando 200 palavras por minuto.")
        velocidade = 200
    
    texto = ler_texto(arquivo)
    
    if not texto:
        print("O arquivo está vazio ou não pôde ser lido.")
        sys.exit(1)

    mostrar_palavras(texto, velocidade)

if __name__ == "__main__":
    main()
