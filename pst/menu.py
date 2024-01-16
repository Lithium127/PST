
import sys
import traceback as tb

from asciimatics.screen import Screen
from asciimatics import widgets as w
from asciimatics.exceptions import NextScene, StopApplication


class BaseFrame(w.Frame):
    def __init__(self, screen: Screen, title = None, *, height = None, width = None, hover_focus = True) -> None:
        super(BaseFrame, self).__init__(
            screen,
            height or screen.height * 3//4,
            width or min(screen.width * 3//4, 100), # Convert to max in config
            hover_focus=hover_focus,
            title=title
        )



class DirectoryFrame(BaseFrame):
    """Frame for listing and navigating directories"""
    def __init__(
        self, 
        screen: Screen, 
        scene_options: list[tuple[str, str]], 
        title: str = "Directory",
        description: str = None
        ) -> None:
        """Frame that lists and navigates a directory

        Args:
            screen (Screen): Current Screen object
            scene_options (list[tuple[str, str]]): List containing directory options
            title (str, optional): Title of the Frame. Defaults to "Directory".
            description (str, optional): Description to add to the frame. Defaults to None.
        """
        
        super(DirectoryFrame, self).__init__(screen,title)

        self.layout = w.Layout([100], fill_frame=True)
        if description is not None:
            self.layout = w.Layout([59,2,39], fill_frame=True)
        
            
        self.add_layout(self.layout)

        self.layout.add_widget(w.Label("Options"), 0)
        self.layout.add_widget(w.Divider(), 0)
        self.layout.add_widget(w.ListBox(
            w.Widget.FILL_FRAME,
            scene_options,
            name="directory"
        ), 0)
        self.layout.add_widget(w.Divider(), 0)
        self.layout.add_widget(w.Button("Open", self._open_list), 0)

        if description is not None:
            
            self.layout.add_widget(w.VerticalDivider(), 1)
            
            desc: w.Widget = self.layout.add_widget(w.TextBox(
                w.Widget.FILL_COLUMN,
                line_wrap = True,
                readonly  = True,
                disabled  = True,
                as_string = True
            ),2)
            
            desc.value = description

        self.fix()
    
    def _open_list(self):
        """Opens currently selected entry in directory list

        Raises:
            NextScene: Moves to next scene
        """
        raise NextScene(self.data["directory"])



class ExceptionFrame(BaseFrame):
    """
    Class for rendering caught exceptions and displaying their content to the terminal
    without stopping application unexpectedly. Provides options to exit with a normal
    error code, return to application, or to quit with error code
    """

    def __init__(self, screen: Screen, exception: Exception) -> None:
        """Renders caught exceptions

        Args:
            screen (Screen): Current Screen object
            exception (Exception): Caught Exception object
        """
        super(ExceptionFrame, self).__init__(screen, f"ERROR: [{exception.__class__.__name__}]")
        
        self._exception = exception
        self._traceback = exception.__traceback__
        self._traceback_str = tb.format_exception(self._exception)
        
        error = w.Layout([100], fill_frame=True)
        
        self.add_layout(error)
        
        error.add_widget(w.Label(f"Exception on line {self._traceback.tb_lineno}"))
        
        error.add_widget(w.Divider())
        
        traceback: w.Widget = error.add_widget(w.TextBox(
            w.Widget.FILL_FRAME,
            line_wrap = True,
            readonly  = True,
            disabled  = True,
            as_string = True
        ))
        traceback.value = "\n\n".join(self._traceback_str)
        
        error.add_widget(w.Divider())
        
        buttons = w.Layout([1,1,1])
        self.add_layout(buttons)
        
        buttons.add_widget(w.Button("Return to Main", self._return), 0)
        buttons.add_widget(w.Button("Trace", self._trace), 1)
        buttons.add_widget(w.Button("Close", self._close), 2)
        
        self.fix()
        
    def _return(self):
        """Returns to PST terminal application

        Raises:
            StopApplication: Safely stops ExceptionFrame
        """
        raise StopApplication("Returning to PST")
    
    def _trace(self):
        """Quits application by raising caught exception

        Raises:
            self._exception: Caught Exception object
        """
        raise self._exception
    
    def _close(self):
        """Force stops application and exits with code 0"""
        sys.exit(0)
        