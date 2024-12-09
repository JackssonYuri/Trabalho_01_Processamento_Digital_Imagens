from PIL import Image
import numpy as np
import argparse

def codificar(imagem_entrada, texto_entrada, plano_bits, imagem_saida):
    imagem = Image.open(imagem_entrada)
    dados = np.array(imagem)

    # Read image
    with open(texto_entrada, 'r', encoding='utf-8') as arquivo:
        mensagem = arquivo.read()

    # Convert image to binary (ASCII) and add a end mark
    mensagem_bin = ''.join(f'{ord(c):08b}' for c in mensagem) + '00000000' 
    
    # Check image capacity
    h, w, _ = dados.shape
    capacidade = h * w * 3
    if len(mensagem_bin) > capacidade:
        raise ValueError("A mensagem é muito grande para ser embutida nesta imagem.")
    
    # Insert message bits into least significant bits
    mensagem_idx = 0
    for i in range(h):
        for j in range(w):
            for k in range(3):  # RGB Channels
                if mensagem_idx < len(mensagem_bin):
                    bit_mensagem = int(mensagem_bin[mensagem_idx])
                    mascara = 255 ^ (1 << plano_bits)  
                    dados[i, j, k] = np.uint8((dados[i, j, k] & mascara) | (bit_mensagem << plano_bits))
                    mensagem_idx += 1
    
    # Save the new image with the message 
    nova_imagem = Image.fromarray(dados)
    nova_imagem.save(imagem_saida)
    print(f"Mensagem embutida com sucesso em {imagem_saida}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script para codificação da mensagem em uma imagem')

    parser.add_argument('imagem_entrada', type=str, help = 'Imagem de entrada para ser decodificada')
    parser.add_argument('texto_entrada', type=str, help = 'Texto de entrada')
    parser.add_argument('plano_bits', type=int, help = 'Plano de bits')
    parser.add_argument('imagem_saida', type=str, help = 'Imagem de saída')

    args = parser.parse_args()
    
    codificar(args.imagem_entrada, args.texto_entrada, args.plano_bits, args.imagem_saida)
