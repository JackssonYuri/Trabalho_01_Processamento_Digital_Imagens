from PIL import Image
import numpy as np
import sys

def codificar(imagem_entrada, texto_entrada, plano_bits, imagem_saida):
    # Abrir a imagem
    imagem = Image.open(imagem_entrada)
    dados = np.array(imagem)

    # Ler a mensagem
    # Abrir a mensagem com UTF-8
    with open(texto_entrada, 'r', encoding='utf-8') as arquivo:
        mensagem = arquivo.read()

    
    # Converter mensagem em binário (ASCII)
    mensagem_bin = ''.join(f'{ord(c):08b}' for c in mensagem) + '00000000'  # Adiciona marcador de fim
    
    # Verificar capacidade da imagem
    h, w, _ = dados.shape
    capacidade = h * w * 3
    if len(mensagem_bin) > capacidade:
        raise ValueError("A mensagem é muito grande para ser embutida nesta imagem.")
    
    # Inserir os bits da mensagem nos bits menos significativos
    mensagem_idx = 0
    for i in range(h):
        for j in range(w):
            for k in range(3):  # Canais RGB
                if mensagem_idx < len(mensagem_bin):
                    bit_mensagem = int(mensagem_bin[mensagem_idx])
                    mascara = 255 ^ (1 << plano_bits)  # Máscara para preservar os bits sem gerar números negativos
                    dados[i, j, k] = np.uint8((dados[i, j, k] & mascara) | (bit_mensagem << plano_bits))
                    mensagem_idx += 1
    
    # Salvar a nova imagem com a mensagem embutida
    nova_imagem = Image.fromarray(dados)
    nova_imagem.save(imagem_saida)
    print(f"Mensagem embutida com sucesso em {imagem_saida}")

if __name__ == "__main__":
    # Leitura dos argumentos
    imagem_entrada = sys.argv[1]
    texto_entrada = sys.argv[2]
    plano_bits = int(sys.argv[3])
    imagem_saida = sys.argv[4]
    
    # Chamada da função
    codificar(imagem_entrada, texto_entrada, plano_bits, imagem_saida)
