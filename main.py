from fastapi import FastAPI, Request
import mercadopago
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

app = FastAPI()

# SDK Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN = "APP_USR-8438761570151366-052501-2b1464152ca6c810de0c205c8177e293-618673042"
sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)

# Global browser driver (para reaproveitar sessão)
driver = None

def iniciar_browser():
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # ou use headless se preferir
        service = Service(ChromeDriverManager().install())  # Use Service to handle the driver path
        driver = webdriver.Chrome(service=service, options=options)  # Pass service and options
    return driver

def renovar_cliente_sistema(id_cliente):
    driver = iniciar_browser()

    # 1. Abre a URL do sistema (login automático via extensão/cookie)
    driver.get("https://onlineoffice.zip/#/login")  # substitua pela sua URL

    print("🔐 Preenchendo login...")
    time.sleep(2)

    # 2. Preenche os campos de login
    usuario = driver.find_element(By.XPATH, '//input[contains(@placeholder, "Usuário")]')
    senha = driver.find_element(By.XPATH, '//input[contains(@placeholder, "Senha")]')
    usuario.send_keys("leoschneider1")
    senha.send_keys("Grenal1")

    # 2. Aguarda 3 minutos para login via extensão quebrar captcha
    print("⏳ Aguardando 3 minutos para login automático via extensão...")
    #time.sleep(180)
    botao_login = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary.my-4')
    botao_login.click()
    print("🔑 Login realizado com sucesso!")


    # 3. Busca o ID do cliente
    print(f"🔍 Buscando cliente {id_cliente}...")
    driver.get("https://onlineoffice.zip/#/users-iptv")
    time.sleep(5)
    campo_busca = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Pesquisar usuário"')  # Substitua pelo ID real
    campo_busca.clear()
    campo_busca.send_keys(533340379)

    # 4. Aguarda carregar resultado e clica no botão de renovação
    time.sleep(1)
    botao_renovar = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-outline-warning.btn-sm")  # Substitua pelo ID real
    botao_renovar.click()

    print(f"✅ Cliente {id_cliente} renovado com sucesso!")

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    print(f"📩 Webhook recebido: {payload}")

    if payload.get("type") == "payment":
        payment_id = payload.get("data", {}).get("id")
        payment_info = sdk.payment().get(payment_id)

        if payment_info["status"] == 200:
            status = payment_info["response"]["status"]
            external_reference = payment_info["response"].get("external_reference")

            if status == "approved" and external_reference:
                print(f"✅ Pagamento aprovado para {external_reference}")
                
                # Agora aciona o processo de renovação via navegador
                renovar_cliente_sistema(external_reference)

    return {"status": "received"}


if __name__ == "__main__":
    # Teste manual
    id_para_testar = "123456"  # Substitua por um ID real de cliente
    renovar_cliente_sistema(id_para_testar)