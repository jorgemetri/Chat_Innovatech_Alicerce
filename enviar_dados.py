import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Defina os escopos necessários
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

def get_gsheets_client():
    try:
        # Isso irá carregar a seção [gsheets_creds] do secrets.toml como um dicionário
        creds_dict = st.secrets["gsheets_creds"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes=SCOPES)
        client = gspread.authorize(creds)
        return client
    except KeyError:
        st.error("Configuração [gsheets_creds] não encontrada em .streamlit/secrets.toml. Verifique o arquivo.")
        return None
    except Exception as e:
        st.error(f"Erro ao autenticar com Google Sheets: {e}")
        return None

# --- Lógica do seu aplicativo Streamlit ---
st.title("Teste de Envio para Google Sheets com st.secrets")
st.markdown("""
Este aplicativo tenta se conectar à sua planilha do Google Sheets usando as credenciais definidas em
`.streamlit/secrets.toml` e adicionar uma linha de dados de teste.
""")

# Exemplo de dados de teste
dados_para_enviar_exemplo = {
    "DataHora": "21/05/2025 às 19:36:06",
    "Campo1": "Dado Teste 1",
    "Campo2": "Dado Teste 2",
    "Campo3": "Dado Teste 3",
    "Campo4": "Dado Teste 4",
    "Campo5": "..."
}
st.write("Dados de teste a serem enviados (primeiros 5 campos):")
st.json(dict(list(dados_para_enviar_exemplo.items())[:5]))


if st.button("🚀 Enviar Dados de Teste para Google Sheets"):
    client = get_gsheets_client()
    if client:
        try:
            # Substitua pelo nome da sua planilha e ID da pasta, se necessário
            # ou pelo ID da planilha se você já o tiver.
            # planilha_completa = client.open_by_key("SEU_SHEET_ID_AQUI")
            planilha_completa = client.open(title="BaseDadosChat", folder_id="1GNJ9tm1cJsAZJMi9sy-vakdmBoJigkMI") # Use o seu folder_id e title
            planilha = planilha_completa.get_worksheet(0) # Pega a primeira aba

            # Defina os dados que você quer enviar
            # IMPORTANTE: Os nomes das chaves aqui devem corresponder aos seus cabeçalhos na planilha
            # ou você precisará enviar uma lista de valores na ordem correta das colunas.
            # Para este exemplo, vamos supor que a planilha espera os valores na ordem.
            linha_para_adicionar = [
                dados_para_enviar_exemplo["DataHora"],
                dados_para_enviar_exemplo["Campo1"],
                dados_para_enviar_exemplo["Campo2"],
                dados_para_enviar_exemplo["Campo3"],
                dados_para_enviar_exemplo["Campo4"],
                dados_para_enviar_exemplo["Campo5"]
            ]
            planilha.append_row(linha_para_adicionar)
            st.success("Dados enviados com sucesso para a planilha!")
            st.balloons()

        except gspread.exceptions.SpreadsheetNotFound:
            st.error("Planilha não encontrada! Verifique o título, folder_id ou se a conta de serviço tem permissão.")
        except gspread.exceptions.APIError as e:
            st.error(f"Erro de API do Google Sheets: {e}")
        except Exception as e:
            st.error(f"Ocorreu um erro ao enviar os dados: {e}")

st.markdown("---")
st.subheader("Verificações:")
try:
    st.secrets["gsheets_creds"]
    st.success("✅ Seção `[gsheets_creds]` encontrada em `secrets.toml`.")
except KeyError:
    st.error("❌ Seção `[gsheets_creds]` NÃO encontrada em `secrets.toml`.")