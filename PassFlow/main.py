import logging

from flet import app, Page, Theme, MainAxisAlignment, CrossAxisAlignment, RouteChangeEvent, ViewPopEvent

from main_view import MainView
from setup_logging import setup_logging
from utilities import *


def main(page: Page) -> None:
	page.title = PAGE_TITLE
	page.window_width = PAGE_WIDTH
	page.window_height = PAGE_HEIGHT
	page.window_resizable = PAGE_RESIZABLE
	page.horizontal_alignment = CrossAxisAlignment.CENTER
	page.vertical_alignment = MainAxisAlignment.CENTER
	page.fonts = {
		'JetBrains': './../assets/fonts/JetBrains Mono.ttf',
		'Helvetica Neue': './../assets/fonts/Helvetica Neue.ttf'
	}
	page.theme = Theme(font_family='Helvetica Neue')

	# Setup logging
	setup_logging(level=logging.INFO, logging_format='[%(levelname)s] - %(message)s')

	def route_change(event: RouteChangeEvent) -> None:
		page.views.clear()
		MainView(page).build()

	def view_pop(event: ViewPopEvent) -> None:
		page.views.pop()
		page.go(page.views[-1].route)

	page.on_route_change = route_change
	page.on_view_pop = view_pop
	page.go(page.route)


if __name__ == '__main__':
	app(target=main, assets_dir='../assets')
