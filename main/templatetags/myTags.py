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
            <button type="button" class="btn btn-outline-success mt-3" id="btnGoTo{siguiente_id}">
                Siguiente
            </button>
        </div>
        '''
    return mark_safe(html)
