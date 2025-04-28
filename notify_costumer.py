from notify import carregar_clientes, filtrar_clientes_para_notificar, notificar_clientes

def main():
    df = carregar_clientes()
    clientes_para_notificar = filtrar_clientes_para_notificar(df)
    print("Clientes a serem notificados:")
    print(clientes_para_notificar)
    notificar_clientes(clientes_para_notificar)

if __name__ == "__main__":
    main()
