import json
import logging
import os
import html
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# INITIAL SETUP

# Cargar variables de entorno
dotenv_path = os.path.join(os.path.dirname(__file__), '.', '.env')
load_dotenv(dotenv_path)

# Configura Telegram
telegram_timer = os.getenv("TELEGRAM_TIMER_SECONDS")
telegram_token = os.getenv("TELEGRAM_TOKEN")

# Configurar el logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de comunidades autónomas
comunidades = [
    "Andalucía", "Cataluña", "Comunidad de Madrid", "Comunidad Valenciana", 
    "Castilla-La Mancha", "País Vasco", "Principado de Asturias", "Castilla y León", 
    "Extremadura", "Illes Balears", "Cantabria", "Galicia", "Región de Murcia", 
    "Comunidad Foral de Navarra", "Canarias", "La Rioja", "Aragón", "Ceuta", "Melilla"
]
# Lista de provincias
provincias = {
    "Andalucía": ["Almería", "Cádiz", "Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla"],
    "Cataluña": ["Barcelona", "Girona", "Lleida", "Tarragona"],
    "Comunidad de Madrid": ["Madrid"],
    "Comunidad Valenciana": ["Alicante", "Castellón", "Valencia"],
    "Castilla-La Mancha": ["Albacete", "Ciudad Real", "Cuenca", "Guadalajara", "Toledo"],
    "País Vasco": ["Álava", "Bizkaia", "Gipuzkoa"],
    "Principado de Asturias": ["Asturias"],
    "Castilla y León": ["Ávila", "Burgos", "León", "Palencia", "Salamanca", "Segovia", "Soria", "Valladolid", "Zamora"],
    "Extremadura": ["Badajoz", "Cáceres"],
    "Illes Balears": ["Illes Balears"],
    "Cantabria": ["Cantabria"],
    "Galicia": ["A Coruña", "Lugo", "Ourense", "Pontevedra"],
    "Región de Murcia": ["Murcia"],
    "Comunidad Foral de Navarra": ["Navarra"],
    "Canarias": ["Las Palmas", "Santa Cruz de Tenerife"],
    "La Rioja": ["La Rioja"],
    "Aragón": ["Huesca", "Teruel", "Zaragoza"],
    "Ceuta": ["Ceuta"],
    "Melilla": ["Melilla"]
}

# BASIC FUNCTIONS

# Función para guardar las preferencias del usuario en un archivo JSON
def save_preferences(preferences):
    try:
        with open('user_preferences.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(preferences)

    with open('user_preferences.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_events_from_file(file_path):
    with open(file_path, 'r') as file:
        events = json.load(file)
    return events

def get_last_processed_id(events_file_path, last_id_file_path):
    if os.path.exists(last_id_file_path):
        with open(last_id_file_path, 'r') as file:
            return int(file.read().strip())
    else:
        # Leer el archivo de eventos para obtener el mayor ID
        try:
            with open(events_file_path, 'r') as file:
                events = json.load(file)
            if events:
                max_id = max(event['id'] for event in events)
                save_last_processed_id(last_id_file_path, max_id)
                return max_id
            else:
                return 0
        except FileNotFoundError:
            return 0

def save_last_processed_id(file_path, last_id):
    with open(file_path, 'w') as file:
        file.write(str(last_id))


# BOT FUNCTIONS

# Función para iniciar el bot y solicitar preferencias
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    logger.info("Usuario %s ha iniciado el bot.", user.first_name)

    # Preguntar por el tipo de eventos
    keyboard = [
        [InlineKeyboardButton("Todos", callback_data='event_type_todos')],
        [InlineKeyboardButton("Firma", callback_data='event_type_Firma')],
        [InlineKeyboardButton("Evento", callback_data='event_type_Evento')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('¿De qué tipo de eventos deseas ser notificado?', reply_markup=reply_markup)

    # Guardar el chat_id en el contexto
    context.user_data['chat_id'] = chat_id

# Función para iniciar el proceso de eliminación de una preferencia
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    logger.info("Usuario %s ha iniciado el proceso de eliminación de una preferencia.", user.first_name)

    # Preguntar por el tipo de eventos
    keyboard = [
        [InlineKeyboardButton("Todos", callback_data='delete_event_type_todos')],
        [InlineKeyboardButton("Firma", callback_data='delete_event_type_Firma')],
        [InlineKeyboardButton("Evento", callback_data='delete_event_type_Evento')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('¿De qué tipo de eventos deseas eliminar la preferencia?', reply_markup=reply_markup)

    # Guardar el chat_id en el contexto
    context.user_data['chat_id'] = chat_id

# Función para manejar las respuestas del usuario
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Obtener el chat_id del contexto
    chat_id = context.user_data['chat_id']

    # Manejar la respuesta del tipo de evento para eliminación
    if query.data.startswith('delete_event_type_'):
        event_type = query.data.split('_')[3]
        context.user_data['delete_event_type'] = event_type

        # Preguntar por la comunidad autónoma
        keyboard = [[InlineKeyboardButton(comunidad, callback_data=f'delete_comunidad_{comunidad}')] for comunidad in comunidades]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="¿De qué comunidad autónoma deseas eliminar la preferencia?", reply_markup=reply_markup)

    # Manejar la respuesta de la comunidad autónoma para eliminación
    elif query.data.startswith('delete_comunidad_'):
        comunidad = query.data.split('_')[2]
        context.user_data['delete_comunidad'] = comunidad

        # Preguntar por la provincia
        keyboard = [[InlineKeyboardButton("Todas", callback_data='delete_provincia_Todas')]]  # Añadir opción "Todas"
        keyboard += [[InlineKeyboardButton(provincia, callback_data=f'delete_provincia_{provincia}')] for provincia in provincias[comunidad]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="¿De qué provincia deseas eliminar la preferencia?", reply_markup=reply_markup)

    # Manejar la respuesta de la provincia para eliminación
    elif query.data.startswith('delete_provincia_'):
        provincia = query.data.split('_')[2]
        context.user_data['delete_provincia'] = provincia

        # Eliminar la preferencia del usuario
        try:
            with open('user_preferences.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []

        # Filtrar las preferencias del usuario
        users = [user for user in users if not (
            user['chat_id'] == chat_id and
            user['event_type'] == context.user_data['delete_event_type'] and
            user['comunidad'] == context.user_data['delete_comunidad'] and
            user['provincia'] == context.user_data['delete_provincia']
        )]

        with open('user_preferences.json', 'w') as file:
            json.dump(users, file, indent=4)

        await query.edit_message_text(text="¡Gracias! La preferencia ha sido eliminada.")

    # Manejar la respuesta del tipo de evento para añadir/modificar
    elif query.data.startswith('event_type_'):
        event_type = query.data.split('_')[2]
        context.user_data['event_type'] = event_type

        # Preguntar por la comunidad autónoma
        keyboard = [[InlineKeyboardButton(comunidad, callback_data=f'comunidad_{comunidad}')] for comunidad in comunidades]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="¿De qué comunidad autónoma deseas recibir notificaciones?", reply_markup=reply_markup)

    # Manejar la respuesta de la comunidad autónoma para añadir/modificar
    elif query.data.startswith('comunidad_'):
        comunidad = query.data.split('_')[1]
        context.user_data['comunidad'] = comunidad

        # Preguntar por la provincia
        keyboard = [[InlineKeyboardButton("Todas", callback_data=f'provincia_Todas')]]
        keyboard += [[InlineKeyboardButton(provincia, callback_data=f'provincia_{provincia}')] for provincia in provincias[comunidad]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="¿De qué provincia deseas recibir notificaciones?", reply_markup=reply_markup)

    # Manejar la respuesta de la provincia para añadir/modificar
    elif query.data.startswith('provincia_'):
        provincia = query.data.split('_')[1]
        context.user_data['provincia'] = provincia

        # Guardar las preferencias del usuario
        preferences = {
            'chat_id': chat_id,
            'event_type': context.user_data['event_type'],
            'comunidad': context.user_data['comunidad'],
            'provincia': context.user_data['provincia']
        }

        # Si estamos modificando una preferencia existente
        if 'modify_index' in context.user_data:
            index = context.user_data['modify_index']
            try:
                with open('user_preferences.json', 'r') as file:
                    users = json.load(file)
            except FileNotFoundError:
                users = []

            user_preferences = [user for user in users if user['chat_id'] == chat_id]
            user_preferences[index] = preferences

            users = [user for user in users if user['chat_id'] != chat_id] + user_preferences

            with open('user_preferences.json', 'w') as file:
                json.dump(users, file, indent=4)

            del context.user_data['modify_index']
            await query.edit_message_text(text="¡Gracias! Tu preferencia ha sido modificada.")
        else:
            save_preferences(preferences)
            await query.edit_message_text(text="¡Gracias! Tus preferencias han sido guardadas.")

# Función para comprobar los eventos 
async def check_events(context: ContextTypes.DEFAULT_TYPE) -> None:
    events_file_path = "./events.json"
    last_id_file_path = "../app2/last_processed_id.txt"
    
    # Leer el último ID procesado
    last_processed_id = get_last_processed_id(events_file_path, last_id_file_path)
    print("############################################")
    logger.info("Último ID procesado: %s", last_processed_id)
    print("############################################")

    try:
        with open(events_file_path, 'r') as file:
            events = json.load(file)
            print("############################################")
            logger.info("Eventos cargados correctamente.")
            print("############################################")
    except FileNotFoundError:
        events = []
        print("############################################")
        logger.info("PWD: %s", os.getcwd())
        logger.error("No se encontró el archivo de eventos.")
        print("############################################")

    try:
        with open('user_preferences.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    # Filtrar los eventos a partir del último ID procesado
    new_events = [event for event in events if event['id'] > last_processed_id]
    print("############################################")
    logger.info("Eventos totales: %s", len(events))
    logger.info("Nuevos eventos: %s", new_events)
    print("############################################")

    for user in users:
        for event in new_events:
            if 'summary' in event:
                logger.info("Evento: %s", event['summary'])
            else:
                logger.warning("Evento sin resumen encontrado: %s", event)
                continue
            if (user['event_type'] == 'todos' or user['event_type'] == event['type']) and \
               (user['comunidad'] == 'todas' or user['comunidad'] == event['community']) and \
               (user['provincia'] == 'Todas' or user['provincia'] == event['province']):
                await notify_users(context, user, event)

    if new_events:
        last_processed_id = max(event['id'] for event in new_events)
        save_last_processed_id(last_id_file_path, last_processed_id)

# Función para notificar a los usuarios
async def notify_users(context, user, event):
    try:
        message = (
            f"🎭 *{html.escape(event['summary'])}*\n"
            f"📅 *Fecha de inicio*: {html.escape(event['start_date'])}\n"
            f"📅 *Fecha de fin*: {html.escape(event['end_date'])}\n"
            f"🌐 *Comunidad*: {html.escape(event['community'])}\n"
            f"🌐 *Provincia*: {html.escape(event['province'])}\n"
            f"🌐 *Ciudad*: {html.escape(event['city'])}\n"
            f"📍 *Dirección*: {html.escape(event['address'])}\n"
            f"🏷️ *Tipo*: {html.escape(event['type'])}\n"
            f"🔗 [Link](https://comicplan.com/?id={event['id']})"
        )
        logger.info("Mensaje a enviar: %s", message)
        logger.info("Enviando Nuevo evento para %s: Summary: %s", user['chat_id'], event['summary'])
        await context.bot.send_message(chat_id=user['chat_id'], text=message, parse_mode='Markdown')
        logger.info("Envio OK evento para %s: %s", user['chat_id'], event['summary'])
    except Exception as e:
        logger.error("Error al enviar el mensaje: %s", e)


# Función para devolver las preferencias del usuario
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    try:
        with open('user_preferences.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    user_preferences = [user for user in users if user['chat_id'] == chat_id]

    if user_preferences:
        message = "Tus preferencias:\n"
        message += "-" * 20 + "\n"
        for pref in user_preferences:
            message += (
                f"Tipo de evento: {pref['event_type']}\n"
                f"Comunidad: {pref['comunidad']}\n"
                f"Provincia: {pref['provincia']}\n\n"
            )
    else:
        message = "No se encontraron preferencias para tu chat_id."

    await update.message.reply_text(message)

# Función para mostrar el mensaje de ayuda
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "¡Hola! Aquí tienes una lista de comandos que puedes usar:\n\n"
        "/start - Iniciar el bot y añadir nuevas preferencias.\n"
        "/check - Listar tus preferencias actuales.\n"
        "/delete - Eliminar una preferencia específica.\n"
        "/clean - Eliminar todas tus preferencias.\n"
        "/about - Mostrar información sobre el bot.\n"
        "/help - Mostrar este mensaje de ayuda.\n"
    )
    await update.message.reply_text(help_text)

# Función para eliminar todas las preferencias del usuario
async def clean(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    try:
        with open('user_preferences.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    # Filtrar las preferencias para eliminar las del chat_id actual
    users = [user for user in users if user['chat_id'] != chat_id]

    with open('user_preferences.json', 'w') as file:
        json.dump(users, file, indent=4)

    await update.message.reply_text("Todas tus preferencias han sido eliminadas.")

# Función para manejar el comando /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_text = (
        "👤 **Autor**: Manuel Alambra [@malambra](https://github.com/malambra)\n"
        "🔗 **Repositorio Backend**: [GitHub](https://github.com/malambra/comicCalendar)\n"
        "🔗 **Repositorio Frontend**: [GitHub](https://github.com/Raixs/ComicCalendarWeb)\n"
        "🌐 **Web**: [https://comicplan.com](https://comicplan.com/)\n"
        "🌐 **API**: [https://api.comicplan.com/docs](https://api.comicplan.com/docs)\n"
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

# Función para establecer la descripción del bot
async def set_bot_description(application) -> None:
    description = (
        "Este bot te notifica sobre los eventos en tu comunidad y provincia. "
        "Usa /start para comenzar y seleccionar tus preferencias."
        "Usa /help para ver una lista de comandos disponibles."
    )
    await application.bot.set_my_description(description)

async def set_bot_commands(application) -> None:
    commands = [
        BotCommand("start", "Iniciar el bot y añadir nuevas preferencias"),
        BotCommand("check", "Listar tus preferencias actuales"),
        BotCommand("delete", "Eliminar una preferencia específica"),
        BotCommand("clean", "Eliminar todas tus preferencias"),
        BotCommand("about", "Mostrar información sobre el bot"),
        BotCommand("help", "Mostrar este mensaje de ayuda")
    ]
    await application.bot.set_my_commands(commands)

# MAIN Function
def main() -> None:
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        raise ValueError("No se ha encontrado el token de Telegram en las variables de entorno")
    # Reemplaza 'YOUR' con el token de tu bot de Telegram
    application = Application.builder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("check", check))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("clean", clean))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("help", help))
    # Configurar el job para revisar eventos cada minuto
    job_queue = application.job_queue
    job_queue.run_repeating(check_events, interval=int(telegram_timer), first=0)
    
    # Establecer la descripción del bot
    application.job_queue.run_once(set_bot_description, 0)

    # Establecer los comandos del bot
    application.job_queue.run_once(set_bot_commands, 0)

    application.run_polling()

if __name__ == '__main__':
    main()