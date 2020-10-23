import pyodide
import sys
from js import document


class BasthonNamespace(object):
    """
    A class that acts as a namespace for Basthon methods.
    This is the part of Basthon implemented in Python that would be loaded
    in the global namspace. Code evaluation would be executed in separate
    namespace that can be cleared (this simulate the kernel restart).
    """

    class StreamManager(object):
        """
        A class to catch stderr/stdout input during eval.
        """
        def __init__(self, stream, flush_callback):
            self.stream = stream
            self.callback = flush_callback
            std = getattr(sys, stream)
            self.std = std
            self.buff = ""
            self.write_bck = std.write
            self.flush_bck = std.flush
            std.write = self.write
            std.flush = self.flush

        def __del__(self):
            self.close()

        def write(self, data):
            self.buff += data
            return len(data)

        def flush(self):
            if not self.buff:
                return
            self.callback(self.buff)
            self.buff = ""

        def close(self):
            self.flush()
            self.std.write = self.write_bck
            self.std.flush = self.flush_bck

    def __init__(self):
        self.execution_count = None
        self._namespace = None
        self.start()

    def start(self):
        """
        Start the Basthon kernel and fill the namespace.
        """
        self.execution_count = 0
        self._namespace = {
            '__name__': '__main__',
            '_': '',
            '__': '',
            '___': '',
            'In': [''],
            'Out': {}
        }

    def stop(self):
        """
        Stop the Basthon kernel.
        """
        pass

    def restart(self):
        """
        Restart the Basthon kernel.
        """
        self.stop()
        self.start()

    def roll_in_history(self, code):
        """ Manage storing in 'In' ala IPython. """
        self._namespace['In'].append(code)

    def roll_out_history(self, out):
        """ Manage storing in 'Out', _, __, ___ ala IPython. """
        outputs = self._namespace['Out']
        # out is not always stored
        if out is not None and out is not outputs:
            outputs[self.execution_count] = out
            self._namespace['___'] = self._namespace['__']
            self._namespace['__'] = self._namespace['_']
            self._namespace['_'] = out

    def eval(self, code, data=None):
        """
        Kernel function to evaluate Python code.
        data can be accessed in code through '__eval_data__' variable
        in gobal namespace.
        """
        self._namespace['__eval_data__'] = data
        res = pyodide.eval_code(code, self._namespace)
        del self._namespace['__eval_data__']
        return res

    def shell_eval(self, code, stdout_callback, stderr_callback, data=None):
        """
        Evaluation of Python code with communication managment
        with the JS part of Basthon and stdout/stderr catching.
        data can be accessed in code through '__eval_data__' variable
        in global namespace.
        """
        self.execution_count += 1
        self.roll_in_history(code)

        stdout_manager = BasthonNamespace.StreamManager("stdout", stdout_callback)
        stderr_manager = BasthonNamespace.StreamManager("stderr", stderr_callback)

        try:
            _ = self.eval(code, data=data)
        except Exception:
            raise
        else:
            self.roll_out_history(_)
            if _ is not None:
                res = {"text/plain": repr(_)}
                if hasattr(_, "_repr_html_"):
                    res["text/html"] = _._repr_html_()
                return res
        finally:
            stdout_manager.close()
            stderr_manager.close()

    def format_display_data(self, data):
        """
        Updating display data with evaulation data.
        """
        res = {}
        # get evaluation data from namespace
        eval_data = self._namespace['__eval_data__']
        if eval_data is not None:
            res.update(eval_data)
        res.update(data)
        return res

    def hack_matplotlib(self, callback_display):
        """
        Hack the Wasm backend of matplotlib to render figures.
        """
        from matplotlib.backends.wasm_backend import FigureCanvasWasm as wasm_backend

        # preserve access to self
        this = self

        # hacking root node creation
        def create_root_element(self):
            self.root = document.createElement("div")
            return self.root

        wasm_backend.create_root_element = create_root_element

        # hacking show (plugging to callback)
        if not hasattr(wasm_backend, "_original_show"):
            wasm_backend._original_show = wasm_backend.show

        def show(self):
            res = self._original_show()
            callback_display(this.format_display_data(
                {"display_type": "matplotlib",
                 "content": self.root}))
            return res

        show.__doc__ = wasm_backend._original_show.__doc__
        wasm_backend.show = show

    def hack_turtle(self, callback_display):
        """
        Hack Turtle to render figures.
        """
        from turtle import Screen

        # preserve access to self
        this = self

        # hacking show_scene (plugging to callback)
        if not hasattr(Screen, "_original_show_scene"):
            Screen._original_show_scene = Screen.show_scene

        def show_scene(self):
            root = self._original_show_scene()
            callback_display(this.format_display_data(
                {"display_type": "turtle",
                 "content": root}))
            self.restart()

        show_scene.__doc__ = Screen._original_show_scene.__doc__

        Screen.show_scene = show_scene

    def hack_sympy(self, callback_display):
        """
        Hack Sympy to render expression using LaTeX (and probably MathJax).
        """
        import sympy

        # preserve access to self
        this = self

        def pretty_print(*args, sep=' '):
            """
            Print arguments in latex form.
            """
            latex = sep.join(sympy.latex(expr) for expr in args)
            callback_display(this.format_display_data(
                {"display_type": "sympy",
                 "content": "$${}$$".format(latex)}))

        sympy.pretty_print = pretty_print

    def hack_folium(self, callback_display):
        """
        Hack Folium to render maps.
        """
        from folium import Map

        # preserve access to self
        this = self

        def display(self):
            """
            Render map to html.
            """
            callback_display(this.format_display_data(
                {"display_type": "html",
                 "content": self._repr_html_()}))

        Map.display = display

    def hack_pandas(self, callback_display):
        """
        Hack Pandas to render data frames.
        """
        from pandas import DataFrame

        # preserve access to self
        this = self

        def display(self):
            """
            Render data frame to html.
            """
            callback_display(this.format_display_data(
                {"display_type": "html",
                 "content": self._repr_html_()}))

        DataFrame.display = display


Basthon = BasthonNamespace()
