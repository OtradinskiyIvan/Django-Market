# План: удаление страницы тега + кнопки-категории с подсветкой

Утверждён пользователем (ответы: теги в товаре → некликабельные чипы; кнопки категорий → везде; фильтр тегов OR → оставить).

## 1. Удалить страницу тега
- `mysite/catalog/urls.py`: удалить строки 17–18:
  - `path('tag/<int:tag_id>/', tag_by_id, name='catalog_tag_id')`
  - `path('tag/<slug:tag_slug>/', tag_by_slug, name='catalog_tag_slug')`
- `mysite/catalog/views.py`: удалить функции `tag_by_slug` и `tag_by_id` (блоки с `_filter_by_tags(tag.catalog_set...)`).
- Удалить файл `mysite/catalog/templates/catalog/tag.html`.

## 2. Теги на странице товара — некликабельные чипы
- `mysite/catalog/templates/catalog/item.html:22`:
  `<a class="chip" href="{% url 'catalog_tag_id' tag.id %}">#{{ tag.title }}</a>`
  → `<span class="chip">#{{ tag.title }}</span>`

## 3. Кнопки-категории с подсветкой активной
- `mysite/catalog/views.py`: в `category_by_id` и `category_by_slug` добавить в контекст `'current_cat': cat.pk`.
- `mysite/catalog/templatetags/catalog_tags.py`: `show_cats` → `takes_context=True`,
  вернуть `{'cats': Category.objects.all(), 'active_cat': context.get('current_cat')}`.
- `mysite/catalog/templates/catalog/list_cats.html` — полная замена на:
```django
{% load catalog_tags %}
<div class="cat-buttons">
    {% for cat in cats %}
        <a class="cat-btn{% if cat.pk == active_cat %} active{% endif %}" href="{% url 'catalog_cat_id' cat.pk %}">{{ cat.title }}</a>
    {% endfor %}
</div>
```
- `style.css`: добавить
```css
.cat-buttons { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
.cat-btn {
    display: inline-block; padding: 4px 14px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; font-size: .88em; font-weight: bold;
    color: var(--dark); text-decoration: none;
}
.cat-btn:hover { border-color: var(--primary); color: var(--primary); text-decoration: none; }
.cat-btn.active, .cat-btn.active:hover {
    background: var(--primary); border-color: var(--primary); color: #fff;
}
```

## Остаётся без изменений
- Мульти-фильтр тегов `?tags=` (OR) на главной и странице категории (`_filter_by_tags`, форма в `list_tags.html`).
- Дефолтные категории/теги из миграции `0005`.

## Проверка
1. Компиляция всех шаблонов движком.
2. grep: не осталось `catalog_tag` ни в одном шаблоне/модуле.
3. Тест-клиент: `/catalog/tag/1/` → 404; главная 200, кнопки категорий есть, `active` отсутствует; `/catalog/cats/<id>/` — ровно один `.cat-btn active`; страница товара — чипы тегов без `<a>`; `?tags=` фильтр работает; `manage.py check`.
