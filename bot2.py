from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from fpdf import FPDF

API_TOKEN = 'TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    reportName = State()
    userName = State()
    typeName = State()
    infoBlock1 = State()
    processGoal = State()
    successCriteria = State()
    processInputs = State()
    processOutputs = State()
    processBoundaries = State()
    infoBlock2 = State()
    processOwner = State()
    processExecutor = State()
    externalParticipants = State()
    infoBlock3 = State()
    processStages = State()
    addMoreStages = State()
    materialResources = State()
    infoResources = State()
    softwareResources = State()
    infoBlock5 = State()
    kpiDescription = State()
    addMoreKPI = State()
    infoBlock6 = State()
    risksDescription = State()
    addMoreRisks = State()
    infoBlock7 = State()
    processImage = State()
    finalConfirmation = State()


confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Подтвердить"), KeyboardButton(text="Редактировать")]
    ],
    resize_keyboard=True
)

continue_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Продолжить"), KeyboardButton(text="Скорректировать")]
    ],
    resize_keyboard=True
)

stage_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить этап"), KeyboardButton(text="Пропустить")],
        [KeyboardButton(text="Завершить описание")]
    ],
    resize_keyboard=True
)

kpi_risk_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить"), KeyboardButton(text="Завершить")]
    ],
    resize_keyboard=True
)

final_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отредактировать"), KeyboardButton(text="Сбросить")],
        [KeyboardButton(text="Выгрузить PDF")]
    ],
    resize_keyboard=True
)

user_data = {}

def generate_pdf_report(data, output_path="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Заголовок отчета
    pdf.cell(200, 10, txt="Отчет по бизнес-процессу", ln=True, align='C')
    pdf.ln(10)

    # Добавление данных
    pdf.cell(200, 10, txt=f"Название процесса: {data.get('process_name', 'не указано')}", ln=True)
    pdf.cell(200, 10, txt=f"Владелец процесса: {data.get('user_name', 'не указано')}", ln=True)
    pdf.cell(200, 10, txt=f"Тип процесса: {data.get('type_name', 'не указано')}", ln=True)
    pdf.cell(200, 10, txt=f"Цель процесса: {data.get('process_goal', 'не указано')}", ln=True)
    pdf.cell(200, 10, txt=f"Критерии успеха: {data.get('success_criteria', 'не указано')}", ln=True)
    pdf.cell(200, 10, txt=f"Входы процесса: {data.get('process_inputs', 'не указано')}", ln=True)
    pdf.cell(200, 10, txt=f"Выходы процесса: {data.get('process_outputs', 'не указано')}", ln=True)
    pdf.cell(200, 10, txt=f"Границы процесса: {data.get('process_boundaries', 'не указано')}", ln=True)
    pdf.cell(200, 10, txt=f"Исполнитель процесса: {data.get('process_executor', 'не указано')}", ln=True)
    pdf.cell(200, 10, txt=f"Внешние участники: {data.get('external_participants', 'не указано')}", ln=True)

    # Этапы процесса
    pdf.cell(200, 10, txt="Этапы процесса:", ln=True)
    for stage in data.get('process_stages', []):
        pdf.cell(200, 10, txt=stage, ln=True)

    # KPI процесса
    pdf.cell(200, 10, txt="KPI процесса:", ln=True)
    for kpi in data.get('kpi_description', []):
        pdf.cell(200, 10, txt=kpi, ln=True)

    # Риски процесса
    pdf.cell(200, 10, txt="Риски процесса:", ln=True)
    for risk in data.get('risks_description', []):
        pdf.cell(200, 10, txt=risk, ln=True)

    # Завершающее сообщение
    pdf.cell(200, 10, txt="Отчет составлен успешно.", ln=True, align='C')

    pdf.output(output_path)
    return output_path

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Начинаю создание отчета...")
    await message.answer("Укажите наименование процесса", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.reportName)


@dp.message(Form.reportName)
async def reportName(message: types.Message, state: FSMContext):
    await state.update_data(process_name=message.text)
    await message.answer(f"Название процесса: {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("Укажите владельца процесса", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.userName)


@dp.message(Form.userName)
async def userName(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer(f"Имя владельца: {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("Укажите тип процесса", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.typeName)


@dp.message(Form.typeName)
async def typeName(message: types.Message, state: FSMContext):
    await state.update_data(type_name=message.text)
    data = await state.get_data()
    await message.answer(
        f"Название процесса: {data['process_name']}\n"
        f"Имя владельца: {data['user_name']}\n"
        f"Тип процесса: {data['type_name']}\n\n"
        "Подтвердить или редактировать?",
        reply_markup=confirm_keyboard
    )
    await state.set_state(Form.infoBlock1)


@dp.message(Form.infoBlock1)
async def infoBlock1(message: types.Message, state: FSMContext):
    if message.text == "Подтвердить":
        await message.answer("Данные подтверждены!", reply_markup=ReplyKeyboardRemove())
        await message.answer("Укажите цель процесса")
        await state.set_state(Form.processGoal)
    elif message.text == "Редактировать":
        await message.answer("Введите новое название процесса", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.reportName)
    else:
        await message.answer("Пожалуйста, используйте кнопки", reply_markup=confirm_keyboard)


@dp.message(Form.processGoal)
async def process_goal(message: types.Message, state: FSMContext):
    await state.update_data(process_goal=message.text)
    await message.answer(f"Цель процесса: {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("Укажите критерии успеха")
    await state.set_state(Form.successCriteria)


@dp.message(Form.successCriteria)
async def success_criteria(message: types.Message, state: FSMContext):
    await state.update_data(success_criteria=message.text)
    await message.answer(f"Критерии успеха: {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("Укажите входы процесса")
    await state.set_state(Form.processInputs)


@dp.message(Form.processInputs)
async def process_inputs(message: types.Message, state: FSMContext):
    await state.update_data(process_inputs=message.text)
    await message.answer(f"Входы процесса: {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("Укажите выходы процесса")
    await state.set_state(Form.processOutputs)


@dp.message(Form.processOutputs)
async def process_outputs(message: types.Message, state: FSMContext):
    await state.update_data(process_outputs=message.text)
    await message.answer(f"Выходы процесса: {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("Укажите границы процесса")
    await state.set_state(Form.processBoundaries)


@dp.message(Form.processBoundaries)
async def process_boundaries(message: types.Message, state: FSMContext):
    await state.update_data(process_boundaries=message.text)
    data = await state.get_data()
    await message.answer(
        f"Цель процесса: {data['process_goal']}\n"
        f"Критерии успеха: {data['success_criteria']}\n"
        f"Входы процесса: {data['process_inputs']}\n"
        f"Выходы процесса: {data['process_outputs']}\n"
        f"Границы процесса: {data['process_boundaries']}\n\n"
        "Подтвердить или редактировать?",
        reply_markup=confirm_keyboard
    )
    await state.set_state(Form.infoBlock2)


@dp.message(Form.infoBlock2)
async def infoBlock2(message: types.Message, state: FSMContext):
    if message.text == "Подтвердить":
        await message.answer("Блок целей и границ подтвержден!", reply_markup=ReplyKeyboardRemove())
        await message.answer("Укажите владельца процесса")
        await state.set_state(Form.processOwner)
    elif message.text == "Редактировать":
        await message.answer("Введите новую цель процесса", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.processGoal)
    else:
        await message.answer("Пожалуйста, используйте кнопки", reply_markup=confirm_keyboard)


@dp.message(Form.processOwner)
async def process_owner(message: types.Message, state: FSMContext):
    await state.update_data(process_owner=message.text)
    await message.answer(f"Владелец процесса: {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("Укажите исполнителя процесса")
    await state.set_state(Form.processExecutor)


@dp.message(Form.processExecutor)
async def process_executor(message: types.Message, state: FSMContext):
    await state.update_data(process_executor=message.text)
    await message.answer(f"Исполнитель процесса: {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("Укажите внешних участников процесса")
    await state.set_state(Form.externalParticipants)


@dp.message(Form.externalParticipants)
async def external_participants(message: types.Message, state: FSMContext):
    await state.update_data(external_participants=message.text)
    data = await state.get_data()
    await message.answer(
        f"Владелец процесса: {data['process_owner']}\n"
        f"Исполнитель процесса: {data['process_executor']}\n"
        f"Внешние участники: {data['external_participants']}\n\n"
        "Продолжить или скорректировать?",
        reply_markup=continue_keyboard
    )
    await state.set_state(Form.infoBlock3)


@dp.message(Form.infoBlock3)
async def infoBlock3(message: types.Message, state: FSMContext):
    if message.text == "Продолжить":
        await message.answer("Укажите этапы процесса", reply_markup=stage_keyboard)
        await state.set_state(Form.processStages)
    elif message.text == "Скорректировать":
        await message.answer("Введите владельца процесса заново", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.processOwner)
    else:
        await message.answer("Пожалуйста, используйте кнопки", reply_markup=continue_keyboard)


@dp.message(Form.processStages)
async def process_stages(message: types.Message, state: FSMContext):
    # Получаем текущие данные пользователя из FSMContext
    data = await state.get_data()

    # Если список этапов еще не существует, создаем его
    if 'process_stages' not in data:
        stages_list = []
    else:
        stages_list = data['process_stages']

    # Добавляем новый этап в список
    stages_list.append(message.text)

    # Обновляем данные с новым списком этапов
    await state.update_data(process_stages=stages_list)

    # Подтверждаем добавление и спрашиваем, нужно ли добавить еще
    await message.answer("Этап добавлен. Добавить еще или завершить?", reply_markup=stage_keyboard)
    await state.set_state(Form.addMoreStages)


@dp.message(Form.addMoreStages)
async def add_more_stages(message: types.Message, state: FSMContext):
    if message.text == "Завершить описание":
        # Когда пользователь завершает добавление этапов, показываем все добавленные этапы
        data = await state.get_data()
        stages = data.get('process_stages', [])

        # Формируем сообщение с перечислением всех этапов
        await message.answer(f"Этапы процесса:\n{'\n'.join(stages)}", reply_markup=confirm_keyboard)

        # Переходим к следующему шагу
        await state.set_state(Form.materialResources)
        await message.answer("Укажите материальные ресурсы")
    else:
        # Если пользователь хочет добавить новый этап
        await message.answer("Введите следующий этап", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.processStages)


@dp.message(Form.materialResources)
async def material_resources(message: types.Message, state: FSMContext):
    await state.update_data(material_resources=message.text)
    await message.answer("Укажите информационные ресурсы")
    await state.set_state(Form.infoResources)


@dp.message(Form.infoResources)
async def info_resources(message: types.Message, state: FSMContext):
    await state.update_data(info_resources=message.text)
    await message.answer("Укажите программные ресурсы")
    await state.set_state(Form.softwareResources)


@dp.message(Form.softwareResources)
async def software_resources(message: types.Message, state: FSMContext):
    await state.update_data(software_resources=message.text)
    data = await state.get_data()
    await message.answer(
        f"Материальные ресурсы: {data['material_resources']}\n"
        f"Информационные ресурсы: {data['info_resources']}\n"
        f"Программные ресурсы: {data['software_resources']}\n\n"
        "Подтвердить или редактировать?",
        reply_markup=confirm_keyboard
    )
    await state.set_state(Form.infoBlock5)


@dp.message(Form.infoBlock5)
async def infoBlock5(message: types.Message, state: FSMContext):
    if message.text == "Подтвердить":
        await message.answer("Ресурсы подтверждены", reply_markup=ReplyKeyboardRemove())
        await message.answer("Укажите KPI процесса")
        await state.set_state(Form.kpiDescription)
    elif message.text == "Редактировать":
        await message.answer("Введите материальные ресурсы заново", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.materialResources)
    else:
        await message.answer("Пожалуйста, используйте кнопки", reply_markup=confirm_keyboard)


@dp.message(Form.kpiDescription)
async def kpi_description(message: types.Message, state: FSMContext):
    # Получаем текущие данные пользователя из FSMContext
    data = await state.get_data()

    # Если список KPI еще не существует, создаем его
    if 'kpi_description' not in data:
        kpi_list = []
    else:
        kpi_list = data['kpi_description']

    # Добавляем новый KPI в список
    kpi_list.append(message.text)

    # Обновляем данные с новым списком KPI
    await state.update_data(kpi_description=kpi_list)

    # Подтверждаем добавление и спрашиваем, нужно ли добавить еще
    await message.answer("KPI добавлен. Добавить еще или завершить?", reply_markup=kpi_risk_keyboard)
    await state.set_state(Form.addMoreKPI)


@dp.message(Form.addMoreKPI)
async def add_more_kpi(message: types.Message, state: FSMContext):
    if message.text == "Завершить":
        # Когда пользователь завершает добавление KPI, показываем все добавленные элементы
        data = await state.get_data()
        kpis = data.get('kpi_description', [])

        # Формируем сообщение с перечислением всех KPI
        await message.answer(f"KPI процесса:\n{'\n'.join(kpis)}", reply_markup=confirm_keyboard)
        await state.set_state(Form.infoBlock6)
    else:
        # Если пользователь хочет добавить новый KPI
        await message.answer("Введите следующий KPI", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.kpiDescription)


@dp.message(Form.infoBlock6)
async def infoBlock6(message: types.Message, state: FSMContext):
    if message.text == "Подтвердить":
        await message.answer("KPI подтверждены", reply_markup=ReplyKeyboardRemove())
        await message.answer("Укажите риски процесса")
        await state.set_state(Form.risksDescription)
    elif message.text == "Редактировать":
        await message.answer("Введите KPI заново", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.kpiDescription)
    else:
        await message.answer("Пожалуйста, используйте кнопки", reply_markup=confirm_keyboard)


@dp.message(Form.risksDescription)
async def risks_description(message: types.Message, state: FSMContext):
    # Получаем текущие данные пользователя из FSMContext
    data = await state.get_data()

    # Если список рисков еще не существует, создаем его
    if 'risks_description' not in data:
        risks_list = []
    else:
        risks_list = data['risks_description']

    # Добавляем новый риск в список
    risks_list.append(message.text)

    # Обновляем данные с новым списком рисков
    await state.update_data(risks_description=risks_list)

    # Подтверждаем добавление и спрашиваем, нужно ли добавить еще
    await message.answer("Риск добавлен. Добавить еще или завершить?", reply_markup=kpi_risk_keyboard)
    await state.set_state(Form.addMoreRisks)


@dp.message(Form.addMoreRisks)
async def add_more_risks(message: types.Message, state: FSMContext):
    if message.text == "Завершить":
        # Когда пользователь завершает добавление рисков, показываем все добавленные риски
        data = await state.get_data()
        risks = data.get('risks_description', [])

        # Формируем сообщение с перечислением всех рисков
        await message.answer(f"Риски процесса:\n{'\n'.join(risks)}", reply_markup=confirm_keyboard)
        await state.set_state(Form.infoBlock7)
    else:
        # Если пользователь хочет добавить новый риск
        await message.answer("Введите следующий риск", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.risksDescription)


@dp.message(Form.infoBlock7)
async def infoBlock7(message: types.Message, state: FSMContext):
    if message.text == "Подтвердить":
        await message.answer("Риски подтверждены", reply_markup=ReplyKeyboardRemove())
        await message.answer("Укажите изображение процесса")
        await state.set_state(Form.processImage)
    elif message.text == "Редактировать":
        await message.answer("Введите риски заново", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.risksDescription)
    else:
        await message.answer("Пожалуйста, используйте кнопки", reply_markup=confirm_keyboard)


@dp.message(Form.processImage)
async def process_image(message: types.Message, state: FSMContext):
    await state.update_data(process_image=message.text)
    data = await state.get_data()
    await message.answer(f"Изображение процесса: {data['process_image']}", reply_markup=final_keyboard)
    await state.set_state(Form.finalConfirmation)



@dp.message(Form.finalConfirmation)
async def final_confirmation(message: types.Message, state: FSMContext):
    if message.text == "Отредактировать":
        await message.answer("Введите название процесса заново", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.reportName)
    elif message.text == "Сбросить":
        await state.clear()
        await message.answer("Все данные сброшены. Начните заново с /start")
    elif message.text == "Выгрузить PDF":
        # Генерация и отправка PDF отчета
        data = user_data
        pdf_file_path = generate_pdf_report(data)  # Генерация PDF отчета
        with open(pdf_file_path, "rb") as pdf_file:
            await message.answer_document(pdf_file)  # Отправка PDF
        await message.answer("Отчет успешно сгенерирован и отправлен.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, используйте кнопки", reply_markup=final_keyboard)


if __name__ == '__main__':
    print("Бот запущен.....")
    dp.run_polling(bot)
