import re
import nltk
import random
import unicodedata
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

nltk.download('wordnet')
nltk.download('stopwords')


# Função para remover acentos das palavras
def remover_acentos(texto):
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))


# Função de pré-processamento para remoção de acentos
def preprocess(text):
    text = remover_acentos(text.lower())
    tokens = re.findall(r'\b\w+\b', text)
    stop_words = set(remover_acentos(word) for word in stopwords.words('portuguese'))
    tokens = [t for t in tokens if t not in stop_words]
    return tokens


# Base de conhecimento e respostas
conhecimentos = {
    "saudação": ["Olá! Como posso ajudá-lo com os serviços notariais?", "Bem-vindo! Em que posso ajudar?"],
    "despedida": ["Obrigado por visitar nossos serviços notariais. Até logo!", "Tenha um ótimo dia! Volte sempre."],
    "horário": ["Estamos abertos de segunda a sexta das 7h30 às 15h30.", "Nosso horário de funcionamento é das 7h30 às 15h30, de segunda a sexta-feira."],
    "localização": ["Estamos localizados na Av. 25 de Setembro, Caixa Postal nº19 – Xai-Xai"],
    "certidão": ["Emitimos certidões de nascimento, casamento e óbito. Para solicitar, traga documentos pessoais."],
    "reconhecimento": ["Realizamos reconhecimento de firma. É necessário comparecer pessoalmente com o documento de identidade e a assinatura a ser autenticada."],
    "autenticação": ["Fazemos autenticação de cópias de documentos. Traga o documento original e a cópia para o procedimento."],
    "procuracao": ["Emitimos procurações para diversos fins, como venda de bens ou representação. Traga seu documento de identidade e, se necessário, o documento do representado."],
    "divorcio": ["Realizamos processos de divórcio consensual extrajudicial. Para isso, ambas as partes devem concordar e estar presentes, além de não haver filhos menores envolvidos."],
    "inventario": ["Para inventário extrajudicial, é preciso que todos os herdeiros estejam de acordo. Traga documentos pessoais, certidão de óbito e documentos dos bens a serem inventariados."],
    "escritura": ["Emitimos escrituras públicas para compra e venda, doação, e outros fins. Documentos pessoais, contrato e documentos do imóvel são necessários."],
    "declaracao": ["Podemos emitir declarações de residência, dependência econômica, entre outras. Traga documentos de identificação e comprovantes relacionados ao que deseja declarar."],
    "certidao_negativa": ["Emitimos certidões negativas para comprovar a inexistência de dívidas ou processos. Para mais informações, consulte um atendente."],
    "alteracao_nome": ["A alteração de nome próprio pode ser realizada em nosso cartório mediante solicitação judicial ou quando justificada. Traga documentos pessoais e motivos para a alteração."],
    "apostila": ["Emitimos apostilas para validação de documentos em outros países. Traga o documento original e cópias para a legalização."],
    "traducoes": ["Oferecemos serviços de tradução juramentada para documentos. Consulte-nos para saber quais idiomas estão disponíveis."]
}

# Função para verificar similaridade com palavras-chave
def similar_token(tokens, palavras_chave, threshold=80):
    for token in tokens:
        for palavra in palavras_chave:
            if fuzz.ratio(token, palavra) >= threshold:
                return True
    return False


# Função para responder perguntas
def responder(pergunta):
    tokens = preprocess(pergunta)
    if similar_token(tokens, ["oi", "ola", "bom", "dia", "tarde", "noite"]):
        return random.choice(conhecimentos["saudação"])
    elif similar_token(tokens, ["tchau", "ate", "logo"]):
        return random.choice(conhecimentos["despedida"])
    elif similar_token(tokens, ["horario", "abre", "funciona", "expediente"]):
        return random.choice(conhecimentos["horário"])
    elif similar_token(tokens, ["localizacao", "onde", "endereco", "fica"]):
        return random.choice(conhecimentos["localização"])
    elif similar_token(tokens, ["certidao", "certidoes", "registro"]):
        return random.choice(conhecimentos["certidão"])
    elif similar_token(tokens, ["reconhecimento", "firma", "assinatura"]):
        return random.choice(conhecimentos["reconhecimento"])
    elif similar_token(tokens, ["autenticacao", "autenticar", "copia", "documento"]):
        return random.choice(conhecimentos["autenticação"])
    elif similar_token(tokens, ["procuracao", "mandato", "representacao"]):
        return random.choice(conhecimentos["procuracao"])
    elif similar_token(tokens, ["divorcio", "separacao", "casamento"]):
        return random.choice(conhecimentos["divorcio"])
    elif similar_token(tokens, ["inventario", "heranca", "bens"]):
        return random.choice(conhecimentos["inventario"])
    elif similar_token(tokens, ["escritura", "contrato", "compra", "venda"]):
        return random.choice(conhecimentos["escritura"])
    elif similar_token(tokens, ["declaracao", "residencia", "dependencia"]):
        return random.choice(conhecimentos["declaracao"])
    elif similar_token(tokens, ["certidao negativa", "divida", "negativa"]):
        return random.choice(conhecimentos["certidao_negativa"])
    elif similar_token(tokens, ["alteracao", "nome", "mudanca"]):
        return random.choice(conhecimentos["alteracao_nome"])
    elif similar_token(tokens, ["apostila", "legalizacao", "documento"]):
        return random.choice(conhecimentos["apostila"])
    elif similar_token(tokens, ["traducao", "juramentada", "idioma"]):
        return random.choice(conhecimentos["traducoes"])
    else:
        return "Desculpe, não entendi. Pode reformular a pergunta sobre nossos serviços notariais?"


# Configuração do bot Telegram
TOKEN = "7593500408:AAGDSj_Jakrgl7ehqk2Z_VDRSfncuQSS5Z8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou o assistente notarial. Como posso ajudar?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = responder(user_message)
    await update.message.reply_text(response)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
