from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

API_TOKEN = 'Token'

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
    # Получаем текущие данные пользователя
    data = await state.get_data()
    stages_list = data.get('process_stages', [])  # Используем существующий список

    # Если пользователь ввел "Завершить описание", переходим к следующему шагу
    if message.text.strip().lower() == "завершить описание":
        if stages_list:
            await message.answer(f"Этапы процесса:\n{'\n'.join(stages_list)}", reply_markup=confirm_keyboard)
            await state.set_state(Form.materialResources)
            await message.answer("Укажите материальные ресурсы")
        else:
            await message.answer("Список этапов пуст. Добавьте хотя бы один этап.")
        return

    # Добавляем новый этап в список
    stages_list.append(message.text)
    await state.update_data(process_stages=stages_list)

    # Спрашиваем, нужно ли добавить еще
    await message.answer("Этап добавлен. Добавить еще или завершить описание?", reply_markup=stage_keyboard)
    await state.set_state(Form.addMoreStages)


@dp.message(Form.addMoreStages)
async def add_more_stages(message: types.Message, state: FSMContext):
    if message.text.strip().lower() == "завершить описание":
        data = await state.get_data()
        stages = data.get('process_stages', [])

        if stages:
            await message.answer(f"Этапы процесса:\n{'\n'.join(stages)}", reply_markup=confirm_keyboard)
            await state.set_state(Form.materialResources)
            await message.answer("Укажите материальные ресурсы")
        else:
            await message.answer("Список этапов пуст. Добавьте хотя бы один этап.")
        return

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


from aiogram import F


@dp.message(Form.processImage, F.photo)
async def process_image(message: types.Message, state: FSMContext):
    # Получаем file_id изображения
    photo_id = message.photo[-1].file_id  # Берем самую качественную версию фото

    # Обновляем данные в состоянии
    await state.update_data(process_image=photo_id)
    data = await state.get_data()

    # Отправляем подтверждение пользователю
    await message.answer_photo(photo_id, caption="Изображение процесса сохранено.", reply_markup=final_keyboard)

    # Переход к следующему шагу
    await state.set_state(Form.finalConfirmation)


# Обработчик на случай, если пользователь отправил не фото
@dp.message(Form.processImage)
async def process_image_invalid(message: types.Message):
    await message.answer("Пожалуйста, отправьте изображение, а не текст.")


@dp.message(Form.finalConfirmation)
async def final_confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == "Отредактировать":
        await message.answer("Введите изображение заново", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.processImage)
    elif message.text == "Сбросить":
        await state.clear()
        await message.answer("Процесс сброшен. Начинаем заново.", reply_markup=ReplyKeyboardRemove())
        await message.answer("Введите название процесса", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.reportName)
    else:
        await message.answer("Отчет успешно завершен!", reply_markup=ReplyKeyboardRemove())

        # Формирование полного отчета
        data = await state.get_data()
        report = (
            f"Название процесса: {data['process_name']}\n"
            f"Имя владельца: {data['user_name']}\n"
            f"Тип процесса: {data['type_name']}\n"
            f"Цель процесса: {data['process_goal']}\n"
            f"Критерии успеха: {data['success_criteria']}\n"
            f"Входы процесса: {data['process_inputs']}\n"
            f"Выходы процесса: {data['process_outputs']}\n"
            f"Границы процесса: {data['process_boundaries']}\n"
            f"Владелец процесса: {data['process_owner']}\n"
            f"Исполнитель процесса: {data['process_executor']}\n"
            f"Внешние участники: {data['external_participants']}\n"
            f"Этапы процесса: {', '.join(data.get('process_stages', []))}\n"
            f"Материальные ресурсы: {data['material_resources']}\n"
            f"Информационные ресурсы: {data['info_resources']}\n"
            f"Программные ресурсы: {data['software_resources']}\n"
            f"KPI процесса: {', '.join(data.get('kpi_description', []))}\n"
            f"Риски процесса: {', '.join(data.get('risks_description', []))}\n"
            f"Изображение процесса: {data['process_image']}\n"
        )
        print(data)

        await message.answer(f"Вот ваш финальный отчет:\n{report}", reply_markup=ReplyKeyboardRemove())

        # Здесь можно добавить код для экспорта отчета в PDF
        await state.clear()

if __name__ == '__main__':
    print("Бот запущен.....")
    dp.run_polling(bot)