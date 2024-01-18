from __future__ import annotations

import sys

import typing as t

from asciimatics.widgets import Frame
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.effects import Julia, Print, Matrix
from asciimatics.renderers import FigletText
from asciimatics import constants as C

from menu import DirectoryFrame, ExceptionFrame, ConfigFrame
from config import CONFIG





def error_handling_views(screen: Screen, exception: Exception, scene: Scene):
    """Function to be wrapped for handling error views

    Args:
        screen (Screen): Current screen object
        exception (Exception): Caught Exception object
        scene (Scene): Previous scene to start on
    """
    warning = FigletText("EXCEPTION", "univers", screen.width)
    warning_x = screen.width//2 - warning.max_width//2
    warning_y = screen.height//2 - warning.max_height//2
    
    exception_view = ExceptionFrame(screen, exception)
    exception_view.set_theme("green")
    
    exception_interaction = []
    if not CONFIG.get("optimised_error_handler", True):
        exception_interaction.append(Matrix(screen))
    exception_interaction.append(exception_view)
    
    scenes = [
        Scene([exception_view, Print(screen, warning, warning_y, warning_x, transparent=False, attr=C.A_BOLD, colour=C.COLOUR_GREEN)], 18),
        Scene(exception_interaction, -1, "exception_handler")
    ]
    
    screen.play(
        scenes,
        stop_on_resize=True,
        start_scene = scene
    )



def error_handler(exception: Exception):
    """Handles caught exceptions

    Args:
        exception (Exception): Caught Exception object
    """
    last_scene: t.Optional[Scene] = None
    
    while True:
        try:
            Screen.wrapper(error_handling_views, arguments=[exception, last_scene])
            main()
        except ResizeScreenError as e_:
            last_scene = e_.scene


def global_shortcuts(event):
    if isinstance(event, KeyboardEvent):
        c = event.key_code
        # Stop on ctrl+q or ctrl+x
        if c in (17, 24):
            raise StopApplication("User terminated app")
        if c == 5:
            raise Exception("User Terminated app")
        
        
        


def start_terminal_menu(screen: Screen, scene: Scene) -> None:
    """Handles PST terminal application views and scenes

    Args:
        screen (Screen): current screen object
        scene (Scene): Previous scene to start on
    """

    scenes: list[Scene] = [
        Scene(
            [DirectoryFrame(
                screen, 
                [
                    ("View Profile Database", ""),
                    ("System Config", "system_config")
                ],
                "PST Main Directory",
                "The PST project is a system designed for tracking profiles and managing information regarding personel"
            )], 
            -1, 
            name="main"
        ),
        Scene(
            [ConfigFrame(screen, CONFIG)],
            -1,
            name="system_config"
        )
    ]

    screen.play(
        scenes,
        stop_on_resize=True,
        start_scene = scene,
        unhandled_input=global_shortcuts
    )
    


def main() -> None:
    """Starts PST terminal application"""
    last_scene: t.Optional[Scene] = None

    while True:
        try:
            Screen.wrapper(start_terminal_menu, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
        except Exception as e:
            error_handler(e)




if __name__ == "__main__":
    # Startup tasks
    
    # Run target
    main()
    
    # Closing Tasks
    