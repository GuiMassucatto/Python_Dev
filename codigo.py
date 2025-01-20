import flet as ft

def main(pagina):
    titulo = ft.Text("Guizap")

    chat = ft.Column()

    nome_usuario = ft.TextField(label="Digite seu Nome")

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]

        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat"))

        pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao = ft.ElevatedButton("Entrar no chat", on_click=entrar_chat)

    def enviar_mensagem(evento):
        pagina.pubsub.send_all({
            "texto": campo_mensagem.value,
            "usuario": nome_usuario.value,
            "tipo": "mensagem"
        })
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(label="Enviar Mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        popup.open = False
        pagina.remove(botao)
        pagina.remove(titulo)
        pagina.add(chat)
        pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem]))

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Bem vindo ao Guizap"),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar no Chat", on_click=entrar_popup)]
    )

    pagina.update()
    pagina.add(titulo)
    pagina.add(botao)

ft.app(target=main, view=ft.WEB_BROWSER)


