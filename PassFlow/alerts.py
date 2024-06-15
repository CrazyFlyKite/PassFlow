from time import sleep
from typing import Optional

from flet import Page, ControlEvent, MainAxisAlignment, Text, TextButton, AlertDialog, SnackBar


def info_alert(page: Page, /, title: str, subtitle: Optional[str] = None) -> None:
	def close_dialog(event: ControlEvent) -> None:
		alert.open = False
		page.update()

	alert: AlertDialog = AlertDialog(
		open=True,
		title=Text(title),
		content=None if subtitle is None else Text(subtitle),
		actions=[TextButton('OK', on_click=close_dialog)],
		actions_alignment=MainAxisAlignment.END
	)

	page.dialog = alert
	page.update()


def show_snackbar(page: Page, /, message: str) -> None:
	page.snack_bar = SnackBar(content=Text(message), action='OK')
	page.snack_bar.open = True
	page.update()
	sleep(1.0)
	page.snack_bar.open = False
	page.update()
