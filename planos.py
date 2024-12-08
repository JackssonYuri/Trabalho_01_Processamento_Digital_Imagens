from PIL import Image
import numpy as np
import sys


def visualizar_planos(imagem_entrada):
    try:
        # Abrir a imagem
        imagem = Image.open(imagem_entrada)
        dados = np.array(imagem)

        # Verificar se a imagem foi carregada corretamente
        if dados.ndim < 2:
            raise ValueError("Imagem inválida ou dados da imagem não carregados corretamente.")
        
        # Gerar imagens para os 3 planos de bits menos significativos
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
    # Verificação para garantir que um argumento foi passado
    if len(sys.argv) < 2:
        print("Uso: python vizualizar_planos.py <caminho_da_imagem>")
    else:
        # Leitura dos argumentos
        imagem_entrada = sys.argv[1]

        # Chamada da função
        visualizar_planos(imagem_entrada)
