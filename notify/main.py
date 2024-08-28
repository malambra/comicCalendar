import json
import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Cargar variables de entorno
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Configura Telegram
telegram_timer = os.getenv("TELEGRAM_TIMER_SECONDS")
telegram_token = os.getenv("TELEGRAM_TOKEN")

# Configurar el logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de comunidades autónomas y provincias
comunidades = [
    "Andalucía", "Cataluña", "Comunidad de Madrid", "Comunidad Valenciana", 
    "Castilla-La Mancha", "País Vasco", "Principado de Asturias", "Castilla y León", 
    "Extremadura", "Illes Balears", "Cantabria", "Galicia", "Región de Murcia", 
    "Comunidad Foral de Navarra", "Canarias", "La Rioja", "Aragón", "Ceuta", "Melilla"
]

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
        keyboard = [[InlineKeyboardButton(provincia, callback_data=f'delete_provincia_{provincia}')] for provincia in provincias[comunidad]]
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
        keyboard = [[InlineKeyboardButton(provincia, callback_data=f'provincia_{provincia}')] for provincia in provincias[comunidad]]
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

# Función para revisar eventos y notificar a los usuarios
async def check_events(context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with open('../auto_update/events_to_add.json', 'r') as file:
            events = json.load(file)
    except FileNotFoundError:
        events = []

    try:
        with open('user_preferences.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    # Obtener la fecha de modificación del archivo events_to_add.json
    events_file_mod_time = datetime.fromtimestamp(os.path.getmtime('events_to_add.json')).isoformat()

    for user in users:
        logger.info("Revisando eventos para %s...", user['chat_id'])
        if 'last_notification' not in user or events_file_mod_time > user['last_notification']:
            for event in events:
                if 'summary' in event:
                    logger.info("Evento: %s", event['summary'])
                else:
                    logger.warning("Evento sin resumen encontrado: %s", event)
                    continue

                if (user['event_type'] == 'todos' or user['event_type'] == event['type']) and \
                   (user['comunidad'] == 'todas' or user['comunidad'] == event['community']) and \
                   (user['provincia'] == 'todas' or user['provincia'] == event['province']):
                    message = (
                        "#######################################\n"
                        f"Nuevo evento: {event['summary']}\n"
                        f"Fecha de inicio: {event['start_date']}\n"
                        f"Fecha de fin: {event['end_date']}\n"
                        f"Provincia: {event['province']}\n"
                        f"Dirección: {event['address']}\n"
                        f"Descripción: {event['description']}\n"
                        f"Comunidad: {event['community']}\n"
                        f"Ciudad: {event['city']}\n"
                        f"Tipo: {event['type']}\n"
                        "#######################################"
                    )
                    await context.bot.send_message(chat_id=user['chat_id'], text=message)
                    logger.info("Nuevo evento para %s: %s", user['chat_id'], event['summary'])

            # Actualizar la fecha de la última notificación
            user['last_notification'] = events_file_mod_time

    with open('user_preferences.json', 'w') as file:
        json.dump(users, file, indent=4)

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

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "¡Hola! Aquí tienes una lista de comandos que puedes usar:\n\n"
        "/start - Iniciar el bot y añadir nuevas preferencias.\n"
        "/check - Listar tus preferencias actuales.\n"
        "/delete - Eliminar una preferencia específica.\n"
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

def main() -> None:
    # Reemplaza 'YOUR' con el token de tu bot de Telegram
    application = Application.builder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("check", check))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("clean", clean))
    application.add_handler(CommandHandler("help", help))
    # Configurar el job para revisar eventos cada minuto
    job_queue = application.job_queue
    job_queue.run_repeating(check_events, interval=int(telegram_timer), first=0)

    application.run_polling()

if __name__ == '__main__':
    main()