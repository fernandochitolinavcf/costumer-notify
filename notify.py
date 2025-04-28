import pandas as pd
from datetime import datetime, timedelta
from twilio.rest import Client
import mercadopago
import uuid
import json

EXCEL_PATH = "UsersIPTV.xlsx"
DIAS_ANTES = 1

# Credenciais Twilio (substitua pelas suas)
TWILIO_SID = "AC598475cef753bffe682162407eba98d6"
TWILIO_AUTH_TOKEN = "9918de6540b336f1fda520ca863aa807"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+15557382360"
#15557382360

# Inicializar cliente Twilio
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Credenciais Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN = "APP_USR-8438761570151366-052501-2b1464152ca6c810de0c205c8177e293-618673042"
sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)


def carregar_clientes(path=EXCEL_PATH):
    return pd.read_excel(path)


def salvar_clientes(df, path=EXCEL_PATH):
    df.to_excel(path, index=False)

def filtrar_clientes_para_notificar(df):
    hoje = datetime.today().date()
    limite_superior = hoje + timedelta(days=3)

    df['Vencimento'] = pd.to_datetime(df['Vencimento']).dt.date
    df_filtrado = df[(df['Vencimento'] <= limite_superior)]
    return df_filtrado


def gerar_link_pagamento_pix(usuario, telefone, valor=100.0):
    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': str(uuid.uuid4())
    }

    payment_data = {
        "installments": 1,
        "metadata": None,
        "payer": {
            "email": f"{telefone}@fake.com",
            "phone": {
                "area_code": "55",
                "number": telefone[-9:]
            },
        },
        "transaction_amount": valor,
        "description": f"Pagamento Mensalidade - {usuario}",
        "payment_method_id": "pix",
        "external_reference": usuario,
    }

    payment_response = sdk.payment().create(payment_data, request_options)

    if payment_response["status"] == 201:
        ticket_url = payment_response["response"]["point_of_interaction"]["transaction_data"]["ticket_url"]
        return ticket_url
    else:
        print(f"Erro ao gerar pagamento para {usuario}: {payment_response}")
        return None


def enviar_mensagem_whatsapp(numero_destino, link_pix):
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{numero_destino}",
        content_sid='HX695f1b8e7540c89b98b6016879169238',
        content_variables=json.dumps({
            '1': link_pix
        })
    )

    print(f"Mensagem enviada para {numero_destino}: SID {message.sid}")


def notificar_clientes(df_clientes):
    for index, row in df_clientes.iterrows():
        usuario = row['Usuário']
        telefone = row['Telefone']
        valor_mensalidade = row.get('Valor', 35.0)

        link_pix = gerar_link_pagamento_pix(usuario, str(telefone), valor=valor_mensalidade)

        if link_pix and telefone:            
            enviar_mensagem_whatsapp(telefone, link_pix)
            

