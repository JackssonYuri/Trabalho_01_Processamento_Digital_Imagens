from PIL import Image
import numpy as np
import sys

def decodificar(imagem_entrada, plano_bits, texto_saida):
    # Abrir a imagem
    imagem = Image.open(imagem_entrada)
    dados = np.array(imagem)
    
    # Recuperar os bits da mensagem
    mensagem_bin = []
    h, w, _ = dados.shape
    for i in range(h):
        for j in range(w):
            for k in range(3):  # Canais RGB
                bit_mensagem = (dados[i, j, k] >> plano_bits) & 1
                mensagem_bin.append(str(bit_mensagem))
    
    # Agrupar os bits em bytes e converter para caracteres
    mensagem = []
    for i in range(0, len(mensagem_bin), 8):  # Lê 8 bits por vez
        byte = ''.join(mensagem_bin[i:i+8])
        if byte == '00000000':  # Marcador de fim da mensagem
            break
        mensagem.append(chr(int(byte, 2)))
    
    mensagem = ''.join(mensagem)  # Junta todos os caracteres
    
    # Salvar a mensagem em um arquivo
    with open(texto_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(mensagem)
    print(f"Mensagem recuperada com sucesso em {texto_saida}")

if __name__ == "__main__":
    # Leitura dos argumentos
    imagem_entrada = sys.argv[1]
    plano_bits = int(sys.argv[2])
    texto_saida = sys.argv[3]
    
    # Chamada da função
    decodificar(imagem_entrada, plano_bits, texto_saida)
