from django import template

register = template.Library()


@register.filter
def format_phone(phone) -> str:
    """
    Форматирует телефонный номер в виде +7(XXX)-XXX-XX-XX
    """
    if phone and len(phone) == 11:
        return f"+{phone[:1]}({phone[1:4]})-{phone[4:7]}-{phone[7:9]}-{phone[9:]}"
    return "Некорректный номер телефона"
