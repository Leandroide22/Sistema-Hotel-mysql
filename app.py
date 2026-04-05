import streamlit as st
from Cliente import Cliente
from Reserva import Reserva
from Suite import Suite

def atualizar_dados_sessao():
    st.session_state.clientes = Cliente.carregar_todos()
    st.session_state.suites = Suite.carregar_todas()
    st.session_state.reservas = Reserva.carregar_todas()

if "clientes" not in st.session_state:
    atualizar_dados_sessao()

st.title("🏨 Sistema de Gestão de Hotel")

aba_checkin, aba_checkout, aba_dados, aba_gerenciar_clientes = st.tabs(
    [
        "📥 Fazer Check-in",
        "📤 Fazer Check-out",
        "📊 Visualizar Dados",
        "👥 Gerenciar Clientes",
    ]
)

with aba_checkin:
    st.header("Novo Check-in")

    nomes_clientes = [c.nome for c in st.session_state.clientes]
    numeros_suites = [s.numero for s in st.session_state.suites]

    cliente_selecionado = st.selectbox(
        "Selecione o Cliente", nomes_clientes if nomes_clientes else ["Nenhum"]
    )
    suite_selecionada = st.selectbox(
        "Selecione a Suíte", numeros_suites if numeros_suites else ["Nenhuma"]
    )

    col1, col2 = st.columns(2)
    with col1:
        data_entrada = st.date_input("Data de Entrada")
    with col2:
        data_saida = st.date_input("Data de Saída")

    if st.button("Confirmar Check-in", type="primary"):
        if (
            cliente_selecionado != "Nenhum"
            and suite_selecionada != "Nenhuma"
        ):
            sucesso = Reserva.registrar_checkin(
                cliente_selecionado,
                suite_selecionada,
                data_entrada,
                data_saida,
            )
            if sucesso:
                st.success("🎉 Check-in realizado com sucesso!")
                atualizar_dados_sessao()
                st.rerun()
        else:
            st.warning("Cadastre clientes e suítes no banco primeiro.")

with aba_checkout:
    st.header("Finalizar Reserva")

    reservas_ativas = [
        r for r in st.session_state.reservas if r.status == "Ativa"
    ]

    if reservas_ativas:
        opcoes_reserva = {
            r.id: f"Reserva #{r.id} - {r.cliente_nome} (Suíte {r.suite_numero})"
            for r in reservas_ativas
        }

        reserva_selecionada = st.selectbox(
            "Selecione a Reserva para Check-out",
            options=list(opcoes_reserva.keys()),
            format_func=lambda x: opcoes_reserva[x],
        )

        objeto_reserva = next(
            r for r in reservas_ativas if r.id == reserva_selecionada
        )

        if st.button("Confirmar Check-out", type="secondary"):
            if objeto_reserva.registrar_checkout():
                st.success("🛎️ Check-out realizado!")
                atualizar_dados_sessao()
                st.rerun()
    else:
        st.info("Não há reservas ativas no momento.")

with aba_dados:
    st.header("Dados Atuais no Banco")
    st.subheader("👥 Clientes")
    st.dataframe(
        [vars(c) for c in st.session_state.clientes],
        use_container_width=True,
    )

    st.subheader("🛏️ Suítes")
    st.dataframe(
        [vars(s) for s in st.session_state.suites], use_container_width=True
    )

    st.subheader("📅 Reservas")
    st.dataframe(
        [vars(r) for r in st.session_state.reservas],
        use_container_width=True,
    )

with aba_gerenciar_clientes:
    st.header("Gerenciamento de Clientes")

    menu_c = st.radio(
        "O que deseja fazer?",
        ["Cadastrar", "Atualizar", "Deletar"],
        horizontal=True,
    )
    if menu_c == "Cadastrar":
        st.subheader("Novo Cadastro")
        with st.form("form_cadastro"):
            nome = st.text_input("Nome do Cliente")
            telefone = st.text_input("Telefone")
            email = st.text_input("Email")
            submit = st.form_submit_button("Cadastrar Cliente")

            if submit:
                if nome and telefone and email:
                    if Cliente.cadastrar(nome, telefone, email):
                        st.success(f"Cliente {nome} cadastrado com sucesso!")
                        atualizar_dados_sessao()
                        st.rerun()
                else:
                    st.warning("Preencha todos os campos!")
    elif menu_c == "Atualizar":
        st.subheader("Editar Cliente")
        clientes = st.session_state.clientes

        if clientes:
            opcoes_clientes = {c.id: f"ID: {c.id} | {c.nome}" for c in clientes}
            id_selecionado = st.selectbox(
                "Selecione o cliente para editar",
                options=list(opcoes_clientes.keys()),
                format_func=lambda x: opcoes_clientes[x],
            )

            cliente_atual = next(c for c in clientes if c.id == id_selecionado)

            with st.form("form_edicao"):
                novo_nome = st.text_input("Nome", value=cliente_atual.nome)
                novo_tel = st.text_input(
                    "Telefone", value=cliente_atual.telefone
                )
                novo_email = st.text_input("Email", value=cliente_atual.email)
                submit_edit = st.form_submit_button("Salvar Alterações")

                if submit_edit:
                    if cliente_atual.atualizar(novo_nome, novo_tel, novo_email):
                        st.success("Dados atualizados com sucesso!")
                        atualizar_dados_sessao()
                        st.rerun()
        else:
            st.info("Nenhum cliente cadastrado.")

    elif menu_c == "Deletar":
        st.subheader("Remover Cliente")
        clientes = st.session_state.clientes

        if clientes:
            opcoes_clientes = {c.id: f"ID: {c.id} | {c.nome}" for c in clientes}
            id_selecionado = st.selectbox(
                "Selecione o cliente para remover",
                options=list(opcoes_clientes.keys()),
                format_func=lambda x: opcoes_clientes[x],
            )

            cliente_selecionado = next(
                c for c in clientes if c.id == id_selecionado
            )

            if st.button("❌ Deletar Permanentemente", type="primary"):
                # Chamamos o método direto no objeto selecionado
                if cliente_selecionado.deletar():
                    st.success("Cliente removido com sucesso!")
                    atualizar_dados_sessao()
                    st.rerun()
        else:
            st.info("Nenhum cliente cadastrado.")