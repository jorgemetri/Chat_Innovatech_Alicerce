import streamlit as st
# from oauth2client.service_account import ServiceAccountCredentials # REMOVA ESTA LINHA
import gspread
from datetime import datetime # Adicionado para dados_para_enviar_exemplo

# SCOPES não é mais explicitamente necessário para service_account_from_dict com os escopos padrão
# SCOPES = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/drive",
# ]

def get_gsheets_client():
    try:
        creds_dict = st.secrets["gsheets_creds"]
        # Usa o método mais moderno do gspread
        client = gspread.service_account_from_dict(creds_dict)
        return client
    except KeyError:
        st.error("Configuração [gsheets_creds] não encontrada em .streamlit/secrets.toml. Verifique o arquivo.")
        return None
    except Exception as e:
        st.error(f"Erro ao autenticar com Google Sheets usando service_account_from_dict: {e}")
        return None

# --- Lógica do seu aplicativo Streamlit ---
st.title("Teste de Envio para Google Sheets com st.secrets (gspread moderno)")
st.markdown("""
Este aplicativo tenta se conectar à sua planilha do Google Sheets usando as credenciais definidas em
`.streamlit/secrets.toml` e adicionar uma linha de dados de teste.
""")

# Seus dados de planilha
SPREADSHEET_TITLE = "BaseDadosChat" 
WORKSHEET_NAME = "Página1"
# SPREADSHEET_ID = "1cUTbptS5QzFNMC3ClFIkupeyyxAfLIJ8HGkPSMCUq3Q" # Pode usar open_by_id se preferir

# Exemplo de dados de teste
# Certifique-se de que o número de colunas aqui corresponde à sua planilha
# O script anterior tinha 28 colunas (DataHora + 27 campos)
dados_para_enviar_exemplo_lista = [datetime.now().strftime("%d/%m/%Y às %H:%M:%S")]
for i in range(1, 28): # Para ter 28 colunas no total (DataHora + 27 campos)
    dados_para_enviar_exemplo_lista.append(f"Dado Teste Moderno {i}")


st.write("Dados de teste a serem enviados (primeiros 5 campos):")
st.json(dados_para_enviar_exemplo_lista[:5] + ["..."])


if st.button("🚀 Enviar Dados de Teste para Google Sheets"):
    client = get_gsheets_client()
    if client:
        try:
            # Abrir por título, como funcionou no seu teste
            planilha_completa = client.open(title=SPREADSHEET_TITLE)
            # Ou por ID, que é geralmente mais robusto se você tiver o ID:
            # planilha_completa = client.open_by_id(SPREADSHEET_ID)
            
            planilha = planilha_completa.worksheet(WORKSHEET_NAME) 

            planilha.append_row(dados_para_enviar_exemplo_lista, value_input_option='USER_ENTERED')
            st.success("Dados enviados com sucesso para a planilha!")
            st.balloons()

        except gspread.exceptions.SpreadsheetNotFound:
            st.error(f"Planilha '{SPREADSHEET_TITLE}' não encontrada! Verifique o título ou se a conta de serviço tem permissão.")
        except gspread.exceptions.WorksheetNotFound:
            st.error(f"Aba '{WORKSHEET_NAME}' não encontrada na planilha '{SPREADSHEET_TITLE}'.")
        except gspread.exceptions.APIError as e:
            st.error(f"Erro de API do Google Sheets: {e}")
        except Exception as e:
            st.error(f"Ocorreu um erro ao enviar os dados: {e}")
    else:
        st.error("Falha ao inicializar o cliente Google Sheets. Verifique os erros de autenticação.")

st.markdown("---")
st.subheader("Verificações de Segredos:")
try:
    creds_check = st.secrets["gsheets_creds"]
    st.success("✅ Seção `[gsheets_creds]` encontrada em `secrets.toml`.")
    st.write("Email da conta de serviço (do secrets.toml): ", creds_check.get("client_email", "Não encontrado"))
except KeyError:
    st.error("❌ Seção `[gsheets_creds]` NÃO encontrada em `secrets.toml`.")
except Exception as e:
    st.error(f"Erro ao acessar st.secrets: {e}")