from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import time
import os

# ================= CONFIGURAÇÕES =================
ARQUIVO_PRODUTOS = "produtos.txt"
ARQUIVO_FEITOS = "produtos_feitos.txt" 
PASTA_IMAGENS = r"C:\Users\Marketing 2\Documents\PRODUTOS" 
# =================================================

def ler_produtos_feitos():
    if not os.path.exists(ARQUIVO_FEITOS):
        return []
    with open(ARQUIVO_FEITOS, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f.readlines()]

def marcar_como_feito(codigo):
    with open(ARQUIVO_FEITOS, "a", encoding="utf-8") as f:
        f.write(codigo + "\n")

def descobrir_caminho_imagem(codigo):
    """Procura o arquivo de imagem testando diferentes extensões comuns"""
    extensoes_para_testar = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]
    for ext in extensoes_para_testar:
        caminho = os.path.join(PASTA_IMAGENS, codigo + ext)
        if os.path.exists(caminho):
            return caminho, ext
    return None, None

def iniciar_automacao():
    produtos_feitos = ler_produtos_feitos()
    
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15) 
    
    driver.get("https://www.conexaodistribuidora.com.br/gestao/index.php?controller=AdminDashboard&token=42188b3298682ce317a6317b25c08986")
    input("Faça o login no site e, depois, pressione ENTER aqui no terminal para começar...")
    print("\n🚀 INICIANDO A AUTOMAÇÃO INTELIGENTE E ACELERADA...\n" + "="*40)

    if not os.path.exists(ARQUIVO_PRODUTOS):
        print(f"❌ Erro: O arquivo '{ARQUIVO_PRODUTOS}' não foi encontrado!")
        return

    with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    for linha in linhas:
        if not linha.strip() or ";" not in linha: 
            continue 
        
        codigo, descricao = linha.strip().split(";", 1)
        
        if codigo in produtos_feitos:
            print(f"⏩ Produto [{codigo}] já foi feito anteriormente. Pulando...")
            continue
            
        print(f"\n📦 INICIANDO PRODUTO: {codigo} - {descricao}")
        
        # Validação antecipada do arquivo de imagem local
        caminho_imagem, ext_encontrada = descobrir_caminho_imagem(codigo)
        if not caminho_imagem:
            print(f"   ⚠️ ERRO LOCAL: A foto para o produto [{codigo}] não foi encontrada na pasta com formato válido (.jpg, .png, etc).")
            print(f"   ⚠️ Ignorando produto para não alterar dados no site sem ter a foto correspondente.")
            continue
            
        try:
            # --- NAVEGAÇÃO INTELIGENTE (PULA MENUS SE JÁ ESTIVER NA TELA) ---
            try:
                # Tenta localizar o campo de busca direto com tolerância baixa (3 segundos)
                input_busca = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="form-product"]/div/div[1]/div[2]/div[3]/input'))
                )
                print(f"   ⚡ [{codigo}] Já estamos na listagem de produtos. Pulando cliques do menu lateral!")
            except:
                # Se não encontrar o campo imediatamente, faz a navegação padrão
                print(f"   ⏳ [{codigo}] Menu de produtos não detectado. Navegando pelo catálogo...")
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="maintab-AdminCatalog"]/a'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="subtab-AdminProducts"]/a'))).click()
                input_busca = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form-product"]/div/div[1]/div[2]/div[3]/input')))
            
            # --- FILTRO ---
            input_busca.clear()
            input_busca.send_keys(codigo)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitFilterButtonproduct"]'))).click()
            print(f"   ⏳ [{codigo}] Filtrando...")
            time.sleep(4) 
            
            # --- EDITAR PRODUTO ---
            print(f"   ✏️ [{codigo}] Acessando edição do produto...")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//table[@id="table-product"]/tbody/tr[1]/td[4]'))).click()
            
            print(f"   ⏳ [{codigo}] Carregando formulário...")
            time.sleep(3.5) 
            
            # --- NOME DO PRODUTO ---
            print(f"   📝 [{codigo}] Atualizando o nome principal...")
            input_nome = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="name_1"]')))
            input_nome.send_keys(Keys.CONTROL + "a")
            input_nome.send_keys(Keys.BACKSPACE)
            time.sleep(0.5) 
            input_nome.send_keys(descricao)
            time.sleep(0.8) 
            
            # --- SEO ---
            print(f"   🔎 [{codigo}] Configurando SEO...")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="link-Seo"]'))).click()
            time.sleep(1.5) 
            
            # Meta Título
            input_seo_titulo = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="meta_title_1"]')))
            input_seo_titulo.send_keys(Keys.CONTROL + "a")
            input_seo_titulo.send_keys(Keys.BACKSPACE)
            input_seo_titulo.send_keys(descricao)
            
            # Meta Descrição
            input_seo_desc = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="meta_description_1"]')))
            input_seo_desc.send_keys(Keys.CONTROL + "a")
            input_seo_desc.send_keys(Keys.BACKSPACE)
            input_seo_desc.send_keys(descricao)
            time.sleep(0.5)
            
            # Gerar URL Amigável
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="generate-friendly-url"]'))).click()
            time.sleep(1)
            
            # --- IMAGENS ---
            print(f"   🖼️ [{codigo}] Acessando aba Imagens...")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="link-Images"]'))).click()
            time.sleep(2) 
            
            # Legenda da Imagem
            print(f"   🖼️ [{codigo}] Ajustando legenda...")
            input_legenda = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="legend_1"]')))
            input_legenda.send_keys(Keys.CONTROL + "a")
            input_legenda.send_keys(Keys.BACKSPACE)
            input_legenda.send_keys(descricao)
            time.sleep(0.5)
            
            # Botão de Atualizar Legenda
            print(f"   ⏳ [{codigo}] Clicando em atualizar legenda e aguardando processamento...")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="product-images"]/div[2]/div[2]/div[3]/button'))).click()
            time.sleep(7) # Pausa estratégica estendida de 7 segundos para salvar a legenda com segurança
            
            # --- UPLOAD DA IMAGEM ---
            print(f"   📤 [{codigo}] Injetando arquivo da foto ({codigo}{ext_encontrada})...")
            input_arquivo_oculto = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
            input_arquivo_oculto.send_keys(caminho_imagem)
            time.sleep(1) 
            
            # Enviar arquivos
            print(f"   📤 [{codigo}] Enviando arquivo ao servidor...")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="file-upload-button"]'))).click()
            time.sleep(4) 
            
            # Salvar alterações do fluxo
            print(f"   💾 [{codigo}] Finalizando e salvando produto...")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="product-images"]/div[5]/button[1]'))).click()
            time.sleep(3) 
            
            # Registro de sucesso
            marcar_como_feito(codigo)
            print(f"   ✅ [{codigo}] CONCLUÍDO COM SUCESSO!")
            time.sleep(1) 
            
        except Exception as e:
            print(f"   ❌ ERRO AO PROCESSAR O PRODUTO [{codigo}]: {e}")
            print(f"   ⚠️ Ignorando e pulando para o próximo produto da lista...")
            time.sleep(2)

    print("\n" + "="*40 + "\n🏁 FIM DA AUTOMAÇÃO! Todos os produtos foram processados.")
    driver.quit()

if __name__ == "__main__":
    iniciar_automacao()