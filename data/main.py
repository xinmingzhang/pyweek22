from . import prepare,tools
from .states import title_screen,intro,level_play,world_info,end_screen

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION, prepare.ICON)
    states = {"TITLE": title_screen.TitleScreen(),
              'INTRO':intro.Intro(),
              'BOTTOM':world_info.bottom_info,
              'BOTUP':world_info.bottup_info,
              'UPPER':world_info.upper_info,
              "LEVELPLAY":level_play.LevelPlay(),
              'WIN':end_screen.win,
              'LOSE':end_screen.lose}
    controller.setup_states(states, "TITLE")
    controller.main()