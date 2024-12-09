from PIL import Image
import numpy as np
import argparse


def decodificar(imagem_entrada, plano_bits, texto_saida):
    imagem = Image.open(imagem_entrada)
    dados = np.array(imagem)
    
    # Recover message bits
    mensagem_bin = []
    h, w, _ = dados.shape
    for i in range(h):
        for j in range(w):
            for k in range(3):  # Canais RGB
                bit_mensagem = (dados[i, j, k] >> plano_bits) & 1
                mensagem_bin.append(str(bit_mensagem))
    
    # Group the bits into bytes and convert to characters
    mensagem = []
    for i in range(0, len(mensagem_bin), 8):  # Read 8 bits 
        byte = ''.join(mensagem_bin[i:i+8])
        if byte == '00000000':  # Find the end mark so end 
            break
        mensagem.append(chr(int(byte, 2)))
    
    mensagem = ''.join(mensagem)  
    
    # Save the image in texto_saida
    with open(texto_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(mensagem)
    print(f"Mensagem recuperada com sucesso em {texto_saida}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script para decodificação da mensagem em uma imagem')

    parser.add_argument('imagem_entrada', type=str, help='Imagem de entrada para ser decodificada')
    parser.add_argument('plano_bits', type=int, help='Plano de Bits')
    parser.add_argument('texto_saida', type=str, help='Texto de saída')
    args = parser.parse_args()
    
    decodificar(args.imagem_entrada, args.plano_bits, args.texto_saida)
