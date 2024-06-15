import logging
from typing import List

import pyperclip
from flet import (
	Page, ControlEvent, MainAxisAlignment, CrossAxisAlignment, TextAlign, FontWeight, icons,
	NumbersOnlyInputFilter, ScrollMode, View, ElevatedButton, Text, TextField, IconButton, Checkbox, Row, Column
)

from alerts import info_alert, show_snackbar
from utilities import *


class MainView:
	def __init__(self, page: Page, /) -> None:
		# Page
		self.page = page

		# Widgets
		self.length_entry = TextField(width=80, value=str(DEFAULT_LENGTH), text_align=TextAlign.CENTER,
		                              input_filter=NumbersOnlyInputFilter(), on_change=self.check_input)
		self.password_text = Text(color='#53a0f0', size=25, weight=FontWeight.BOLD, font_family='JetBrains')
		self.copy_button = ElevatedButton('Copy', icon=icons.COPY, on_click=self.copy_password)
		self.lowercase_checkbox = Checkbox(label='Lowercase', value=True, on_change=self.check_input)
		self.numbers_checkbox = Checkbox(label='Numbers', value=True, on_change=self.check_input)
		self.uppercase_checkbox = Checkbox(label='Uppercase', value=True, on_change=self.check_input)
		self.special_characters_checkbox = Checkbox(
			label='Special Characters', value=True, on_change=self.check_input
		)
		self.generate_button = ElevatedButton(text='Generate', on_click=self.generate)

		# Variables
		self.has_shown_length_warning = False

		# Generate first password
		self.current_password = generate_password(DEFAULT_LENGTH)
		self.password_text.value = self.current_password
		self.page.update()

	@property
	def checkbox_values(self) -> List[bool]:
		return [
			checkbox.value for checkbox in [
				self.lowercase_checkbox, self.uppercase_checkbox, self.numbers_checkbox,
				self.special_characters_checkbox
			]
		]

	def check_input(self, control: ControlEvent) -> None:
		self.generate_button.disabled = (
				self.length_entry.value == '0' or not self.length_entry.value or not any(self.checkbox_values)
		)
		self.page.update()

	def change_length(self, control: ControlEvent, /, length: int) -> None:
		if length_value := self.length_entry.value:
			self.length_entry.value = str(new_length) if (new_length := int(length_value) + length) > 0 else '0'
			self.check_input(control)
			self.page.update()

	def generate(self, control: ControlEvent) -> None:
		if (length := int(self.length_entry.value)) > MAX_LENGTH:
			info_alert(self.page, 'Password is too large!', 'By providing enormous length, the app can stop working.')
			return

		self.current_password = generate_password(length, *self.checkbox_values)

		if length > PAGE_WIDTH / length + 7.5:
			self.password_text.value = f'{self.current_password[:4]}...{self.current_password[-4:]}'
			if not self.has_shown_length_warning:
				show_snackbar(self.page, 'Password is too large for the screen. But it\'s still there.')
				self.has_shown_length_warning = True
		else:
			self.password_text.value = self.current_password

		logging.info(f'Generated password: {self.current_password}')
		self.page.update()

	def copy_password(self, control: ControlEvent) -> None:
		pyperclip.copy(self.current_password)
		logging.info(f'Copied password: {self.current_password}')
		show_snackbar(self.page, 'Password copied!')

	def build(self) -> None:
		view: View = View(
			route='/',
			controls=[
				Column(
					[
						Text('Length', size=20, weight=FontWeight.BOLD, text_align=TextAlign.CENTER),
						Row(
							[
								IconButton(
									icon=icons.REMOVE, icon_size=20,
									on_click=lambda control: self.change_length(control, -1)
								),
								self.length_entry,
								IconButton(
									icon=icons.ADD, icon_size=20,
									on_click=lambda control: self.change_length(control, 1)
								),
							],
							alignment=MainAxisAlignment.CENTER,
							spacing=10
						),
					],
					spacing=5,
					horizontal_alignment=CrossAxisAlignment.CENTER
				),
				Column(
					[
						Text('Include', size=20, weight=FontWeight.BOLD, text_align=TextAlign.CENTER),
						Row(
							[
								Column(
									[
										self.lowercase_checkbox,
										self.numbers_checkbox
									],
									alignment=MainAxisAlignment.CENTER
								),
								Column(
									[
										self.uppercase_checkbox,
										self.special_characters_checkbox
									],
									alignment=MainAxisAlignment.CENTER
								),
							],
							alignment=MainAxisAlignment.CENTER
						),
					],
					spacing=5,
					horizontal_alignment=CrossAxisAlignment.CENTER
				),
				Row(
					[
						self.generate_button,
						self.copy_button
					],
					alignment=MainAxisAlignment.CENTER
				),
				self.password_text
			],
			spacing=30,
			vertical_alignment=MainAxisAlignment.CENTER,
			horizontal_alignment=CrossAxisAlignment.CENTER,
			scroll=ScrollMode.HIDDEN
		)
		self.page.views.append(view)
