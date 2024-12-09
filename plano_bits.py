from PIL import Image
import numpy as np
import argparse


def visualizar_planos(imagem_entrada):
    try:
        imagem = Image.open(imagem_entrada)
        dados = np.array(imagem)

        # Check if the image was loaded correctly
        if dados.ndim < 2:
            raise ValueError("Imagem inválida ou dados da imagem não carregados corretamente.")
        
        # Generate images for the 3 least significant bit planes
        for plano in range(3):
            try:
                plano_bits = (dados >> plano) & 1
                plano_imagem = (plano_bits * 255).astype('uint8')
                nova_imagem = Image.fromarray(plano_imagem)
                nova_imagem.save(f"plano_{plano}.png")
                print(f"Plano {plano} salvo como plano_{plano}.png")
            except Exception as e:
                print(f"Erro ao processar o plano {plano}: {e}")

    except Exception as e:
        print(f"Erro ao abrir ou processar a imagem '{imagem_entrada}': {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script para decodificação da mensagem em uma imagem')

    parser.add_argument('imagem_entrada', type=str, help='Imagem de entrada')
    args = parser.parse_args()

    visualizar_planos(args.imagem_entrada)
