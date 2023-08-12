from telegram import InlineKeyboardButton


def create_pagination_buttons(page, total_pages):
    buttons = []
    print('create_button', page)
    # Add "Prev" button if not on the first page
    if page > 0:
        buttons.append(InlineKeyboardButton(
            "⬅️ Prev", callback_data=f"action_prev_{page-1}"))

    label = f"Page {page + 1 } / {total_pages}"
    buttons.append(InlineKeyboardButton(label, callback_data=f"none"))

    # Add "Next" button if not on the last page
    if (page + 1) < total_pages:
        buttons.append(InlineKeyboardButton(
            "Next ➡️", callback_data=f"action_next_{page+1}"))

    return buttons
