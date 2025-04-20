from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def opciones_respuesta(id):
    id = int(id)
    siguiente_id = id + 1
    html = f'''
    <div class="form-check py-3">
        <input class="form-check-input" type="radio" name="p{id}" id="p{id}-1" value="0" required>
        <label class="form-check-label" for="p{id}-1">
            No describe nada de lo que me pasó o sentí en la semana
        </label>
    </div>
    <div class="form-check py-3">
        <input class="form-check-input" type="radio" name="p{id}" id="p{id}-2" value="1">
        <label class="form-check-label" for="p{id}-2">
            Sí, esto me pasó o lo sentí en alguna medida o en algún momento
        </label>
    </div>
    <div class="form-check py-3">
        <input class="form-check-input" type="radio" name="p{id}" id="p{id}-3" value="2">
        <label class="form-check-label" for="p{id}-3">
            Sí, esto me pasó bastante o lo sentí muchas veces
        </label>
    </div>
    <div class="form-check py-3">
        <input class="form-check-input" type="radio" name="p{id}" id="p{id}-4" value="3">
        <label class="form-check-label" for="p{id}-4">
            Sí, esto me pasó mucho o casi siempre
        </label>
    </div>
    '''
    if id != 21:
        html += f'''
        <div class="float-end">
            <button type="button" class="btn btn-outline-success m-3 w-150" id="btnGoTo{siguiente_id}">
                Siguiente
            </button>
        </div>
        '''
    return mark_safe(html)

@register.simple_tag
def DepressionReport(questionnaire):
    score = questionnaire.getDepressionScore()
    print("getDepressionScore", score)
    if score <= 7:
        html = f'''
        <b>Nivel 1: Leve o sin síntomas significativos</b>
        <p class="text-justify">
            Tus respuestas indican que actualmente no estás presentando síntomas significativos de depresión. Te percibes con energía, con capacidad para disfrutar cosas positivas, motivarte y ver sentido en tu vida. Aunque es normal tener altibajos, tu estado emocional general se mantiene estable.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Mantén rutinas saludables: duerme bien, aliméntate de forma equilibrada.</li>
            <li>Realiza ejercicio físico de forma regular.</li>
            <li>Practica la gratitud y el autocuidado.</li>
            <li>Dedica tiempo a tus pasatiempos o actividades que disfrutes.</li>
            <li>Cuida tus relaciones sociales, exprésate y mantente conectado con quienes te rodean.</li>
        </ul>
        '''
    elif score >= 8 and score <= 14:
        html = f'''
        <b>Nivel 2: Moderado</b>
        <p class="text-justify">
            Tus respuestas reflejan que podrías estar experimentando algunos síntomas de depresión. Quizás sientas falta de energía, dificultades para disfrutar cosas que antes te gustaban, pensamientos negativos o una disminución en tu motivación.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Intenta mantener una rutina diaria que te ayude a organizar tu tiempo.</li>
            <li>Busca actividades que te generen pequeños momentos de placer o satisfacción.</li>
            <li>Habla con alguien de confianza sobre cómo te sientes.</li>
            <li>Practica técnicas de relajación o mindfulness.</li>
            <li>Considera buscar orientación psicológica si los síntomas persisten o se intensifican.</li>
        </ul>
        '''
    else:
        html = f'''
        <b>Nivel 3: Grave</b>
        <p class="text-justify">
            Tus respuestas muestran indicadores claros de síntomas depresivos intensos. Puede que estés experimentando pensamientos negativos constantes, desesperanza, fatiga profunda, falta de motivación, o pensamientos relacionados con la vida y la muerte.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Es fundamental que busques ayuda psicológica profesional lo antes posible.</li>
            <li>No enfrentes esto solo/a. Habla con una persona cercana y coméntale lo que estás sintiendo.</li>
            <li>Evita el aislamiento y establece pequeñas metas diarias.</li>
            <li>Considera acudir a un centro de salud, un psicólogo o una línea de atención emocional.</li>
        </ul>
        '''

    return mark_safe(html)

@register.simple_tag
def AnxietyReport(questionnaire):
    score = questionnaire.getAnxietyScore()
    print("getAnxietyScore", score)
    
    if score <= 7:
        html = f'''
        <b>Nivel 1: Leve o sin síntomas significativos</b>
        <p class="text-justify">
            Tus respuestas no reflejan síntomas preocupantes de ansiedad. Tu cuerpo y mente parecen responder con normalidad ante el estrés y no hay evidencia de tensión, miedo o preocupaciones constantes que te afecten.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Mantente activo físicamente.</li>
            <li>Realiza respiración profunda o meditación en tu día a día.</li>
            <li>Evita el consumo excesivo de café u otros estimulantes.</li>
            <li>Crea espacios de descanso y desconexión.</li>
        </ul>
        '''
    elif 8 <= score <= 14:
        html = f'''
        <b>Nivel 2: Moderado</b>
        <p class="text-justify">
            Tus respuestas indican que podrías estar sintiendo ansiedad con cierta frecuencia. Podrías experimentar inquietud, tensión, palpitaciones, pensamientos intrusivos o dificultad para relajarte.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Practica técnicas de respiración, relajación muscular progresiva o mindfulness.</li>
            <li>Establece rutinas y evita la sobrecarga de tareas.</li>
            <li>Limita el tiempo en redes sociales o noticias que puedan intensificar tus síntomas.</li>
            <li>Considera hablar con un profesional de salud mental si estos síntomas interfieren en tu rutina diaria.</li>
        </ul>
        '''
    else:
        html = f'''
        <b>Nivel 3: Grave</b>
        <p class="text-justify">
            Tus respuestas muestran signos claros de ansiedad elevada. Puedes estar experimentando crisis de pánico, miedo sin causa aparente, dificultades para dormir, sensaciones físicas de alerta constante o pensamientos de catástrofe.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Busca ayuda psicológica profesional de forma inmediata.</li>
            <li>Prioriza tu salud mental: reduce obligaciones, delega tareas y enfócate en tu bienestar.</li>
            <li>Evita el aislamiento y habla con personas de confianza.</li>
            <li>Considera acudir a un centro de salud o línea de atención emocional.</li>
        </ul>
        '''

    return mark_safe(html)

@register.simple_tag
def StressReport(questionnaire):
    score = questionnaire.getStressScore()
    print("getStressScore", score)
    if score <= 7:
        html = f'''
        <b>Nivel 1: Leve o sin síntomas significativos</b>
        <p class="text-justify">
            Tus respuestas indican un manejo saludable del estrés. No presentas síntomas físicos o emocionales que afecten tu vida diaria. Tienes una buena capacidad de adaptación ante situaciones exigentes.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Mantén hábitos saludables y un buen equilibrio entre trabajo, estudio y descanso.</li>
            <li>Realiza pausas activas y ejercicios de respiración.</li>
            <li>Cuida tu entorno social y date espacios para desconectar.</li>
        </ul>
        '''
    elif score >= 8 and score <= 14:
        html = f'''
        <b>Nivel 2: Moderado</b>
        <p class="text-justify">
            Tus respuestas muestran signos de estrés moderado. Puedes estar sintiéndote irritado/a, sobrecargado/a o con dificultades para concentrarte y relajarte.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Establece prioridades y organiza tus actividades con pausas programadas.</li>
            <li>Evita la multitarea y enfócate en una cosa a la vez.</li>
            <li>Practica actividad física, técnicas de relajación o expresión emocional.</li>
            <li>Si el estrés interfiere en tu vida diaria, considera buscar orientación psicológica.</li>
        </ul>
        '''
    elif score >= 15:
        html = f'''
        <b>Nivel 3: Grave</b>
        <p class="text-justify">
            Tus respuestas reflejan un nivel alto de estrés. Puede que sientas tensión constante, dificultades para relajarte, reacciones explosivas, fatiga o incluso problemas físicos.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Busca ayuda psicológica profesional.</li>
            <li>Haz pausas profundas y prioriza el descanso.</li>
            <li>Establece rutinas simples y realistas.</li>
            <li>Evita ambientes que generen alta sobrecarga emocional.</li>
        </ul>
        '''
    
    return mark_safe(html)


@register.simple_tag
def GlobalReport(questionnaire):
    score = questionnaire.getGlobalScore()
    print("getGlobalScore", score)
    
    if score <= 20:
        html = f'''
        <b>Nivel 1: Leve o sin síntomas significativos</b>
        <p class="text-justify">
            No se observa un nivel alto de malestar emocional general. Tu estado anímico, tu capacidad para gestionar el estrés y los niveles de ansiedad se encuentran en equilibrio.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Continúa con tus hábitos saludables.</li>
            <li>Mantén espacios de autocuidado.</li>
            <li>Refuerza tus redes de apoyo.</li>
        </ul>
        '''
    elif score >= 21 and score <= 42:
        html = f'''
        <b>Nivel 2: Moderado</b>
        <p class="text-justify">
            Hay presencia moderada de malestar emocional. Tus niveles de estrés, ansiedad o depresión podrían estar afectando algunas áreas de tu vida.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Identifica los focos principales de malestar.</li>
            <li>Establece pequeños cambios que puedas implementar de inmediato.</li>
            <li>Busca ayuda profesional si notas que esto persiste o interfiere en tu rutina.</li>
        </ul>
        '''
    elif score >= 43:
        html = f'''
        <b>Nivel 3: Grave</b>
        <p class="text-justify">
            Se identifican niveles altos de malestar emocional general. Es posible que estés enfrentando varias dificultades al mismo tiempo, con sensaciones de agobio, tristeza o desesperanza.
        </p>
        <b>Recomendaciones:</b>
        <ul>
            <li>Es prioritario que busques atención psicológica.</li>
            <li>No enfrentes esto solo/a. Acude a tu red de apoyo y exprésate.</li>
            <li>Si sientes que no puedes manejar la situación, contacta una línea de ayuda o centro de salud mental.</li>
        </ul>
        '''
    
    return mark_safe(html)
